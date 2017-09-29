from __future__ import absolute_import, unicode_literals
import subprocess
import os

def verify_bed(input_path, output_path):
	with open(input_path) as bed:
		bed_lines = bed.readlines()

	with open(output_path, "w") as bed_out:
		start = False
		for x in xrange(len(bed_file)):
			if not (bed_lines[x].startswith("browser") or bed_lines[x].startswith("track"))
				start = True
			if start:
				row = bed_lines[x].strip().split("\t")
				if len(row) < 3:
					raise ValueError("Insufficient columns in BED input", x+1, "BED Input File", bed_lines[x])
				try: 
					int(row[1]):
				except ValueError:
					raise ValueError("Chromosome start position is not an integer", x+1, "BED Input File", bed_lines[x])
				try: 
					int(row[2]):
				except ValueError:
					raise ValueError("Chromosome end position is not an integer", x+1, "BED Input File", bed_lines[x])
				line = ("\t").join(row).encode("ascii")
				bed_out.write(line + "\n")
			else:
				line = bed_lines[x].strip().encode("ascii")
				bed_out.write(line + "\n")

def make_control(bed_path, control_path):
	with open(input_path) as bed:
		bed_lines = bed.readlines()

	with open(control_path, "w") as control:
		start = False
		for x in xrange(len(bed_file)):
			if not (bed_lines[x].startswith("browser") or bed_lines[x].startswith("track"))
				start = True
			if start:
				row = bed_lines[x].strip().split("\t")
				begin = int(row[1])
				end = int(row[2])
				row[1] = str(end + 300)
				row[2] = str(2 * end - begin + 300)
				line = ("\t").join(row).encode("ascii")
				bed_out.write(line + "\n")
			else:
				line = bed_lines[x].strip().encode("ascii")
				bed_out.write(line + "\n")

def run_bedtools_getfasta(args_dict, bedtools_path):
	# args_dict = {
	# 	"-fi": genome_path,
	# 	"-fo": output_path,
	# 	"-bed": bed_path
	# }
	args = [bed_path, "getfasta"] + [j.encode('ascii') for i in args_dict.items() for j in i]
	subprocess.call(args)


