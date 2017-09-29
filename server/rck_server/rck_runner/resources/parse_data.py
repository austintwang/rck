import os
import random
import multiprocessing

class Filterable:

	def __init__(self, input_dir):
		self.files = os.listdir(input_dir)
		self.file_dict = {}

	def has_keyword(self, name, keywords, antikeywords):
		hit = True
		for i in keywords:
			if i not in name:
				hit = False
		for i in antikeywords:
			if i in name:
				hit = False
		return hit

	def filter_all(self, keywords, antikeywords):
		for b in xrange(len(self.files) - 1, -1, -1):
			if not self.has_keyword(self.files[b], keywords, antikeywords):
				del self.files[b]

	def build_dict(self):
		for i in self.files:
			rnap_name = i.partition(".")[0]
			self.file_dict.setdefault(rnap_name, {}).setdefault("Misc", []).append(i)

	def filter_to_cat(self, category, keywords, antikeywords):
		for k, v in self.file_dict.iteritems():
			for i in v["Misc"]:
				if self.has_keyword(i, keywords, antikeywords):
					self.file_dict[k][category] = i

	def clean_dict(self, required_cats):
		marked_del = []
		for k in self.file_dict:
			unfilled = any(len(self.file_dict[k].get(i, {})) == 0 for i in required_cats)
			if unfilled:
				marked_del.append(k)
		for i in marked_del:
			del self.file_dict[i]
		for k in self.file_dict:
			del self.file_dict[k]["Misc"]

	def return_dict(self):
		return self.file_dict
	


