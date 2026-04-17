from app.websocket.manager import manager


class NotificationService:
    async def send_notification(self , user_id:int , msg:str):
        await manager.send_msg(user_id , msg)

notification_service = NotificationService()


