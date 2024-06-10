from django.contrib import admin
from django.urls import path

# from bot.views import TelegramBotView
from main import webhook

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('webhook/', TelegramBotView.as_view(), name='webhook')
    path('webhook/', webhook, name='webhook')
]
