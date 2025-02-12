from channels.generic.websocket import AsyncWebsocketConsumer
import json
from datetime import datetime
from channels.db import database_sync_to_async
from .models import Message
from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope["user"]
        self.user_id = str(self.user.id)
        self.username = self.user.username

        # Join user's personal channel for private messages
        self.personal_group = f"user_{self.user_id}"
        await self.channel_layer.group_add(self.personal_group, self.channel_name)

        # Join general chat room
        self.room_name = "chat_room"
        self.room_group_name = "chat_%s" % self.room_name
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)

        await self.accept()

        # Send user online status
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "user_status",
                "user": self.username,
                "status": "online",
                "request_status": False,
            },
        )

        # Request status from all users
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "request_status",
                "requester": self.username,
            },
        )

        # Send recent messages history
        await self.send_message_history()

    @database_sync_to_async
    def get_user_by_username(self, username):
        try:
            return User.objects.get(username=username)
        except User.DoesNotExist:
            return None

    @database_sync_to_async
    def save_message(self, content, is_private=False, recipient=None):
        recipient_user = None
        if recipient:
            recipient_user = User.objects.get(username=recipient)

        message = Message.objects.create(
            sender=self.user,
            content=content,
            is_private=is_private,
            recipient=recipient_user,
        )
        return message

    @database_sync_to_async
    def get_recent_messages(self):
        # Get last 50 messages (public and private for this user)
        messages = (
            Message.objects.filter(
                models.Q(is_private=False)
                | models.Q(is_private=True, recipient=self.user)
                | models.Q(is_private=True, sender=self.user)
            )
            .select_related("sender")
            .order_by("-timestamp")[:50]
        )
        return list(reversed(messages))

    async def send_message_history(self):
        messages = await self.get_recent_messages()
        for message in messages:
            await self.send(
                text_data=json.dumps(
                    {
                        "type": "message",
                        "message": message.content,
                        "sender": message.sender.username,
                        "timestamp": message.timestamp.isoformat(),
                        "is_private": message.is_private,
                    }
                )
            )

    async def disconnect(self, close_code):
        # Send user offline status
        await self.channel_layer.group_send(
            self.room_group_name,
            {"type": "user_status", "user": self.username, "status": "offline"},
        )

        # Leave room groups
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)
        await self.channel_layer.group_discard(self.personal_group, self.channel_name)

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message_type = text_data_json.get("type", "message")
        message = text_data_json.get("message", "")
        recipient = text_data_json.get("recipient", None)

        # Save message to database
        saved_message = await self.save_message(
            content=message, is_private=bool(recipient), recipient=recipient
        )

        message_data = {
            "type": "chat_message",
            "message": message,
            "sender": self.username,
            "timestamp": saved_message.timestamp.isoformat(),
        }

        if recipient:
            # Send private message
            recipient_group = f"user_{recipient}"
            message_data["is_private"] = True
            await self.channel_layer.group_send(recipient_group, message_data)
            # Also send to sender
            await self.channel_layer.group_send(self.personal_group, message_data)
        else:
            # Send message to room group
            await self.channel_layer.group_send(self.room_group_name, message_data)

    async def chat_message(self, event):
        # Send message to WebSocket
        await self.send(
            text_data=json.dumps(
                {
                    "type": "message",
                    "message": event["message"],
                    "sender": event["sender"],
                    "timestamp": event["timestamp"],
                    "is_private": event.get("is_private", False),
                }
            )
        )

    async def user_status(self, event):
        # Don't send status updates triggered by our own status request
        if (
            event.get("request_status", False)
            and event.get("requester") == self.username
        ):
            return

        # Send user status to WebSocket
        await self.send(
            text_data=json.dumps(
                {"type": "status", "user": event["user"], "status": event["status"]}
            )
        )

    async def request_status(self, event):
        """Handle status request from new users"""
        if event["requester"] != self.username:
            # Send our status to the requester
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    "type": "user_status",
                    "user": self.username,
                    "status": "online",
                    "request_status": False,
                },
            )
