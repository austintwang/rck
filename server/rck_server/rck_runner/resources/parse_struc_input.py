from __future__ import absolute_import, unicode_literals

def parse_annotations(job_path, seq_path, struc_path, task_id, struc_cats):
	with open(seq_path) as seq_file, open(struc_path) as struc_file:
		seq_lines = seq_file.readlines()
		struc_lines = struc_file.readlines()
		if len(seq_lines)*struc_cats/2 != len(struc_lines):
			line = min(len(seq_lines)*struc_cats/2, len(struc_lines))
			raise ValueError("Misalignment between sequences and annotations", line+1, "Annotations File", struc_lines[line])
	with open(job_path + "/" + task_id + "_struc", "w"):
		for x in xrange(len(struc_lines)):
			seq = seq_lines[2*(x//struc_cats)+1].strip()
			if x % struc_cats == 0:
				if not struc_lines[x][0] == ">":
					raise ValueError("FASTA formatting error", x+1, "Annotations File", struc_lines[x])
				output.write("> " + seq + "\n")
			else:
				line = struc_lines[x].split()
				if not len(line) = len(seq):
					raise ValueError("Length of annotation does not match that of sequence", x+1, "Annotations File", struc_lines[x])
				for i in line:
					try: 
						float(i)
					except ValueError:
						raise ValueError("Annotation value is not a number", x, "Annotations File", input_lines[x])
				output.write(("\t".join(line) + "\n").encode("ascii"))