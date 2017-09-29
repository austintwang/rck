
from __future__ import absolute_import, unicode_literals
import subprocess
from rck_server.settings import BASE_DIR
import os

def get_auc(file):
	with open(file) as auc_file:
		# print file ####
		# print auc_file ####
		# print auc_file.tell() ####
		# print len(auc_file.read()) ####
		# print auc_file.read() ####
		# print "owiehfoiwehfo" ####
		for l in auc_file:
			# print l ####
			if l.startswith("[1] \"aupr"):
				auc = float(l.split(" ")[-1][:-2])
				assert type(auc) == float
				# print auc ####
				return auc

def write_dict(auc_dict, output_dir, csv_name, widths):
	auc_list = [(i, auc_dict[i]) for i in sorted(auc_dict.keys())]
	with open(output_dir + "/" + csv_name, "w") as aucs:
		aucs.write("Experiment," + ",".join("w=" + str(i) for i in widths) + "\n")
		# print auc_list ####
		for i in auc_list:
			print i ####
			line = i[0] + "," + ",".join(str(j) for j in i[1]) + "\n"
			aucs.write(line)
			print line

def get_auc_avg(input_dir, output_dir, output_name, csv_name, widths, task_id):
	data = [input_dir + "/" + j + "/" + output_name for j in os.listdir(input_dir)]
	# print data ####
	print [[get_auc(k + "/auc_out_" + str(j) + ".txt") for k in data] for j in widths] ####
	auc_dict = {task_id: [sum(get_auc(k + "/auc_out_" + str(j) + ".txt") for k in data) / len(data) for j in widths]}
	write_dict(auc_dict, output_dir, csv_name, widths)
	
def get_auc_single(input_dir, output_dir, output_name, csv_name, widths, task_id):
	data = [input_dir + "/" + j + "/" + output_name for j in os.listdir(input_dir)]
	auc_dict = {task_id: [get_auc(input_dir + "/auc_out_" + str(j) + ".txt") for j in widths]}
	write_dict(auc_dict, output_dir, csv_name, widths)


# if __name__ == "__main__":
# 	root_dir = "/data/cb/austintwang/CLIP/RCK_CLIP_x10"
# 	output_dir = "/data/cb/austintwang/CLIP"
# 	output_name = "RCK_output_k3-7_b200"
# 	csv_name = "auc_k3-7_b200.csv"
# 	widths = xrange(3, 8)
# 	main(root_dir, output_dir, output_name, csv_name, widths)
