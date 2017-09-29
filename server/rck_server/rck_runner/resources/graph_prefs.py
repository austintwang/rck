from __future__ import absolute_import, unicode_literals
from rck_server.settings import BASE_DIR
import matplotlib.pyplot as plt

def graph_prefs(prefs_dict, alphabet, task_id, width, output_dir):
	prefs = [float(prefs_dict[i][0]) for i in alphabet]
	pos = range(len(alphabet))

	plt.bar(pos, prefs, align='center', alpha=0.5)
	plt.set_ylabel("Preference")
	plt.set_title("task_id + ", w = " + str(width)")
	plt.set_xticks(pos, list(alphabet))
	
	with open(output_dir+"/struc_prefs"+task_id+"_w"+str(width)+".svg","w") as svg_out:
		plt.savefig(svg_out, format="svg")
	with open(output_dir+"/struc_prefs"+task_id+"_w"+str(width)+".png","w") as png_out:
		plt.savefig(svg_out, format="png")


