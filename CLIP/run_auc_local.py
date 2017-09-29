import os
import subprocess
# import time ####

def make_directory(path):
	if not os.path.isdir(path):
		os.makedirs(path)
	return path

def auc(auc_path, data_path, rnap_name, nice):
	with open(data_path + "/" + "auc_out.txt", "w") as out, open(data_path + "/" + "auc_err.txt", "w") as err:
		args = ["nice", "-n", str(nice), "Rscript", auc_path, data_path + "/test_" + rnap_name + "_5.txt"]
		return subprocess.Popen(args, stdout=out, stderr=err)

def main(input_dir, auc_path, nice):
	assert nice >= -20 and nice <= 19, "Invalid nice value"
	rnaps = {i: input_dir + "/" + i for i in os.listdir(input_dir)}
	data = {i: [input_dir + "/" + i + "/" + j + "/RCK_output" for j in os.listdir(rnaps[i])] for i in rnaps}
	processes = {j: auc(auc_path, j, i, nice) for i in data for j in data[i]}
	print "\nStarting processes:\n" + "\n".join(str(i) + ": " + str(processes[i].pid) for i in processes) + "\n"

	# time.sleep(10) ####
	# for i in processes: ####
	# 	processes[i].kill() ####

if __name__ == "__main__":
	root_dir = "/home/austin/Documents/Berger_UROP/CLIP/CLIP_processed"
	auc_path = "/home/austin/Documents/Berger_UROP/CLIP/calc_auc.R"
	nice = 19
	main(root_dir, auc_path, nice)