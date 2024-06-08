from django.urls import path

from . import views

app_name = 'simplebot'

urlpatterns = [
    path('', views.telegram, name='telegram'),
]
