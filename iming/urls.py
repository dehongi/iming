from django.urls import path
from . import views

app_name = "iming"

urlpatterns = [
    path("", views.chat_room, name="chat_room"),
]
