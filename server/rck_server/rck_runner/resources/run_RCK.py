from __future__ import absolute_import, unicode_literals
import subprocess
import os
# from rck_server.settings import BASE_DIR

def rck(args_dict, rck_path):
	"""
	Python wrapper around RCK
	args_dict contains arguments to be passed upon execution:
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
	os.makedirs(args_dict["-m"])
	args = [j.encode('ascii') for i in args_dict.items() for j in i]
	args.insert(0, rck_path)
	# print " ".join(args) ####
	subprocess.call(args)