from app.websocket.manager import manager
from app.db.session import session_local
from app.models.notification import Notification
from sqlalchemy import select

class NotificationService:
    async def create_notification(self , user_id:int , message: str):
        async with session_local() as session:
            notif = Notification(user_id=user_id, message=message)
            session.add(notif)
            await session.commit()
            await session.refresh(notif)
            return notif
        
    async def send_notification(self , user_id:int , msg:str):
        await manager.send_msg(user_id , msg)

    async def get_undelivered(self , user_id:int):
        async with session_local() as session:
            result = await session.execute(
                select(Notification).where(
                    Notification.user_id == user_id,
                    Notification.is_delivered == False
                )
            )
            return result.scalars().all()
    
    async def mark_delivered(self, notif_id:int):
        async with session_local() as session:
            notif = await session.get(Notification, notif_id)
            if notif:
                notif.is_delivered = True
                await session.commit()
        

notification_service = NotificationService()


