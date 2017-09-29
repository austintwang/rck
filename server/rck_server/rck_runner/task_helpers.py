from __future__ import absolute_import, unicode_literals
from .models import RckUserModel, RckModelXval, RckPreloadedModel, RckPredictionResult, RckPredictionSingle
import sys
import os
from resources import *


def bed_setup_helper(task_id, genome, input_path, input_format, output_bed_path, output_control_path):
	parse_bed.verify_bed(input_path, output_path)
	if input_format == "pos_neg":
		parse_bed.make_control(output_path, output_control_path)


def run_bedtools_helper(args_dict, bedtools_path):
	parse_bed.run_bedtools_getfasta(args_dict, bedtools_path)


def bed_postprocess_helper(task_id, input_format, upload_paths_dict, bed_seq_path, bed_control_path, output_path):
	if input_format == "bed":
		if bed_control_path:
			parse_input.parse_pos_neg_input(bed_seq_path, bed_control_path, output_path)
		else:
			parse_input.parse_fasta(bed_seq_path, output_path)
	elif input_format == "seq_intens_bed":
		parse_input.parse_seq_intens_input(bed_seq_path, upload_paths_dict["intens"], output_path)


def verify_sequences_helper(task_id, upload_paths_dict, output_path, input_format):
	if input_format == "pos_neg":
		parse_input.parse_pos_neg_input(upload_paths_dict["pos_seq"], upload_paths_dict["neg_seq"], output_path)
	elif input_format == "seq_intens_fasta":
		parse_input.parse_seq_intens_input(upload_paths_dict["seq_fasta"], upload_paths_dict["intens"], output_path)
	elif input_format == "rck":
		parse_input.parse_rck_format_input(upload_paths_dict["rck"], output_path)
	elif input_path == "fasta":
		parse_input.parse_fasta(upload_paths_dict["fasta"], output_path)


def rnaplfold_setup_helper(seq_path):
	with open(seq_path) as infile, open(seq_path+"_stripped", "w") as outfile:
		outfile.write("\n".join(i for i in infile.read().splitlines() if i[0] != ">"))


def run_rnaplfold_helper(args_dict, input_path, output_path, motif, rnaplfold_path):
	run_rnaplfold.rnaplfold(args_dict, input_path, output_path, motif, rnaplfold_path)


def create_profiles_helper(job_path, name, struc_output_path, alphabet):
	Epath = job_path + "/" + name + "_Eprof"
	Hpath = job_path + "/" + name + "_Hprof"
	Ipath = job_path + "/" + name + "_Iprof"
	Mpath = job_path + "/" + name + "_Mprof"
	if alphabet == "PHIME":
		create_profiles.merge_profiles_PHIME(Epath, Hpath, Ipath, Mpath, struc_output_path)
	elif alphabet == "PU":
		create_profiles.merge_profiles_PU(Epath, Hpath, Ipath, Mpath, struc_output_path)


def verify_annotations_helper(task_id, seq_path, annotations_path, output_path, alphabet):
	verify_annotations.verify_annotations(task_id, seq_path, annotations_path, output_path, alphabet)


def rck_inference_setup_helper(job_path, seq_path, annotations_path, numxval, task_id, alphabet):
	rck_setup.input_to_rck_inference(seq_path, annotations_path, task_id, job_path, numxval, len(alphabet))


def run_rck_helper(args_dict, rck_path):
	run_RCK.rck(args_dict, rck_path)


