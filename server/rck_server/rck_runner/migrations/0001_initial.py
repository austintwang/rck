# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import os

from django.db import migrations, models
from django.conf import settings

GENOMES_DIR = settings.MEDIA_ROOT + "/genomes"
RBPS_DIR = settings.MEDIA_ROOT + "/rbps"

def load_genomes(apps, schema_editor):
	genomes = os.listdir(GENOMES_DIR)
	for g in genomes:
		g_model = Genome(name=g)
		g_model.genome_file.name = GENOMES_DIR + "/" + g
		g_model.save()

def load_rbps(apps, schema_editor):
	rbps = os.listdir(RBPS_DIR)
	for r in rbps:
		r_model = RckPreloadedRBP(name=r)
		r.save()
		for m in os.listdir(RBPS_DIR + "/" + r):
			w = int("_".split(m)[-1])
			m_model = RckPreloadedModel(rbp_name=r, width=w)
			m_model.model_file.name = RBPS_DIR + "/" + r + "/model_" + r + "_" + str(w)
			m_model.save()


class Migration(migrations.Migration):

    dependencies = [
    	('rck_runner', '0001_initial'),
    ]

    operations = [
    	migrations.RunPython(load_genomes),
    	migrations.RunPython(load_rbps)
    ]
