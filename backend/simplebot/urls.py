from django.urls import path

from . import views

app_name = 'simplebot'

urlpatterns = [
    path('', views.index, name='index'),
    path('hook/', views.talkin_to_me_bruh, name='hook'),
    path('telegram', views.telegram, name='ptb'),
]
