from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# Create your views here.


@login_required
def chat_room(request):
    return render(
        request,
        "iming/chat_room.html",
        {
            "username": request.user.username,
            "user_id": request.user.id,
        },
    )
