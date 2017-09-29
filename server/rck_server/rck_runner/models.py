from django.db import models
import random
import datetime
import json
from celery import group, chain, chord, result
from django.conf import settings

# def set_upload_name(instance):
# 	return instance.pk +"/"+ instance.pk + "_" + filetype

class Genome(models.Model):
	name = models.CharField(max_length=20)
	genome_file = models.FileField()



class RckPredictionResult(models.Model):
	width = models.IntegerField()


class RckPredictionSingle(models.Model):
	prediction_result = models.ForeignKey(RckPredictionResult, on_delete=models.CASCADE)
	sequence = models.TextField()
	score = models.FloatField()

class RckPreloadedRBP(models.Model):
	name = models.CharField(max_length=25)


class RckPreloadedModel(models.Model):
	rbp_name = models.ForeignKey(RckPreloadedRBP, on_delete=models.CASCADE)
	width = models.IntegerField()
	model_file = models.FileField()


class RckInference(models.Model):

	INPUT_CHOICES = (
		("pos_neg", "Positive and Negative Sequences"),
		("bed", "Positive BED Peaks"),
		("seq_intens_fasta", "Sequences and Intensities (BED)"),
		("seq_intens_bed", "Sequences and Intensities (BED)"),
		("rck", "RCK/RNAContext Format Input"),
	)

	ANNOT_ALPHABET_CHOICES = (
		("PHIME", "PHIME"),
		("PU", "PU")
	)

	task_id = models.CharField(primary_key=True, unique=True, max_length=10)
	task_dir = models.CharField(max_length=100)

	input_format = models.CharField(max_length=15, choices=INPUT_CHOICES)

	pos_seq_file = models.FileField(upload_to="uploads/"+str(random.randint(0, 999999999)))
	neg_seq_file = models.FileField(upload_to="uploads/"+str(random.randint(0, 999999999)))
	seq_fasta_file = models.FileField(upload_to="uploads/"+str(random.randint(0, 999999999)))
	seq_bed_file = models.FileField(upload_to="uploads/"+str(random.randint(0, 999999999)))
	intens_file = models.FileField(upload_to="uploads/"+str(random.randint(0, 999999999)))
	rck_file = models.FileField(upload_to="uploads/"+str(random.randint(0, 999999999)))

	genome = models.ForeignKey(Genome, on_delete=models.SET_NULL, null=True)

	generate_annotations = models.NullBooleanField(null=True)
	alphabet = models.CharField(max_length=4, choices=ANNOT_ALPHABET_CHOICES)

	annotations_file = models.FileField(upload_to="uploads/"+str(random.randint(0, 999999999)))

	min_width = models.IntegerField(null=True)
	max_width = models.IntegerField(null=True)
	max_iterations = models.IntegerField(null=True)
	num_x_val = models.IntegerField(null=True)

	complete = models.BooleanField(default=False)
	success = models.NullBooleanField(null=True)
	error_message = models.TextField()
	error_linenum = models.IntegerField(null=True)
	error_filetype = models.TextField()
	error_culprit = models.TextField()


	@classmethod
	def create(cls, post_request, files_request):
		ID_LEN = 6
		CHARS = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNPQRSTUVWXYZ123456789"
		task_id_init = "".join(random.choice(CHARS) for _ in xrange(ID_LEN))
		task_instance = cls(task_id=task_id_init, task_dir="inference/"+task_id_init)
		FORM_MAP = {
			"input_format": task_instance.input_format,
			"pos_seq": task_instance.pos_seq_file,
			"neg_seq": task_instance.neg_seq_file,
			"seq_fasta": task_instance.seq_fasta_file,
			"seq_bed": task_instance.seq_bed_file,
			"intens": task_instance.intens_file,
			"rck_in": task_instance.rck_file,
			"genome": task_instance.genome,
			"generate_annotations": task_instance.generate_annotations,
			"alphabet": task_instance.alphabet,
			"annotations": task_instance.annotations_file,
			"min_width": task_instance.min_width,
			"max_width": task_instance.max_width,
			"max_iterations": task_instance.max_iterations,
			"num_x_val": task_instance.num_x_val
		}
		for i in post_request:
			FORM_MAP[i] = post_request[i]
		for i in files_request:
			FORM_MAP[i] = files_request[i]
		task_instance.save()
		return task_instance

	def start_rck(self):
		from .tasks import *

		TASK_TYPE = "inference"
		task_id = self.task_id
		media_root = settings.MEDIA_ROOT
		job_path = media_root + "/" + self.task_dir
		seq_path = job_path + "/" + task_id + "_seq"
		annotations_path = job_path + "/" + task_id + "_struc"
		input_format = self.input_format
		generate_annotations = self.generate_annotations
		alphabet = self.alphabet
		genome_path = media_root + "/" + self.genome.genome_file.name
		numxval = int(self.num_x_val)
		min_width = int(self.min_width)
		max_width = int(self.max_width)
		max_iterations = self.max_iterations
		widths = range(min_width, max_width + 1)
		upload_paths_dict = {
			"pos_seq": media_root + "/" + self.pos_seq_file.name,
			"neg_seq": media_root + "/" + self.neg_seq_file.name,
			"seq_fasta": media_root + "/" + self.seq_fasta_file.name,
			"seq_bed": media_root + "/" + self.seq_bed_file.name,
			"intens": media_root + "/" + self.intens_file.name,
			"rck": media_root + "/" + self.rck_file.name
		}
		annotations_upload_path = media_root + "/" + self.annotations_file.name

		bedtools_path = settings.BASE_DIR+"/rck_runner/resources/bedtools2/bin/bedtools"
		bed_output_path = job_path + "/model/" + task_id + "_bed_sequences"
		bed_control_path = job_path + "/model/" + task_id + "_bed_control"
		bedtools_args_dicts = [{
			"-fi": media_root + self.seq_bed.name,
			"-fo": bed_output_path,
			"-bed": bedtools_path
		}]
		if input_format == "bed":
			bedtools_args_dicts.append(
				{
					"-fi": bed_output_path,
					"-fo": bed_control_path,
					"-bed": bedtools_path
				}
			)

		rnaplfold_path = settings.BASE_DIR+"/rck_runner/resources/RNAplfold"
		rnaplfold_args_dict = {
			"-W": "240",
			"-L": "160",
			"-u": "1",
		}

		rck_path =settings.BASE_DIR+"/rck_runner/resources/RCK/bin/rnacontext"
		rck_args_dicts = [{
			"-a": "ACGU",
			"-e": alphabet,
			"-w": str(min_width) + "-" + str(max_width),
			"-c": job_path + "/model/" + task_id + "_sequences",
			"-d": job_path + "/model/" + task_id + "_sequences_dummy",
			"-h": job_path + "/model/" + task_id + "_annotations",
			"-n": job_path + "/model/" + task_id + "_annotations_dummy",
			"-m": job_path + "/model/" + "RCK_output",
			# "-l": "",
			"-o": task_id,
			"-s": "3",
			"-b": str(max_iterations)
		}]
		for i in xrange(numxval):
			rck_args_dicts.append({
				"-a": "ACGU",
				"-e": "PHIME",
				"-w": str(min_width) + "-" + str(max_width),
				"-c": job_path + "/xval/" + str(i) + "/" + task_id + "_sequences_train",
				"-d": job_path + "/xval/" + str(i) + "/" + task_id + "_sequences_test",
				"-h": job_path + "/xval/" + str(i) + "/" + task_id + "_annotations_train",
				"-n": job_path + "/xval/" + str(i) + "/" + task_id + "_annotations_test",
				"-m": job_path + "/xval/" + str(i) + "/" + "RCK_output",
				# "-l": "",
				"-o": task_id,
				"-s": "3",
				"-b": str(max_iterations)
			})

		tasks = []

		if input_format == "bed" or input_format == "seq_intens_bed":
			tasks.append(
				bed_extract_task.si(
					TASK_TYPE,
					task_id, 
					bedtools_args_dicts,
					bedtools_path,
					genome_path, 
					upload_paths_dict, 
					input_format, 
					seq_path,
					bed_output_path, 
					bed_control_path
				)
			)
		else:
			tasks.append(
				verify_sequences_task.si(
					TASK_TYPE,
					task_id, 
					upload_paths_dict, 
					seq_path, 
					input_format
				)
			)

		if generate_annotations:
			tasks.append(
				create_annotations_task.si(
					TASK_TYPE,
					task_id, 
					job_path, 
					seq_path, 
					annotations_path, 
					rnaplfold_args_dict, 
					rnaplfold_path, 
					alphabet
				)
			)
		else:
			tasks.append(
				verify_annotations_task.si(
					TASK_TYPE,
					task_id, 
					seq_path,
					annotations_upload_path, 
					annotations_path, 
					alphabet
				)
			)

		tasks.append(
			create_RCK_model_task.si(
				TASK_TYPE,
				task_id, 
				job_path, 
				seq_path, 
				annotations_path, 
				rck_args_dicts, 
				alphabet, 
				numxval
			)
		)

		tasks.append(
			make_inference_task(
				task_id, 
				job_path, 
				widths, 
				numxval, 
				alphabet
			)
		)

		workflow = group(tasks)
		workflow.apply_async()

	def get_result_download(self):
		return settings.MEDIA_ROOT + "/" + self.task_dir + "/" + self.task_id + ".zip"


