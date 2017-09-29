from __future__ import absolute_import, unicode_literals
import os

def verify_fasta(file_path):
	is_fasta = True
	allowed_chars = "actguACTGU"
	with open(file_path) as in_file:
		in_lines = in_file.readlines()
		for i in xrange(len(in_lines)):
			if i % 2 == 1:
				is_fasta = (in_lines[i][0] == ">")
			else:
				is_fasta = all(c in allowed_chars for c in in_lines[i])

	return is_fasta