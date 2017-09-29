from __future__ import absolute_import, unicode_literals
from rck_server.settings import BASE_DIR

def get_pwms_prefs(pwm_path):
	with open(pwm_path) as pwm_file:
		prefs_data = dict(i.split(":") for i in pwm_file.readlines().split("\n"))
	for k in prefs_data:
		prefs_data[k].strip().split("\t")
	return prefs_data

def get_matrix_pwm(prefs):
	return zip(*[prefs["A"],prefs["C"],prefs["G"],prefs["U"]])