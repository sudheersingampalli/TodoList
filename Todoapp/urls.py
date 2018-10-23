from django.conf.urls import url
from . import views

app_name = 'todoapp'

urlpatterns = [
	url(r'register/',views.register,name='register'),
	url(r'list/',views.list,name = 'list'),
  	url(r'edit/(?P<item_id>[0-9]+)',views.edit,name = 'edit'),
    url(r'details/(?P<item_id>[0-9]+)',views.details,name = 'details'),
    ]