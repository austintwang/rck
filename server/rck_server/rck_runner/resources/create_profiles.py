from __future__ import absolute_import, unicode_literals
import os

def create_Pprof(Eprof, Hprof, Iprof, Mprof):
	return [
		'\t'.join(
			"{0:.4f}".format(1 - sum(float(k) for k in j))
			for j in zip(Eprof[i].split(), Hprof[i].split(), Iprof[i].split(), Mprof[i].split()))
				for i in xrange(len(Eprof))
	]

def create_Uprof(Eprof, Hprof, Iprof, Mprof):
	return [
		'\t'.join(
			"{0:.4f}".format(sum(float(k) for k in j))
			for j in zip(Eprof[i].split(), Hprof[i].split(), Iprof[i].split(), Mprof[i].split()))
				for i in xrange(len(Eprof))
	]

def merge_profiles_PHIME(Epath, Hpath, Ipath, Mpath, output_path):
	with open(Epath) as Efile, open(Hpath) as Hfile, open(Ipath) as Ifile, open(Mpath) as Mfile:
		Eprof = [l.strip() for l in Efile]
		Hprof = [l.strip() for l in Hfile]
		Iprof = [l.strip() for l in Ifile]
		Mprof = [l.strip() for l in Mfile]
	Pprof = create_Pprof(Eprof, Hprof, Iprof, Mprof)
	header = (">" for _ in xrange(len(Eprof)))
	output = "\n".join(j for i in zip(header, Pprof, Hprof, Iprof, Mprof, Eprof) for j in i)
	with open(output_path, "w") as outfile:
		outfile.write(output)

def merge_profiles_PU(Epath, Hpath, Ipath, Mpath, output_path):
	with open(Epath) as Efile, open(Hpath) as Hfile, open(Ipath) as Ifile, open(Mpath) as Mfile:
		Eprof = [l.strip() for l in Efile]
		Hprof = [l.strip() for l in Hfile]
		Iprof = [l.strip() for l in Ifile]
		Mprof = [l.strip() for l in Mfile]
	Pprof = create_Pprof(Eprof, Hprof, Iprof, Mprof)
	Uprof = create_Uprof(Eprof, Hprof, Iprof, Mprof)
	header = (">" for _ in xrange(len(Eprof)))
	output = "\n".join(j for i in zip(header, Pprof, Uprof) for j in i)
	with open(output_path, "w") as outfile:
		outfile.write(output)
