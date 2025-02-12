from django.contrib import admin
from django.urls import path, include
from accounts.views import SignUpView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/", include("django.contrib.auth.urls")),
    path("accounts/signup/", SignUpView.as_view(), name="register"),
    path("", include("iming.urls")),
    # Include other URL patterns here
]

# WebSocket URL routing
from iming.consumers import ChatConsumer

websocket_urlpatterns = [
    path("ws/chat/", ChatConsumer.as_asgi()),
]
