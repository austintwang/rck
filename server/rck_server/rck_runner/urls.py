from django.conf.urls import url
from . import views

app_name = 'rck_runner'
urlpatterns = [
	url(r'^$', views.rck_options, name='rck_options'),
	url(r'^$', views.inference_options, name='inference_options'),
	url(r'^$', views.prediction_options, name='prediction_options'),
	url(r'^prediction/(?P<task_id>[a-zA-Z0-9]+)/$', views.prediction_status, name='prediction_status'),
	url(r'^prediction/(?P<task_id>[a-zA-Z0-9]+)/download/$', views.prediction_results_file, name='prediction_results_file'),
	url(r'^inference/(?P<task_id>[a-zA-Z0-9]+)/$', views.inference_status, name='inference_status'),
	url(r'^inference/(?P<task_id>[a-zA-Z0-9]+)/download/$', views.inference_results_file, name='inference_results_file'),
]