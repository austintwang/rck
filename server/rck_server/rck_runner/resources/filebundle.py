from __future__ import absolute_import, unicode_literals
import os
import random

class Filebundle:

	def __init__(self, output_dir, numxval, length):
		if not os.path.isdir(output_dir):
			os.makedirs(output_dir)
		self.provision_directories = {}
		provisions = xrange(numxval)
		for i in provisions:
			provision_directory_name = output_dir + "/" + str(i)
			file_directory = {}
			file_directory["train"] = [self.make_directory(provision_directory_name) , {}]
			file_directory["test"] = [self.make_directory(provision_directory_name) , {}]
			self.provision_directories[i] = file_directory
		self.provisions_remaining = length
		self.tallies = [-(-length // numxval) for i in provisions]
		self.selected_block = None

	def make_directory(self, path):
		if not os.path.isdir(path):
			os.makedirs(path)
		return path

	def advance_block(self):
		selected_block = None
		total = sum( i for i in self.tallies )
		cumu = 0
		num = random.uniform(0, total)
		for x in xrange(len(self.tallies)):
			cumu += self.tallies[x]
			if num <= cumu:
				self.tallies[x] -= 1
				self.provisions_remaining -= 1
				self.selected_block = x
				# print self.tallies ####
				break

	def add_files(self, filenames):
		for k in self.provision_directories:
			for i in filenames:
				self.provision_directories[k]["test"][1][i] = open(self.provision_directories[k]["test"][0] + "/" + i + "_test", "a")
			for i in filenames:
				self.provision_directories[k]["train"][1][i] = open(self.provision_directories[k]["train"][0] + "/" + i + "_train", "a")

	def append(self, linedict):
		"""
		linedict: {filename, line}
		"""
		for y in self.provision_directories:
			if y == self.selected_block:
				for k , v in linedict.iteritems():
					self.provision_directories[y]["test"][1][k].write(v)
			else:
				for k , v in linedict.iteritems():
					self.provision_directories[y]["train"][1][k].write(v)

	def close_files(self, filenames):
		for y in self.provision_directories:
			for i in filenames:
				self.provision_directories[y]["test"][1][i].close()
				self.provision_directories[y]["train"][1][i].close()