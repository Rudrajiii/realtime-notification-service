from fastapi import APIRouter
from app.schemas.notification import NotificationRequest
from app.services.notification_service import notification_service
from app.core.redis import redis_client , CHANNEL
from app.db.session import session_local
from app.models.notification import Notification
from sqlalchemy import select
import json

router = APIRouter()

@router.post("/notify")
async def notify_user(request:NotificationRequest):

    """
    1. store in DB 
    2. publish event in redis
    """

    notification = await notification_service.create_notification(
        request.user_id,
        request.msg
    )

    event = {
        "id": notification.id,
        "user_id": request.user_id,
        "message": request.msg
    }

    await redis_client.publish(CHANNEL, json.dumps(event))

    # await notification_service.send_notification(
    #     request.user_id,
    #     request.msg
    # )

    return {"status":"queued"}


@router.get("/notification/{user_id}")
async def get_notifications(user_id:int):
    async with session_local() as session:
        result = await session.execute(
            select(Notification).where(Notification.user_id == user_id)
        )

        notifications = result.scalars().all()

        return [
            {
                "id": n.id,
                "message": n.message,
                "delivered": n.is_delivered,
                "read": n.is_read
            }
            for n in notifications
        ]

