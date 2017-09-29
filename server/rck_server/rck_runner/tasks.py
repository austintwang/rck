from __future__ import absolute_import, unicode_literals
from celery import shared_task, states
from celery.exceptions import Ignore
from .signals import inference_status, prediction_status
import sys
from multiprocessing import Process, current_process
sys.path.append(os.path.dirname(os.path.abspath(__file__))) 
from task_helpers import *
# from celery.utils.log import get_task_logger

# logger = get_task_logger(__name__)

@shared_task(bind=True)
def bed_extract_task(self, task_type, task_id, bedtools_args_dicts, bedtools_path, genome, upload_paths_dict, input_format, seq_output_path, bed_output_path, output_control_path=None):
	current_process().daemon = False
	current_process()._authkey = current_process().authkey
	current_process()._daemonic = current_process().daemon
	current_process()._tempdir = current_process()._config.get('tempdir')
	if task_type == "inference":
		status = inference_status
	elif task_type == "prediction":
		status = prediction_status
	else:
		raise ValueError

	try:
		bed_setup_helper(task_id, genome, upload_paths_dict["bed"], input_format, bed_output_path, output_control_path):
	except ValueError, e:
		if len(e.args) == 5:
			status.send(
				sender=self.__name__,
				id=task_id, 
				success=False, 
				message=e.args[0], 
				linenum=e.args[1], 
				filetype=e.args[2], 
				culprit=e.args[3]
			)
		else:
			status.send(
				sender=self.__name__, 
				id=task_id, 
				success=False,
				message="Error with input BED files"
			)
			self.update_state(
				state = states.FAILURE,
			)
			raise Ignore()
	except Exception:
		status.send(
			sender=self.__name__, 
			id=task_id, 
			success=False,
			message="Error with input BED files"
		)
		self.update_state(
			state = states.FAILURE,
		)
		raise Ignore()

	bedtools_jobs = [
		Process(target=run_bedtools_helper, args=(i, bedtools_path))
		for i in bedtools_args_dicts
	]
	for j in bedtools_jobs: j.start()
	for j in bedtools_jobs: j.join()
	for j in bedtools_jobs:
		try:
			j.get()
		except Exception:
			status.send(
				sender=self.__name__, 
				id=task_id, 
				success=False,
				message="Error extracting BED peaks"
			)
			self.update_state(
				state = states.FAILURE,
			)
			raise Ignore()

	try:
		bed_postprocess_helper(task_id, input_format, upload_paths_dict, bed_output_path, output_control_path, seq_output_path)
	except Exception:
		status.send(
			sender=self.__name__, 
			id=task_id, 
			success=False,
			message="Error extracting BED peaks"
		)
		self.update_state(
			state = states.FAILURE,
		)
		raise Ignore()



@shared_task(bind=True)
def verify_sequences_task(self, task_type, task_id, upload_paths_dict, seq_output_path, input_format):
	current_process().daemon = False
	current_process()._authkey = current_process().authkey
	current_process()._daemonic = current_process().daemon
	current_process()._tempdir = current_process()._config.get('tempdir')
	if task_type == "inference":
		status = inference_status
	elif task_type == "prediction":
		status = prediction_status
	else:
		raise ValueError

	try:
		verify_sequences_helper(task_id, upload_paths_dict, seq_output_path, input_format)
	except ValueError, e:
		if len(e.args) == 5:
			status.send(
				sender=self.__name__,
				id=task_id, 
				success=False, 
				message=e.args[0], 
				linenum=e.args[1], 
				filetype=e.args[2], 
				culprit=e.args[3]
			)
		else:
			status.send(
				sender=self.__name__, 
				id=task_id, 
				success=False,
				message="Error with input files"
			)
			self.update_state(
				state = states.FAILURE,
			)
			raise Ignore()
	except Exception:
		status.send(
			sender=self.__name__, 
			id=task_id, 
			success=False,
			message="Error with input files"
		)
		self.update_state(
			state = states.FAILURE,
		)
		raise Ignore()


@shared_task(bind=True)
def create_annotations_task(self, task_type, task_id, job_path, seq_path, annotations_output_path, rnaplfold_args_dict, rnaplfold_path, alphabet):
	current_process().daemon = False
	current_process()._authkey = current_process().authkey
	current_process()._daemonic = current_process().daemon
	current_process()._tempdir = current_process()._config.get('tempdir')
	if task_type == "inference":
		status = inference_status
	elif task_type == "prediction":
		status = prediction_status
	else:
		raise ValueError

	try:
		rnaplfold_setup_helper(seq_path)
	except Exception:
		status.send(
			sender=self.__name__, 
			id=task_id, 
			success=False,
			message="Error creating structural annotations"
		)


	rnaplfold_jobs = [
		Process(target=run_rnaplfold_helper, args=(rnaplfold_args_dict, seq_path+"_stripped", job_path + "/" + task_id + "_Eprof", "E", rnaplfold_path)),
		Process(target=run_rnaplfold_helper, args=(rnaplfold_args_dict, seq_path+"_stripped", job_path + "/" + task_id + "_Hprof", "H", rnaplfold_path)),
		Process(target=run_rnaplfold_helper, args=(rnaplfold_args_dict, seq_path+"_stripped", job_path + "/" + task_id + "_Iprof", "I", rnaplfold_path)),
		Process(target=run_rnaplfold_helper, args=(rnaplfold_args_dict, seq_path+"_stripped", job_path + "/" + task_id + "_Iprof", "M", rnaplfold_path))  
	]
	for j in rnaplfold_jobs: j.start()
	for j in rnaplfold_jobs: j.join()
	for j in rnaplfold_jobs:
		try:
			j.get()
		except Exception:
			status.send(
				sender=self.__name__, 
				id=task_id, 
				success=False,
				message="Error creating structural annotations"
			)
			self.update_state(
				state = states.FAILURE,
			)
			raise Ignore()

	try:
		create_profiles_helper(job_path, task_id, annotations_output_path, alphabet)
	except Exception:
			inference_status.send(
				sender=self.__name__, 
				id=task_id, 
				success=False,
				message="Error creating structural annotations"
			)
			self.update_state(
				state = states.FAILURE,
			)
			raise Ignore()


