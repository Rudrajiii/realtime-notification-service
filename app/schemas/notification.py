from pydantic import BaseModel

class NotificationRequest(BaseModel):
    user_id: int
    msg: str