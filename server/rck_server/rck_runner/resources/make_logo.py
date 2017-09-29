from __future__ import absolute_import, unicode_literals
from rck_server.settings import BASE_DIR
from weblogolib import *

def make_logo(pwm, task_id, width, output_dir):
	data = LogoData.from_counts("ACGU", pwm)
	options = LogoOptions()
	options.title = task_id + ", w = " + str(width)
	format = LogoFormat(data, options)
	svg = svg_formatter(data, format)
	png = png_print_formatter(data, format)
	with open(output_dir+"/logo"+task_id+"_w"+str(width)+".svg","w") as svg_out:
		svg_out.write(svg)
	with open(output_dir+"/logo"+task_id+"_w"+str(width)+".png","w") as png_out:
		png_out.write(svg)






# import matplotlib as mpl
# from matplotlib.text import TextPath
# from matplotlib.patches import PathPatch
# from matplotlib.font_manager import FontProperties
# import matplotlib.pyplot as plt

# fp = FontProperties(family="Arial", weight="bold") 
# globscale = 1.35
# LETTERS = { "U" : TextPath((-0.305, 0), "T", size=1, prop=fp),
#             "G" : TextPath((-0.384, 0), "G", size=1, prop=fp),
#             "A" : TextPath((-0.35, 0), "A", size=1, prop=fp),
#             "C" : TextPath((-0.366, 0), "C", size=1, prop=fp) }
# COLOR_SCHEME = {'G': 'orange', 
#                 'A': 'red', 
#                 'C': 'blue', 
#                 'U': 'darkgreen'}

# def letterAt(letter, x, y, yscale=1, ax=None):
#     text = LETTERS[letter]

#     t = mpl.transforms.Affine2D().scale(1*globscale, yscale*globscale) + \
#         mpl.transforms.Affine2D().translate(x,y) + ax.transData
#     p = PathPatch(text, lw=0, fc=COLOR_SCHEME[letter],  transform=t)
#     if ax != None:
#         ax.add_artist(p)
#     return p


# fig, ax = plt.subplots(figsize=(10,3))

# all_scores = ALL_SCORES2
# x = 1
# maxi = 0
# for scores in all_scores:
#     y = 0
#     for base, score in scores:
#         letterAt(base, x,y, score, ax)
#         y += score
#     x += 1
#     maxi = max(maxi, y)

# plt.xticks(range(1,x))
# plt.xlim((0, x)) 
# plt.ylim((0, maxi)) 
# plt.tight_layout()      
# plt.show()