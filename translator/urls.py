from django.conf.urls import url

from . import views

app_name = 'translator'
urlpatterns = [
	url(r'^$', views.index, name='index'),
	url(r'^get_code/', views.get_code, name='get_code')
]