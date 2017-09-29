from __future__ import absolute_import, unicode_literals
import os
from rck_server.settings import BASE_DIR

def create_Pprof(Eprof, Hprof, Iprof, Mprof):
	return [
		'\t'.join(
			1 - sum(j) 
			for j in zip(Eprof[i].split(), Hprof[i].split(), Iprof[i].split(), Mprof[i].split())) 
				for i in xrange(len(Eprof))
	]

def merge_profiles(Epath, Hpath, Ipath, Mpath, output_path):
	with open(Epat), open(Hpath), open(Ipath), open(Mpath) as Efile, Hfile, Ifile, Mfile:
		Eprof, Hprof, Iprof, Mprof = Efile.readlines(), Hfile.readlines(), Ifile.readlines(), Mfile.readlines()
	Pprof = create_Pprof(Eprof, Hprof, Iprof, Mprof)
	output = "\n".join(j for i in zip(Pprof, Hprof, Iprof, Mprof, Eprof) for j in i)
	with open(output_path, "w") as outfile:
		outfile.write(output)

