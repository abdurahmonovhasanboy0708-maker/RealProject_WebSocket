from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncJsonWebsocketConsumer

from .models import Student


class DashboardConsumer(AsyncJsonWebsocketConsumer):
    group_name = "dashboard"

    async def connect(self):
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()
        await self.send_json({"type": "init", "students": await self.get_students()})

    async def disconnect(self, code):
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def ball_update(self, event):
        await self.send_json({
            "type": "ball_update",
            "student_id": event["student_id"],
            "ball": event["ball"],
        })

    @database_sync_to_async
    def get_students(self):
        result = []
        for s in Student.objects.select_related("ball"):
            result.append({
                "id": s.id,
                "fullname": s.fullname,
                "photo": s.photo.url if s.photo else None,
                "ball": s.ball.coin if hasattr(s, "ball") else 0,
            })
        return result