class RckUserModel(models.Model):
	inference_task = models.ForeignKey(RckInference, on_delete=models.CASCADE)
	width = models.IntegerField()
	xval_fold = models.IntegerField(null=True)
	auc_avg = models.FloatField(null=True)
	corr_avg = models.FloatField(null=True)
	model_file = models.FileField()
	logo = models.ImageField()
	struc_pref_graph = models.ImageField()

	@classmethod
	def create(cls, width, parent_id):
		parent = RckInference.objects.get(pk=parent_id)
		task_instance = cls(width=width, inference_task=parent)
		task_instance.save()
		return task_instance


class RckModelXval(models.Model):
	rck_model = models.ForeignKey(RckUserModel, on_delete=models.CASCADE)
	fold = models.IntegerField()
	auc = models.FloatField()
	corr = models.FloatField()





class RckPrediction(models.Model):
	INPUT_CHOICES = (
		("bed", "BED Peaks"),
		("fasta", "FASTA"),
	)

	MODEL_TYPE_CHOICES = (
		("preloaded", "From Server"),
		("by_id", "By Model Task ID"),
		("upload", "User-Uploaded")

	)

	ANNOT_ALPHABET_CHOICES = (
		("PHIME", "PHIME"),
		("PU", "PU")
	)

	task_id = models.CharField(primary_key=True, unique=True, max_length=10)
	task_dir = models.CharField(max_length=100)

	model_type = models.CharField(max_length=15, choices=MODEL_TYPE_CHOICES)
	model_preloaded = models.ForeignKey(RckPreloadedRBP, on_delete=models.SET_NULL, null=True)
	model_by_id = models.ForeignKey(RckInference, on_delete=models.SET_NULL, null=True)
	# model_name = models.CharField(max_length=15)
	# model_name_preloaded = models.CharField(max_length=15)
	model_file = models.FileField(upload_to="uploads/"+str(random.randint(0, 999999999)))

	input_format = models.CharField(max_length=15, choices=INPUT_CHOICES)

	seq_file = models.FileField(upload_to="uploads/"+str(random.randint(0, 999999999)))

	genome = models.ForeignKey(Genome, on_delete=models.SET_NULL, null=True)

	generate_annotations = models.NullBooleanField(null=True)
	alphabet = models.CharField(max_length=4, choices=ANNOT_ALPHABET_CHOICES)

	annotations_file = models.FileField(upload_to="uploads/"+str(random.randint(0, 999999999)))

	width = models.IntegerField(null=True)

	complete = models.BooleanField(default=False)
	success = models.NullBooleanField(null=True)
	error_message = models.TextField()
	error_linenum = models.IntegerField(null=True)
	error_filetype = models.TextField()
	error_culprit = models.TextField()


	@classmethod
	def create(cls, post_request, files_request):
		ID_LEN = 6
		CHARS = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNPQRSTUVWXYZ123456789"
		task_id_init = "".join(random.choice(CHARS) for _ in xrange(ID_LEN))
		task_instance = cls(task_id=task_id_init, task_dir="prediction/"+task_id_init)
		FORM_MAP = {
			"model_type": task_instance.model_type,
			"model_by_id": task_instance.model_by_id,
			"model_preloaded": task_instance.model_preloaded,
			"model_file": task_instance.model_file,
			"input_format": task_instance.input_format,
			"seq_file": task_instance.seq_file,
			"genome": task_instance.genome,
			"generate_annotations": task_instance.generate_annotations,
			"alphabet": task_instance.alphabet,
			"annotations": task_instance.annotations_file,
			"min_width": task_instance.min_width,
			"max_width": task_instance.max_width,
			"max_iterations": task_instance.max_iterations,
		}
		for i in post_request:
			FORM_MAP[i] = post_request[i]
		for i in files_request:
			FORM_MAP[i] = files_request[i]
		task_instance.save()
		return task_instance

	def start_rck(self):
		from .tasks import *

		TASK_TYPE = "prediction"
		task_id = self.task_id
		media_root = settings.MEDIA_ROOT
		job_path = media_root + "/" + self.task_dir
		seq_path = job_path + "/" + task_id + "_seq"
		annotations_path = job_path + "/" + task_id + "_struc"
		input_format = self.input_format
		generate_annotations = self.generate_annotations
		alphabet = self.alphabet
		genome_path = media_root + "/" + self.genome.genome_file.name
		upload_paths_dict = {
			"fasta": media_root + "/" + self.seq_file.name,
			"bed" : media_root + "/" + self.seq_file.name
		}
		model_upload_path = media_root + "/" + self.model_file.name
		model_by_id = self.model_by_id
		model_preloaded = self.model_preloaded
		# model_name = self.model_name
		# model_name_preloaded = self.model_name_preloaded
		annotations_upload_path = media_root + "/" + self.annotations_file.name

		bedtools_path = settings.BASE_DIR+"/rck_runner/resources/bedtools2/bin/bedtools"
		bed_output_path = job_path + "/" + task_id + "_bed_sequences"
		bedtools_args_dicts = [{
			"-fi": media_root + self.seq_bed.name,
			"-fo": bed_output_path,
			"-bed": bedtools_path
		}]

		rnaplfold_path = settings.BASE_DIR+"/rck_runner/resources/RNAplfold"
		rnaplfold_args_dict = {
			"-W": "240",
			"-L": "160",
			"-u": "1",
		}

		width = self.width
		if model_type == "upload":
			with open(model_upload_path) as model, open(job_path+"/model/model_"+task_id+"_"+str(width), "w") as out:
				content = model.read()
				out.write(content)
			min_width = width
			max_width = width
		else:
			if model_type == "preloaded":
				# models = RckPreloadedModel.objects.filter(name=model_name_preloaded)
				model_files = [(m.model_file, m.width) for m in model_preloaded.rckPreloadedRBP_set.all()]
			elif model_type == "by_id":
				# models = RckUserModel.objects.filter(inference_task=model_name)
				model_files = [(m.model_file, m.width) for m in model_by_id.rckUserModel_set.all()]
			for f, w in model_files:
				f.open()
				content = f.read()
				f.close()
				with open(job_path+"/pred_"+task_id+"_"+str(w), "w") as out:
					out.write(content)
			widths = sorted(zip(*model_files)[1])
			min_width = widths[0]
			max_width = widths[-1]


		rck_path = settings.BASE_DIR+"/rck_runner/resources/RCK/bin/rnacontext"
		rck_args_dict = {
			"-a": "ACGU",
			"-e": alphabet,
			"-w": str(min_width) + "-" + str(max_width),
			"-d": job_path + "/model/" + task_id + "_sequences_dummy",
			"-n": job_path + "/model/" + task_id + "_annotations_dummy",
			"-m": job_path + "/model/" + "RCK_output",
			"-l": task_id,
			"-b": str(max_iterations)
		}

		MAX_ENTRIES = 10


		tasks = []

		if input_format == "bed":
			tasks.append(
				bed_extract_task.si(
					TASK_TYPE,
					task_id, 
					bedtools_args_dicts,
					bedtools_path,
					genome_path, 
					upload_paths_dict, 
					input_format, 
					seq_path,
					bed_output_path, 
					None
				)
			)
		else:
			tasks.append(
				verify_sequences_task.si(
					TASK_TYPE,
					task_id, 
					upload_paths_dict, 
					seq_path, 
					input_format
				)
			)

		if generate_annotations:
			tasks.append(
				create_annotations_task.si(
					TASK_TYPE,
					task_id, 
					job_path, 
					seq_path, 
					annotations_path, 
					rnaplfold_args_dict, 
					rnaplfold_path, 
					alphabet
				)
			)
		else:
			tasks.append(
				verify_annotations_task.si(
					TASK_TYPE,
					task_id, 
					seq_path,
					annotations_upload_path, 
					annotations_path, 
					alphabet
				)
			)

		tasks.append(
			RCk_prediction_task.si(
				TASK_TYPE,
				task_id, 
				job_path, 
				seq_path, 
				annotations_path, 
				rck_args_dict, 
				alphabet, 
				numxval
			)
		)

		tasks.append(
			make_prediction_task(
				task_id, 
				job_path, 
				MAX_ENTRIES
			)
		)

		workflow = group(tasks)
		workflow.apply_async()

	def get_result_download(self):
		return settings.MEDIA_ROOT + "/" + self.task_dir + "/"+ self.task_id + ".zip"
