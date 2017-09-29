from __future__ import absolute_import, unicode_literals
from rck_server.settings import BASE_DIR
import os

def read_auc(file):
	with open(file) as auc_file:
		for l in auc_file:
			if l.startswith("[1] \"aupr"):
				corr = float(l.split(" ")[-1][:-2])
				return auc

def read_corr(file):
	with open(file) as corr_file:
		for l in auc_file:
			if l.startswith("[1] \"correlation"):
				corr = float(l.split(" ")[-1][:-2])
				return corr

def get_aucs(input_dir, rck_output_name, width, numxval):
	data = [input_dir + "/" + j + "/" + rck_output_name for j in xrange(numxval)]
	return [read_auc(k + "/auc_out_" + str(width) + ".txt") for k in data]

def get_corrs(input_dir, rck_output_name, width, numxval):
	data = [input_dir + "/" + j + "/" + rck_output_name for j in xrange(numxval)]
	return [read_corr(k + "/auc_out_" + str(width) + ".txt") for k in data]

write_data(data, data_name, output_name, task_id, width, output_dir)
	out_matrix=zip(*([["CV-fold"] + range(len(data)) + ["Mean"]] + [[data_name] + data + [float(sum(data))/len(data)]]))
	out_str = "\n".join("\t".join(i) for i in out_matrix)
	with open(output_dir+"/"+output_name+task_id+"_w"+str(width)+".txt","w") as out:
		out.write(out_str)