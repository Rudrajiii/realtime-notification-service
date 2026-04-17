from fastapi import FastAPI , WebSocket , WebSocketDisconnect
from app.websocket.manager import manager
from app.api.notification import router as notification_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Realtime Notification System")

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