def make_inference_helper(job_path, widths, numxval, struc_alphabet, task_id):
	xval_dir = job_path + "/xval"
	model_dir = job_path + "/model"
	
	for w in widths:
		str_w = str(w)
		results_path = job_path + "/results/width_" + str_w
		os.makedirs(results_path)

		prefs = get_pwms_prefs.get_pwms_prefs(model_dir+"/pwm_"+task_id+"_"+str_w+".txt")
		pwm = get_pwms_prefs.get_matrix_pwm(prefs)

		make_logo.make_logo(pwm, task_id, w, results_path)
		graph_prefs.graph_prefs(prefs, struc_alphabet,task_id, w, results_path)

		aucs = get_stats.get_aucs(results_path, "RCK_output", w, numxval)
		corrs = get_stats.get_corrs(results_path, "RCK_output", w, numxval)

		get_stats.write_data(aucs, "AUROC", "AUROC", task_id, w, results_path)
		get_stats.write_data(aucs, "Pearson Correlation", "correlation", task_id, w, results_path)

		rck_model = RckUserModel.create(width=w, xval_fold=numxval, parent_id=task_id)
		rck_model.xval_fold = numxval
		rck_model.auc_avg = float(sum(aucs)) / numxval
		rck_model.corr_avg = float(sum(corrs)) / numxval

		rck_model.model_file.name = model_dir+"/model_"+task_id+"_"+str_w+".txt"
		rck_model.logo.name = model_dir+"/logo"+task_id+"_w"+str_w+".svg"
		rck_model.struc_pref_graph.name = model_dir+"/struc_prefs"+task_id+"_w"+str_w+".svg"
		# with open(model_dir+"/model_"+task_id+"_"+str_w+".txt") as model_file:
		# 	rck_model.model_file.save("user_models/"+task_id+"_"+str_w, File(model_file))
		# with open(model_dir+"/logo"+task_id+"_w"+str_w+".svg") as logo:
		# 	rck_model.logo.save("model_logos/"+task_id+"_"+str_w+".svg", logo)
		# with open(model_dir+"/struc_prefs"+task_id+"_w"+str_w+".svg") as struc_prefs:
		# 	rck_model.struc_pref_graph.save("model_struc_graphs/"+task_id+"_"+str_w+".svg", struc_prefs)
		rck_model.save()

		for x in range(len(numxval)):
			auc = aucs[x]
			corr = corrs[x]
			rck_model_xval = RckModelXval(rck_model=rck_model, fold=x, auc=auc, corr=corr)
			rck_model_xval.save()

	with zipfile.ZipFile(job_path + "/"+ task_id + ".zip", 'w') as output:
		for root, dirs, files in os.walk(job_path + "/results"):
			for file in files:
				output.write(os.path.join(root, file))


def load_model(model_name, model_type, job_path, task_id):
	if model_type == "preloaded":
		models = RckPreloadedModel.objects.filter(name=model_name)
		model_files = [(m.model_file, m.width) for m in models]
	elif model_type == "by_id":
		models = RckUserModel.objects.filter(name=model_name)
		model_files = [(m.model_file, m.width) for m in models]
	for f, w in model_files:
		f.open()
		content = f.read()
		f.close()
		with open(job_path+"/pred_"+task_id+"_"+str(w), "w") as out:
			out.write(content)

	
def load_model_uploaded(model_path, width, job_path, task_id):
	with open(model_path) as model, open(job_path+"/model/model_"+task_id+"_"+str(w), "w") as out:
		content = model.read()
		out.write(content)


def rck_prediction_setup_helper(job_path, seq_path, annotations_path, task_id, alphabet):
	rck_setup.input_to_rck_prediction(seq_path, annotations_path, task_id, job_path, numxval, len(alphabet))


def make_prediction_helper(job_path, max_entries, task_id):
	result_dir = job_path + "/model"
	output_dir = job_path + "/output"
	results = [i for i in os.listdir(result_dir) if i.startswith("pred_")]
	for r in results:
		width = int("_".split(".".split(r)[0])[-1])
		seq_path = job_path + "/" + task_id + "_sequences"
		result_path = result_dir + "/" + r
		output_path = output_dir + "/" + r
		with open(result_path) as raw_result:
			result_lines = raw_result.readlines()
		results = [i.strip().split()[1] for i in result_lines]
		num_results = [float(i) for i in results]
		with open(output_path, "w") as output:
			output.write("\n".join(results))
		with open(seq_path) as seq_file:
			seqs = [i[1] for i in seq_file.readlines.strip().split()]
		results_with_seqs = zip(results, seqs)
		with open(output_path+"_with_seqs", "w") as output_with_seqs:
			output_with_seqs.write("\n".join("\t".join(i) for i in results_with_seqs))

		num_results_with_seqs = sorted(zip(num_results, seqs), reverse=True)[:max_entries-1]
		result_model = RckPredictionResult(width=width)
		result_model.save()
		for score, seq in num_results_with_seqs:
			result_single = RckPredictionSingle(prediction_result=result_model, sequence=seq, score=score)
			result_single.save()

		with zipfile.ZipFile(job_path + "/"+ task_id + ".zip", 'w') as output:
			for root, dirs, files in os.walk(result_dir):
				for file in files:
					output.write(os.path.join(root, file))




			