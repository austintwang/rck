from __future__ import absolute_import, unicode_literals

def verify_annotations(task_id, sequences_path, annotations_path, output_path, alphabet):
	alphabet_len = len(alphabet)

	with open(annotations_path) as annotations_file:
		annotations_lines = annotations_file.readlines()

	# if len(annotations_lines) % (alphabet_len + 1) != 0:
	# 	raise ValueError("Annotations formatting error", len(annotations_lines), "Annotations File", annotations_lines[-1])

	with open(sequences_path) as sequences_file:
		sequences_lines = sequences_file.readlines()

	if len(annotations_lines) / (alphabet_len + 1) != len(sequences_lines) / 2:
		raise ValueError("Number of annotations does not match number of sequences", len(annotations_lines), "Annotations File", annotations_lines[-1])
	
	with open(output_path, "w") as output:
		for x in xrange(len(annotations_lines)/(alphabet_len+1)):
			pos = alphabet_len * x
			if annotations_lines[pos] == ">":
				output.write(">\n")
			else:
				raise ValueError("Annotations formatting error", pos, "Annotations File", annotations_lines[pos])
			annotations_dict = {alphabet[i]: annotations_lines[pos+i+1].strip().split()} for i in xrange(alphabet_len):
			for i in xrange(alphabet_len):
				try:
					annotations_dict[alphabet[i]] = [float(n) for n in annotations_dict[alphabet[i]]]
				except ValueError:
					raise ValueError("Annotations contain non-numerical value(s)", pos+i+1, "Annotations File", annotations_lines[pos+i+1])
				if len(annotations_dict[alphabet[i]]) != len(annotations_dict[alphabet[0]]):
					raise ValueError("Annotations are not of the same length", pos+i+1, "Annotations File", annotations_lines[pos+i+1])
				output.write("\t".join("{0:.4f}".format(n) for n in annotations_dict[alphabet[i]]) + "\n")
