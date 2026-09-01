from fastapi import FastAPI , WebSocket , WebSocketDisconnect
from app.websocket.manager import manager
from app.api.notification import router as notification_router
from fastapi.middleware.cors import CORSMiddleware
from app.services.notification_service import notification_service
from contextlib import asynccontextmanager

import asyncio
from app.services.subscriber import redis_subscriber
from app.db.init_db import init_db

@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    print("db initialized...")
    task = asyncio.create_task(redis_subscriber())
    print("redis subscriber started...")
    yield
    task.cancel()

app = FastAPI(title="Realtime Notification System", lifespan=lifespan)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(notification_router)

@app.websocket("/ws/{user_id}")
async def websocket_endpoint(websocket:WebSocket , user_id:int):
    await manager.connect(user_id , websocket)

    undelivered = await notification_service.get_undelivered(user_id)

    for notif in undelivered:
        await websocket.send_text(notif.message)
        await notification_service.mark_delivered(notif.id)

    try:
        while True:
            # keep connection alive
            data = await websocket.receive_text()
            await websocket.send_text(f"ECHO: {data}")
    except WebSocketDisconnect:
        manager.disconnect(user_id)


@app.get("/")
async def root():
    return {"message": "Welcome to Realtime Notification Server"}
