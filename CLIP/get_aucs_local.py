import os

def get_auc(file):
	with open(file) as auc_file:
		for l in auc_file:
			if l.startswith("[1] \"aupr"):
				return float(l.split(" ")[-1][:-2])

def write_dict(auc_dict, output_dir):
	with open(output_dir + "/auc.csv", "a") as aucs:
		for i in auc_dict:
			aucs.write(i + "," + str(auc_dict[i]))

def main(input_dir, output_dir):
	rnaps = {i: input_dir + "/" + i for i in os.listdir(input_dir)}
	data = {i: [input_dir + "/" + i + "/" + j + "/RCK_output/auc_out.txt" for j in os.listdir(rnaps[i])] for i in rnaps}
	auc_dict = {i: sum(get_auc(j) for j in data[i]) / len(data[i]) for i in data}
	write_dict(auc_dict, output_dir)

if __name__ == "__main__":
	root_dir = "/home/austin/Documents/Berger_UROP/CLIP/CLIP_processed"
	output_dir = "/home/austin/Documents/Berger_UROP/CLIP"
	main(root_dir, output_dir)