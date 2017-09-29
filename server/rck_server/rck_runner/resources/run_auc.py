
from __future__ import absolute_import, unicode_literals
import subprocess
from rck_server.settings import BASE_DIR
import os
import subprocess
# import time ####

def make_directory(path):
	if not os.path.isdir(path):
		os.makedirs(path)
	return path

def auc(auc_path, data_path, rnap_name, width):
	with open(data_path + "/" + "auc_out_" + str(width) + ".txt", "w") as out, open(data_path + "/" + "auc_err_" + str(width) + ".txt", "w") as err:
		args = ["Rscript", auc_path, data_path + "/test_" + rnap_name + "_" + str(width) + ".txt"]
		# print args ####
		return subprocess.Popen(args, stdout=out, stderr=err)

def auc_all(input_dir, widths, id, auc_path=BASE_DIR+"/rck_runner/resources/calc_auc.R"):
	data = [input_dir + "/" + j + "/RCK_output" for j in os.listdir(input_dir)]
	processes = [auc(auc_path, j, id, k) for j in data for k in widths]
	for p in processes:
		p.wait()
	
def auc_single(input_dir, widths, id, auc_path=BASE_DIR+"/rck_runner/resources/calc_auc.R"):
	processes = [auc(auc_path, input_dir, id, k) for k in widths]
	for p in processes:
		p.wait()

