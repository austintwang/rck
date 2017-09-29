from __future__ import absolute_import, unicode_literals
import os
from rck_runner.resources.filebundle import Filebundle

def write_files_xval(seq_lines, struc_lines, length, struc_cats, sequences_name, annotations_name, output_xval):
	for i in xrange(length):
		binding = None
		for q in xrange(2):
			ind = 2*i + q
			line = seq_lines[ind].replace("\n", "")
			if line[0] == ">":
				binding = line.split()[1]
			else:
				seq_line = line
				comb_line = str(binding) + " " + line
				output_xval.append({sequences_name: (comb_line + "\n")})
		for r in xrange(struc_cats+1):
			ind = (struc_cats+1)*i + r
			line = struc_lines[ind].replace("\n", "")
			if line[0] == ">":
				output_xval.append({annotations_name: (">" + seq_line + "\n")})
			else:
				output_xval.append({annotations_name: (line + "\n")})
		output_xval.advance_block()

def write_files(seq_lines, struc_lines, length, struc_cats, output_seq, output_struc, sequences_name, annotations_name):
	for i in xrange(length):
		binding = None
		for q in xrange(2):
			ind = 2*i + q
			line = seq_lines[ind].replace("\n", "")
			if line[0] == ">":
				binding = line.split()[1]
			else:
				seq_line = line
				comb_line = str(binding) + " " + line
				output_seq.write((comb_line + "\n"))
		for r in xrange(struc_cats+1):
			ind = (struc_cats+1)*i + r
			line = struc_lines[ind].replace("\n", "")
			if line[0] == ">":
				output_struc.write((">" + seq_line + "\n"))
			else:
				output_struc.write((line + "\n"))

def write_files_dummy_intens(seq_lines, struc_lines, length, struc_cats, output_seq, output_struc, sequences_name, annotations_name):
	for i in xrange(length):
		binding = None
		for q in xrange(2):
			ind = 2*i + q
			line = seq_lines[ind].replace("\n", "")
			if line[0] == ">":
				pass
			else:
				seq_line = line
				comb_line = "0 " + line
				output_seq.write((comb_line + "\n"))
		for r in xrange(struc_cats+1):
			ind = (struc_cats+1)*i + r
			line = struc_lines[ind].replace("\n", "")
			if line[0] == ">":
				output_struc.write((">" + seq_line + "\n"))
			else:
				output_struc.write((line + "\n"))

def input_to_rck_inference(seq_path, struc_path, name, output_dir, numxval, struc_cats)
	with open(seq_path) as seq, open(struc_path) as struc:
		seq_lines = seq.readlines()
		struc_lines = struc.readlines()

	sequences_name = name + "_sequences"
	annotations_name = name + "_annotations"

	num_sequences = len(seq_lines) / 2

	if numxval:
		os.makedirs(output_dir + "/xval/")
		output_xval = Filebundle(output_dir + "/xval", numxval, num_sequences)
		output_xval.add_files([sequences_name, annotations_name])
		write_files_xval(seq_lines, struc_lines, num_sequences, struc_cats, sequences_name, annotations_name, output_xval)
		output_xval.close_files([sequences_name, annotations_name])

	os.makedirs(output_dir + "/model/")
	with open(output_dir + "/model/" + sequences_name, "w") as output_seq:
		with open(output_dir + "/model/" + annotations_name, "w") as output_struc:
			write_files(seq_lines, struc_lines, num_sequences, struc_cats, sequences_name, annotations_name)
	with open(output_dir + "/model/" + sequences_name) as output_seq:
		with open(output_dir + "/model/" + sequences_name + "_dummy", "w") as seq_dummy:
			seq_dummy.write("".join(output_seq.readlines()[:20]))
	with open(rbp_dir + "/model/" + annotations_name) as output_struc:
		with open(rbp_dir + "/model/" + annotations_name + "_dummy", "w") as struc_dummy:
			struc_dummy.write("".join(output_struc.readlines()[:10*(struc_cats+1)]))

def input_to_rck_prediction(seq_path, struc_path, name, output_dir, numxval, struc_cats):
	with open(output_dir + sequences_name, "w") as output_seq:
		with open(seq_path) as seq, open(struc_path) as struc:
			seq_lines = seq.readlines()
			struc_lines = struc.readlines()

	sequences_name = name + "_sequences"
	annotations_name = name + "_annotations"

	num_sequences = len(seq_lines) / 2

	with open(output_dir + annotations_name, "w") as output_struc:
		write_files_dummy_intens(seq_lines, struc_lines, num_sequences, struc_cats, sequences_name, annotations_name)


# def fasta_to_rck(pos_seq_path, neg_seq_path, pos_struc_path, neg_struc_path, name, output_dir, numxval, struc_cats):
# 	with open(pos_seq_path) as pos_seq:
# 		with open(neg_seq_path) as neg_seq:
# 			with open(pos_struc_path) as pos_struc:
# 				with open(neg_struc_path) as neg_struc:
# 					pos_seq_lines = pos_seq.readlines()
# 					pos_struc_lines = pos_struc.readlines()
# 					neg_seq_lines = neg_seq.readlines()
# 					neg_struc_lines = neg_struc.readlines()
	
# 	rbp_dir = output_dir #+ "/" + name
# 	sequences_name = name + "_sequences"
# 	annotations_name = name + "_annotations"

# 	pos_seq_len = len(pos_seq_lines)
# 	neg_seq_len = len(neg_seq_lines)

# 	print len(pos_seq_lines), len(neg_seq_lines), len(pos_struc_lines), len(neg_struc_lines) ####

# 	num_sequences = (pos_seq_len + neg_seq_len) / 2

# 	if numxval:
# 		os.makedirs(rbp_dir + "/xval/")
# 		# with open(rbp_dir + "/xval/" + sequences_name, "w") as output_seq:
# 		# 	with open(rbp_dir + "/xval/" + annotations_name, "w") as output_struc:
# 		output_xval = Filebundle(rbp_dir + "/xval", numxval, num_sequences)
# 		output_xval.add_files([sequences_name, annotations_name])

# 		write_files_xval(pos_seq_lines, pos_struc_lines, 1, pos_seq_len / 2, struc_cats, sequences_name, annotations_name, output_xval)
# 		write_files_xval(neg_seq_lines, neg_struc_lines, 0, neg_seq_len / 2, struc_cats, sequences_name, annotations_name, output_xval)

# 		output_xval.close_files([sequences_name, annotations_name])
# 		# print "iwhoeifhowe" ####
# 		# print output_xval.provision_directories ####

# 	os.makedirs(rbp_dir + "/model/")
# 	with open(rbp_dir + "/model/" + sequences_name, "w") as output_seq:
# 		with open(rbp_dir + "/model/" + annotations_name, "w") as output_struc:
# 			write_files(pos_seq_lines, pos_struc_lines, 1, pos_seq_len / 2, struc_cats, output_seq, output_struc, sequences_name, annotations_name)
# 			write_files(neg_seq_lines, neg_struc_lines, 0, neg_seq_len / 2, struc_cats, output_seq, output_struc, sequences_name, annotations_name)
# 	with open(rbp_dir + "/model/" + sequences_name) as output_seq:
# 		with open(rbp_dir + "/model/" + sequences_name + "_dummy", "w") as seq_dummy:
# 			seq_dummy.write("".join(output_seq.readlines()[:20]))
# 	with open(rbp_dir + "/model/" + annotations_name) as output_struc:
# 		with open(rbp_dir + "/model/" + annotations_name + "_dummy", "w") as struc_dummy:
# 			struc_dummy.write("".join(output_struc.readlines()[:10*(struc_cats+1)]))