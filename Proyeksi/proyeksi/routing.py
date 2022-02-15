from django.urls import path, re_path

from proyeksi.consumers import ProyeksiConsumer

ws_urlpatterns = [
  path('ws/proyeksi/', ProyeksiConsumer.as_asgi()),
]