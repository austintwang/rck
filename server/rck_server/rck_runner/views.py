from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from .forms import *
from .models import *

def rck_options(request):
	context = {
		"inference_form": RckInferenceForm(),
		"prediction_form": RckPredictionForm()
	}
	return render(request, "rck_runner/index.html", context)

def prediction_options(request):
	prediction_form = RckPredictionForm(request.POST, request.FILES)
	if prediction_form.is_valid():
		rck_instance = RckPrediction.create(request.POST, request.FILES)
		rck_instance.start_rck()
		return HttpResponseRedirect("/prediction/" + rck_instance.model_id + "/")
	context = {
		"inference_form": RckInferenceForm(),
		"prediction_form": prediction_form
	}
	return render(request, "rck_runner/index.html", context)

def prediction_status(request, task_id):
	rck_instance = get_object_or_404(RckPrediction, pk=task_id)
	if rck_instance.complete:
		if rck_instance.success:
			top_sequences = [[i.width, i.rckPredictionResultSingle_set.order_by("-score")] for i in rck_instance.rckPredictionResult_set.order_by("width")]
			context = {
				"task_id": task_id,
				"top_sequences": top_sequences,
			}
			return render(request, 'rck_runner/prediction_complete.html', context)
		else:
			context = {
				"task_id": task_id,
				"error_message": rck_instance.error_message,
				"error_linenum": rck_instance.error_linenum,
				"error_filetype": rck_instance.error_filetype,
				"error_culprit": rck_instance.error_culprit
			}
			return render(request, 'rck_runner/prediction_failed.html', context)
	else:
		context = {
			"task_id": task_id
		}
		return render(request, 'rck_runner/prediction_in_progress.html', context)

def prediction_results_file(request, task_id):
	rck_instance = get_object_or_404(RckPrediction, pk=task_id)
	results_file_path = rck_instance.get_result()
	results_file = open(results_file_path, "r")
	response = HttpResponse(results_file, "application/zip")
	response['Content-Disposition'] = 'attachment; filename=' + str(task_id) + ".zip"
	return response

def inference_options(request):
	inference_form = RckInferenceForm(request.POST, request.FILES)
	if inference_form.is_valid():
		rck_instance = RckInference.create(request.POST, request.FILES)
		rck_instance.start_rck()
		return HttpResponseRedirect("/inference/" + rck_instance.model_id + "/")
	context = {
		"inference_form": inference_form,
		"prediction_form": RckPredictionForm()
	}
	return render(request, "rck_runner/index.html", context)

def inference_status(request, task_id):
	rck_instance = get_object_or_404(RckInference, pk=task_id)
	if rck_instance.complete:
		if rck_instance.success:
			xvalfolds = range(rck_instance.num_x_val)
			models = rck_instance.rckUserModel_set.order_by("width")
			widths = [i.width for i in models]
			xvals = [m.objects.order_by("fold") for m in models]
			context = {
				"task_id": task_id,
				"models": models,
				"xvals": xvals,
				"widths": widths,
				"xvalfolds": xvalfolds
			}
			return render(request, 'rck_runner/inference_complete.html', context)
		else:
			context = {
				"task_id": task_id,
				"error_message": rck_instance.error_message,
				"error_linenum": rck_instance.error_linenum,
				"error_filetype": rck_instance.error_filetype,
				"error_culprit": rck_instance.error_culprit
			}
			return render(request, 'rck_runner/inference_failed.html', context)
	else:
		context = {
			"task_id": task_id
		}
		return render(request, 'rck_runner/inference_in_progress.html', context)

def inference_results_file(request, task_id):
	rck_instance = get_object_or_404(RckInference, pk=task_id)
	results_file_path = rck_instance.get_result()
	results_file = open(results_file_path, "r")
	response = HttpResponse(results_file, "application/zip")
	response['Content-Disposition'] = 'attachment; filename=' + str(task_id) + ".zip"
	return response

