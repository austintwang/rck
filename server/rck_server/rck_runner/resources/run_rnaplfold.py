from __future__ import absolute_import, unicode_literals
import subprocess


def rnaplfold(args_dict, input_path, output_path, motif, rnaplfold_path):
	args = [j for i in zip(args_dict.keys(), args_dict.values()) for j in i]
	motif_choices = {
		"E": rnaplfold_path + "/E_RNAplfold",
		"H": rnaplfold_path + "/H_RNAplfold",
		"I": rnaplfold_path + "/I_RNAplfold",
		"M": rnaplfold_path + "/M_RNAplfold"
	}
	args.insert(0, motif_choices[motif])
	with open(input_path) as in_file, open(output_path, "w") as out_file:
		subprocess.call(args, stdin=in_file, stdout=out_file)
