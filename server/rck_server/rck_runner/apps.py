from django.apps import AppConfig
from .signals import inference_status, prediction_status
from django.dispatch import receiver

class RckRunnerConfig(AppConfig):
	name = 'rck_runner'
	verbose_name = "RCK Webserver Runner"

	def ready(self):
		from .models import RckInference, RckPrediction

		@receiver(inference_status)
		def inference_status_callback(sender, **kwargs):
			obj = RckInference.objects.get(pk=kwargs["id"])
			obj.complete = True
			obj.success = kwargs["success"]
			obj.error_message = kwargs.get("message", "")
			obj.error_linenum = kwargs.get("linenum", "")
			obj.error_filetype = kwargs.get("filetype", "")
			obj.error_culprit = kwargs.get("filetype", "")
			obj.save()

		@receiver(prediction_status)
		def inference_status_callback(sender, **kwargs):
			obj = RckPrediction.objects.get(pk=kwargs["id"])
			obj.complete = True
			obj.success = kwargs["success"]
			obj.error_message = kwargs.get("message", "")
			obj.error_linenum = kwargs.get("linenum", "")
			obj.error_filetype = kwargs.get("filetype", "")
			obj.error_culprit = kwargs.get("filetype", "")
			obj.save()



		## importing model classes
		# from .models import MyModel  # or...
		# MyModel = self.get_model('MyModel')

		# # registering signals with the model's string label
		# pre_save.connect(receiver, sender='app_label.MyModel')