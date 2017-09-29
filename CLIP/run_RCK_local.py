import os
import subprocess
# import time ####

def make_directory(path):
	if not os.path.isdir(path):
		os.makedirs(path)
	return path

def rck(rck_path, args_dict, nice):
	"""
	-a    <alphabet> (default ACGU)
	-e    <annotation alphabet> (default PLMU)
	-w    <motifwidth range> (default 4-10)
	-c    <training input filename>
	-d    <test input filename>
	-h    <annotation profile for training sequences>
	-n    <annotation profile for test sequences>
	-m    <output dir>
	-l    <model filename key>
	-o    <output filename key>
	-q    <sequence mode>
	-s    <number of initializations or restarts> (default 5)
	"""
	output_dir = make_directory(args_dict["-m"])
	with open(output_dir + "/" + "RCK_out.txt", "w") as out, open(output_dir + "/" + "RCK_err.txt", "w") as err:
		args = [j for i in zip(args_dict.keys(), args_dict.values()) for j in i]
		args.insert(0, rck_path)
		args[0:0] = ["nice", "-n", str(nice)]
		return subprocess.Popen(args, stdout=out, stderr=err)

def main(input_dir, rck_path, nice):
	assert nice >= -20 and nice <= 19, "Invalid nice value"
	rnaps = {i: input_dir + "/" + i for i in os.listdir(input_dir)}
	data = {i: [input_dir + "/" + i + "/" + j for j in os.listdir(rnaps[i])] for i in rnaps}
	processes = {
		j :
		rck(
			rck_path,
			{
				"-a": "ACGU",
				"-b": "200", ####
				"-e": "PHIME",
				"-w": "5-5",
				"-c": j + "/" + i + "_sequences_train.txt",
				"-d": j + "/" + i + "_sequences_test.txt",
				"-h": j + "/" + i + "_annotations_train.txt",
				"-n": j + "/" + i + "_annotations_test.txt",
				"-m": j + "/RCK_output_test_maxiter_200",
				# "-l": "",
				"-o": i,
				"-s": "3"
			},
			nice 
		) 
		for i in data
			for j in data[i]
	}
	print "\nStarting processes:\n" + "\n".join(str(i) + ": " + str(processes[i].pid) for i in processes) + "\n"

	# time.sleep(10) ####
	# for i in processes: ####
	# 	processes[i].kill() ####

if __name__ == "__main__":
	root_dir = "/home/austin/Documents/Berger_UROP/CLIP/CLIP_processed"
	rck_path = "/home/austin/Documents/Berger_UROP/RCK/bin/rnacontext"
	nice = 19
	main(root_dir, rck_path, nice)