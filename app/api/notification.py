from fastapi import APIRouter
from app.schemas.notification import NotificationRequest
from app.services.notification_service import notification_service

router = APIRouter()

@router.post("/notify")
async def notify_user(request:NotificationRequest):
    await notification_service.send_notification(
        request.user_id,
        request.msg
    )

    return {"status":"sent"}


