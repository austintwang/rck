import django.dispatch

inference_status = django.dispatch.Signal(
	providing_args=["id", "success", "message", "linenum", "filetype", "culprit"]
)

prediction_status = django.dispatch.Signal(
	providing_args=["id", "success", "message", "linenum", "filetype", "culprit"]
)