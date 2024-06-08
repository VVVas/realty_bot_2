from django.contrib import admin
from django.urls import include, path

from bot.views import TelegramBotView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('webhook/', TelegramBotView.as_view(), name='webhook'),
    path('sb/', include('simplebot.urls', namespace='simplebot')),
]
