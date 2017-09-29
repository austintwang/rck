from django import forms
from models import *

class RckInferenceForm(forms.Form):
	INPUT_CHOICES = (
		("pos_neg", "Positive and Negative Sequences"),
		("bed", "Positive BED Peaks"),
		("seq_intens_fasta", "Sequences and Intensities (BED)"),
		("seq_intens_bed", "Sequences and Intensities (BED)"),
		("rck", "RCK/RNAContext Format Input"),
	)

	ANNOT_GENERATION_CHOICES = (
		("True", "RNAplfold-Generated"),
		("False", "User-Specified")
	)

	ANNOT_ALPHABET_CHOICES = (
		("PHIME", "PHIME"),
		("PU", "PU")
	)

	# genomes = [(i.name, i.readable_name) for i in Genomes.objects]

	input_format = forms.ChoiceField(label="Input Format", choices=INPUT_CHOICES)
	pos_seq = forms.FileField(label="Sequences that bind to RBP (FASTA)", required=False)
	neg_seq = forms.FileField(label="Sequences that do not bind to RBP (FASTA)", required=False)
	seq_fasta = forms.FileField(label="Sequences File (FASTA)", required=False)
	seq_bed = forms.FileField(label="Sequences File (BED)", required=False)
	intens = forms.FileField(label="Intensities File", required=False)
	rck_in = forms.FileField(label="RCK format input", required=False)

	genome = forms.ModelChoiceField(label="Genome", queryset=Genome.objects, required=False)

	generate_annotations = forms.TypedChoiceField(label="Structural Annotations Source", choices=ANNOT_GENERATION_CHOICES, coerce=bool, empty_value=False)
	alphabet = forms.ChoiceField(label="Structural Alphabet", choices=ANNOT_ALPHABET_CHOICES)
	annotations = forms.FileField(label="Annotations File", required=False)

	min_width = forms.IntegerField(label="K-mer width lower bound")
	max_width = forms.IntegerField(label="K-mer width upper bound")
	max_iterations = forms.IntegerField(label="Maximum iterations before termination")
	num_x_val = forms.IntegerField(label="Number-Fold Cross-Validation", min_value=2, max_value=20)


class RckPredictionForm(forms.Form):
	# def __init__(self, *args, **kwargs):
	# 	choices = kwargs.pop('preloaded_models')
	#  	super(RckPredictionForm, self).__init__(*args, **kwargs)
	#  	self.fields["model_name_preloaded"] = forms.ChoiceField(choices=choices)

	DUMMY_CHOICES = (
		(" ", " "),
	)

	INPUT_CHOICES = (
		("bed", "BED Peaks"),
		("fasta", "FASTA"),
	)

	MODEL_TYPE_CHOICES = (
		("preloaded", "From Server"),
		("by_id", "By Inference Task ID"),
		("upload", "User-Uploaded")

	)

	ANNOT_GENERATION_CHOICES = (
		("True", "RNAplfold-Generated"),
		("False", "User-Specified")
	)

	ANNOT_ALPHABET_CHOICES = (
		("PHIME", "PHIME"),
		("PU", "PU")
	)

	model_type = forms.ChoiceField(label="Model Source", choices=MODEL_TYPE_CHOICES)
	model_preloaded = forms.ModelChoiceField(label="Server Models", queryset=RckPreloadedRBP.objects, required=False)
	model_by_id = forms.ModelChoiceField(label="Inference Task ID", queryset=RckInference.objects, required=False, widget=forms.TextInput())
	# model_name = forms.CharField(label="Inference Task ID", max_length=10, required=False)
	# model_name_preloaded = forms.ChoiceField(label="Server Models", choices=DUMMY_CHOICES)
	model_file = forms.FileField(label="Model File", required=False)

	input_format = forms.ChoiceField(label="Input Format", choices=INPUT_CHOICES)
	seq_file = forms.FileField(label="Sequences File")
	intens = forms.FileField(label="Intensities File", required=False)

	genome = forms.ModelChoiceField(label="Genome", queryset=Genome.objects, required=False)

	generate_annotations = forms.TypedChoiceField(label="Structural Annotations Source", choices=ANNOT_GENERATION_CHOICES, coerce=bool, empty_value=False)
	alphabet = forms.ChoiceField(label="Structural Alphabet", choices=ANNOT_ALPHABET_CHOICES)
	annotations = forms.FileField(label="Annotations File", required=False)

	min_width = forms.IntegerField(label="K-mer width lower bound")
	max_width = forms.IntegerField(label="K-mer width upper bound")
	max_iterations = forms.IntegerField(label="Maximum iterations before termination")
