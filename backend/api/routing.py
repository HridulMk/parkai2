from django.urls import re_path

from .consumers import SpaceSlotsConsumer


websocket_urlpatterns = [
    re_path(r'^ws/spaces/(?P<space_id>\d+)/slots/?$', SpaceSlotsConsumer.as_asgi()),
]
