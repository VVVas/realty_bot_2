from django.contrib import admin
from django.urls import path, include

# from bot.views import TelegramBotView
from bot.views import webhook

admin.autodiscover()
admin.site.enable_nav_sidebar = False

urlpatterns = [
    path('admin/', admin.site.urls),
    path('webhook/', webhook, name='webhook')
]
