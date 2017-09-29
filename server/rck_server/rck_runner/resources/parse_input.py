from __future__ import absolute_import, unicode_literals

def parse_pos_neg_input(pos_seq_path, neg_seq_path, output_path):
	with open(pos_seq_path) as pos_seq, open(neg_seq_path) as neg_seq:
		pos_seq_lines = pos_seq.readlines()
		neg_seq_lines = neg_seq.readlines()

	with open(output_path, "w") as output:
		for x in xrange(len(pos_seq_lines)):
			if x % 2 == 0:
				if not pos_seq_lines[x][0] == ">":
					raise ValueError("FASTA formatting error", x+1, "Positive Sequences File", pos_seq_lines[x])
				output.write("> " + str(1) + "\n")
			else:
				line = pos_seq_lines[x].strip().upper().replace("T", "U").encode("ascii")
				permitted = set(["A", "C", "G", "U"])
				if not all(i in permitted for i in line):
					raise ValueError("Non-nucleotide character encountered", x+1, "Positive Sequences File", pos_seq_lines[x])
				output.write(line + "\n")
		if len(pos_seq_lines) % 2 == 1:
			raise ValueError("FASTA formatting error,", len(pos_seq_lines), "Positive Sequences File", pos_seq_lines[-1])
	
		for x in xrange(len(neg_seq_lines)):
			if x % 2 == 0:
				if not neg_seq_lines[x][0] == ">":
					raise ValueError("FASTA formatting error", x+1, "Negative Sequences File", neg_seq_lines[x])
				output.write("> " + str(0) + "\n")
			else:
				line = neg_seq_lines[x].strip().upper().replace("T", "U").encode("ascii")
				permitted = set(["A", "C", "G", "U"])
				if not all(i in permitted for i in line):
					raise ValueError("Non-nucleotide character encountered", x+1, "Negative Sequences File", neg_seq_lines[x])
				output.write(line + "\n")
		if len(neg_seq_lines) % 2 == 1:
			raise ValueError("FASTA formatting error,", len(pos_seq_lines), "Negative Sequences File", neg_seq_lines[-1])


def parse_seq_intens_input(seq_path, intens_path, output_path):
	with open(seq_path) as seq, open(intens_path) as intens:
		seq_lines = seq.readlines()
		intens_lines = intens.readlines()
		if len(seq_lines) != len(intens_lines) * 2:
			line = min(len(seq_lines)-1, len(intens_lines)*2-1)
			raise ValueError("Misalignment between sequences and intensities", line+1, "Sequences File", seq_lines[line])

	with open(output_path, "w") as output:
		for x in xrange(len(seq_lines)):
			if x % 2 == 0:
				if not seq_lines[x][0] == ">":
					raise ValueError("FASTA formatting error", x+1, "Positive Sequences File", seq_lines[x])
				intensity = intens_lines[x/2].strip()
				try: 
					float(intensity)
				except ValueError:
					raise ValueError("Intensity is not a number", x/2+1, "Intensities File", intens_lines[x/2])
				output.write("> " + intensity.encode("ascii") + "\n")
			else:
				line = seq_lines[x].strip().upper().replace("T", "U").encode("ascii")
				permitted = set(["A", "C", "G", "U"])
				if not all(i in permitted for i in line):
					raise ValueError("Non-nucleotide character encountered", x+1, "Sequences File", seq_lines[x])
				output.write(line + "\n")

def parse_rck_format_input(input_path, output_path):
	with open(input_path) as input_file:
		input_lines = input_file.readlines()

	with open(output_path, "w") as output:
		for x in xrange(len(input_lines))
			pair = input_lines[x].split()
			if len(pair) != 2:
				raise ValueError("Whitespace formatting error", x, "Input File", input_lines[x])
			intensity, sequence = pair
			try: 
				float(intensity)
			except ValueError:
				raise ValueError("Intensity is not a number", x, "Input File", input_lines[x])
			output.write("> " + intensity.encode("ascii") + "\n")
			line = sequence.strip().upper().replace("T", "U").encode("ascii")
			if not all(i in permitted for i in line):
				raise ValueError("Non-nucleotide character encountered in sequence", x+1, "Input File", input_lines[x])
			output.write(line + "\n")


def parse_fasta(input_path, output_path):
	with open(input_path) as input_file:
		input_lines = input_file.readlines()

	with open(output_path, "w") as output:
		for x in xrange(len(input_lines)):
			if x % 2 == 0:
				if not input_lines[x][0] == ">":
					raise ValueError("FASTA formatting error", x+1, "Input File", input_lines[x])
				output.write(">" + "\n")
			else:
				line = input_lines[x].strip().upper().replace("T", "U").encode("ascii")
				permitted = set(["A", "C", "G", "U"])
				if not all(i in permitted for i in line):
					raise ValueError("Non-nucleotide character encountered", x+1, "Input File", input_lines[x])
				output.write(line + "\n")