class Filebundle:

	def __init__(self, output_dir, provision_number, length):
		if not os.path.isdir(output_dir):
			os.makedirs(output_dir)
		provision_directories_ind = xrange(provision_number)
		self.provision_directories = {}
		provisions = [i for i in provision_directories_ind]
		for i in provisions:
			provision_directory_name = output_dir + "/" + str(i)
			file_directory = {}
			# file_directory["train"] = [self.make_directory(provision_directory_name + "/train"), {}]
			# file_directory["test"] = [self.make_directory(provision_directory_name + "/test"), {}]
			file_directory["train"] = [self.make_directory(provision_directory_name) , {}]
			file_directory["test"] = [self.make_directory(provision_directory_name) , {}]
			self.provision_directories[i] = file_directory
		self.provisions_left = length
		self.tallies = [-(-length // provision_number) for i in provision_directories_ind]
		self.selected_block = None

	def make_directory(self, path):
		if not os.path.isdir(path):
			os.makedirs(path)
		return path

	def select_wo_replacement(self):
		selected_block = None
		total = sum( i for i in self.tallies )
		cumu = 0
		num = random.uniform(0, total)
		for x in xrange(len(self.tallies)):
			cumu += self.tallies[x]
			if num <= cumu:
				self.tallies[x] -= 1
				self.provisions_left -= 1
				selected_block = x
				break
		return selected_block 

	def add_files(self, filenames):
		for k in self.provision_directories:
			for i in filenames:
				self.provision_directories[k]["test"][1][i] = open(self.provision_directories[k]["test"][0] + "/" + i + "_test.txt", "a")
			for i in filenames:
				self.provision_directories[k]["train"][1][i] = open(self.provision_directories[k]["train"][0] + "/" + i + "_train.txt", "a")
	def advance_block(self):
		self.selected_block = self.select_wo_replacement()

	def append_line(self, linedict):
		"""
		linedict: {filename, line}
		"""
		for y in self.provision_directories:
			if y == self.selected_block:
				for k , v in linedict.iteritems():
					self.provision_directories[y]["test"][1][k].write(v)
			else:
				for k , v in linedict.iteritems():
					self.provision_directories[y]["train"][1][k].write(v)

	def close_files(self, filenames):
		for y in self.provision_directories:
			for i in filenames:
				self.provision_directories[y]["test"][1][i].close()
				self.provision_directories[y]["train"][1][i].close()



def merge_score_sequence(score, seq):
	return (str(score) + "\t" + seq)

def write_file(input):
	name = input[0]
	cat_dict = input[1]
	input_dir = input[2]
	output_dir = input[3]
	provision_number = input[4]

	filestr = "Files for " + name + ":\n" + str(cat_dict) + "\n"
	print filestr

	with open(input_dir + "/" + cat_dict["pos_seq"]) as pos_seq:
		with open(input_dir + "/" + cat_dict["neg_seq"]) as neg_seq:
			with open(input_dir + "/" + cat_dict["pos_struc"]) as pos_struc:
				with open(input_dir + "/" + cat_dict["neg_struc"]) as neg_struc:
					print "Reading Input Files for " + name + "\n"
					pos_seq_lines = pos_seq.readlines()
					pos_struc_lines = pos_struc.readlines()
					neg_seq_lines = neg_seq.readlines()
					neg_struc_lines = neg_struc.readlines()
					print "Done Reading Input Files for " + name + "\n"
	
	rbp_dir = output_dir + "/" + name
	sequences_name = name + "_sequences"
	annotations_name = name + "_annotations"

	pos_seq_len = len(pos_seq_lines)
	pos_struc_len = len(pos_struc_lines)
	neg_seq_len = len(neg_seq_lines)
	neg_struc_len = len(neg_struc_lines)

	aligned = pos_seq_len * 3 == pos_struc_len and neg_seq_len * 3 == neg_struc_len
	if not aligned:
		print \
			"### SKIPPING " + name + " ###\n" + \
			"Number of sequences don't match" + "\n" + \
			"Sequences in positive sequence file: " + str(pos_seq_len / 2) + "\n" + \
			"Sequences in positive structure file: " + str(pos_struc_len / 6) + "\n" + \
			"Sequences in negative sequence file: " + str(neg_seq_len / 2) + "\n" + \
			"Sequences in negative structure file: " + str(neg_struc_len / 6) + "\n"
		return
	else:
		print \
		"For " + name + ":\n" + \
		"Sequences in positive sequence file: " + str(pos_seq_len / 2) + "\n" + \
		"Sequences in positive structure file: " + str(pos_struc_len / 6) + "\n" + \
		"Sequences in negative sequence file: " + str(neg_seq_len / 2) + "\n" + \
		"Sequences in negative structure file: " + str(neg_struc_len / 6) + "\n"

	num_sequences = (pos_seq_len + neg_seq_len) / 2

	print "Creating Output Files for " + name + "\n"
	output = Filebundle(rbp_dir, provision_number, num_sequences)
	output.add_files([sequences_name, annotations_name])

	print "Writing to Output for " + name + "\n"
	for i in xrange(pos_seq_len / 2):
		seq_line = ""
		for q in xrange(2):
			ind = 2*i + q
			line = pos_seq_lines[ind]
			is_seq = line[0] == ">" or line[0] == "A" or line[0] == "C" or line[0] == "G" or line[0] == "U" or line[0] == "T"
			assert is_seq, "\nNot Sequence Data:\n" + str(line)
			if line[0] == ">":
				continue
			else:
				line = line.replace("T", "U")
				seq_line = line
				comb_line = merge_score_sequence(1, line)
				output.append_line({sequences_name: comb_line})
		for r in xrange(6):
			
			ind = 6*i + r
			line = pos_struc_lines[ind]
			if line[0] == ">":
				output.append_line({annotations_name: (">" + seq_line)})
			else:
				output.append_line({annotations_name: line})
		output.advance_block()

	for j in xrange(neg_seq_len / 2):
		seq_line = ""
		for q in xrange(2):
			ind = 2*j + q
			line = neg_seq_lines[ind]
			is_seq = line[0] == ">" or line[0] == "A" or line[0] == "C" or line[0] == "G" or line[0] == "U" or line[0] == "T"
			assert is_seq, "\nNot RNA Sequence Data:\n" + str(line)
			if line[0] == ">":
				continue
			else:
				line = line.replace("T", "U")
				seq_line = line
				comb_line = merge_score_sequence(0, line)
				output.append_line({sequences_name: comb_line})
		for r in xrange(6):
			ind = 6*j + r
			line = neg_struc_lines[ind]
			if line[0] == ">":
				output.append_line({annotations_name: (">" + seq_line)})
			else:
				output.append_line({annotations_name: line})
		output.advance_block()

	print "Done Writing output for " + name + "\n"

	output.close_files([sequences_name, annotations_name])

	print "All Done for " + name + "\n"

def write_all_files(file_dict, input_dir, output_dir, provision_number, processes):
	inputs = [[name, cat_dict, input_dir, output_dir, provision_number] for name, cat_dict in file_dict.iteritems()]
	workers = multiprocessing.Pool(processes)
	workers.map(write_file, inputs)
	print "Finished"

def main(input_dir, output_dir, provision_number, processes):
	if os.path.isdir(output_dir):
		print "Output Directory Already Exists"
	else:
		keywords = ["train", "fa"]
		antikeywords = [".ls", ".all", ".zip", ".gz", ".class", "onlyseq", "verbose", "feature", ".dist", "txt.r1.txt", "txt.train.fa", "cv_results"]
		pqkeywords = ["positives", "upper"]
		pqantikeywords = ["negatives", "filtered_profile"]
		prkeywords = ["positives", "filtered_profile"]
		prantikeywords = ["negatives", "upper"]
		nqkeywords = ["negatives", "upper"]
		nqantikeywords = ["positives", "filtered_profile"]
		nrkeywords = ["negatives", "filtered_profile"]
		nrantikeywords = ["positives", "upper"]

		filter_dir = Filterable(input_dir)
		filter_dir.filter_all(keywords, antikeywords)
		filter_dir.build_dict()
		filter_dir.filter_to_cat("pos_seq", pqkeywords, pqantikeywords)
		filter_dir.filter_to_cat("neg_seq", nqkeywords, nqantikeywords)
		filter_dir.filter_to_cat("pos_struc", prkeywords, prantikeywords)
		filter_dir.filter_to_cat("neg_struc", nrkeywords, nrantikeywords)
		filter_dir.clean_dict(["pos_seq", "neg_seq", "pos_struc", "neg_struc"])
		file_dict = filter_dir.return_dict()
		write_all_files(file_dict, input_dir, output_dir, provision_number, processes)

if __name__ == "__main__":
	#input_dir = os.getcwd()
	input_dir = "/data/cb/yaronore/sequences/GraphProt_CLIP_sequences"
	output_dir = "/data/cb/austintwang/CLIP/RCK_CLIP_x2"
	provision_number = 2
	processes = multiprocessing.cpu_count()
	main(input_dir, output_dir, provision_number, processes)