@shared_task(bind=True)
def verify_annotations_task(self, task_type, task_id, seq_path, annotations_upload_path, annotations_output_path, alphabet):
	current_process().daemon = False
	current_process()._authkey = current_process().authkey
	current_process()._daemonic = current_process().daemon
	current_process()._tempdir = current_process()._config.get('tempdir')
	if task_type == "inference":
		status = inference_status
	elif task_type == "prediction":
		status = prediction_status
	else:
		raise ValueError

	try:
		verify_annotations_helper(task_id, seq_path, annotations_upload_path, annotations_output_path, alphabet)
	except ValueError, e:
		if len(e.args) == 5:
			status.send(
				sender=self.__name__, 
				id=task_id, 
				success=False, 
				message=e.args[0], 
				linenum=e.args[1], 
				filetype=e.args[2], 
				culprit=e.args[3]
			)
		else:
			status.send(
				sender=self.__name__, 
				id=task_id, 
				success=False,
				message="Unknown Error"
			)
			self.update_state(
				state = states.FAILURE,
			)
			raise Ignore()


@shared_task(bind=True)
def create_RCK_model_task(self, task_type, task_id, job_path, seq_path, annotations_path, rck_args_dicts, alphabet, numxval):
	current_process().daemon = False
	current_process()._authkey = current_process().authkey
	current_process()._daemonic = current_process().daemon
	current_process()._tempdir = current_process()._config.get('tempdir')
	if task_type == "inference":
		status = inference_status
	elif task_type == "prediction":
		status = prediction_status
	else:
		raise ValueError

	try:
		rck_inference_setup_helper(job_path, seq_path, annotations_path, numxval, task_id, alphabet)
	except Exception:
		status.send(
			sender=self.__name__, 
			id=task_id, 
			success=False,
			message="Error running RCK"
		)
		self.update_state(
			state = states.FAILURE,
		)
		raise Ignore()

	rck_jobs = [
		Process(target=run_rck_helper, args=(i, rck_path))
		for i in rck_args_dicts
	]
	for j in rck_jobs: j.start()
	for j in rck_jobs: j.join()
	for j in rck_jobs:
		try:
			j.get()
		except Exception:
			status.send(
				sender=self.__name__, 
				id=task_id, 
				success=False,
				message="Error running RCK"
			)
			self.update_state(
				state = states.FAILURE,
			)
			raise Ignore()

@shared_task(bind=True)
def RCK_prediction_task(self, task_type, task_id, job_path, seq_path, annotations_path, rck_args_dict, alphabet):
	current_process().daemon = False
	current_process()._authkey = current_process().authkey
	current_process()._daemonic = current_process().daemon
	current_process()._tempdir = current_process()._config.get('tempdir')
	if task_type == "inference":
		status = inference_status
	elif task_type == "prediction":
		status = prediction_status
	else:
		raise ValueError

	try:
		rck_prediction_setup_helper(job_path, seq_path, annotations_path, task_id, alphabet)
	except Exception:
		status.send(
			sender=self.__name__, 
			id=task_id, 
			success=False,
			message="Error running RCK"
		)
		self.update_state(
			state = states.FAILURE,
		)
		raise Ignore()




@shared_task(bind=True)
def make_inference_task(self, task_id, job_path, widths, numxval, alphabet):
	current_process().daemon = False
	current_process()._authkey = current_process().authkey
	current_process()._daemonic = current_process().daemon
	current_process()._tempdir = current_process()._config.get('tempdir')

	try:
		make_inference_helper(job_path, widths, numxval, alphabet, task_id)
	except Exception:
		inference_status.send(
			sender=self.__name__,
			id=task_id,  
			success=False,
			message="Error generating output"
		)
		self.update_state(
			state = states.FAILURE,
		)
		raise Ignore()

	inference_status.send(sender=self.__name__, success=True)


@shared_task(bind=True)
def make_prediction_task(self, task_id, job_path, max_entries):
	try:
		make_prediction_helper(job_path, max_entries, task_id)
	except Exception:
		prediction_status.send(
			sender=self.__name__,
			id=task_id,  
			success=False,
			message="Error generating output"
		)
		self.update_state(
			state = states.FAILURE,
		)
		raise Ignore()

	prediction_status.send(sender=self.__name__, success=True)


