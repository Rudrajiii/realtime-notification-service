from fastapi import WebSocket
from typing import Dict


class ConnectionManager:
    def __init__(self):
        # we will get user_id from the respone
        # and will use that to connect that user client
        # via websocket and store in a dictionary as of now
        self.active_connections: Dict[int, WebSocket] = {}
    
    async def connect(self , user_id:int , websocket:WebSocket):
        await websocket.accept()
        # store the user connection in dict
        self.active_connections[user_id] = websocket
    
    def disconnect(self , user_id:int):
        if user_id in self.active_connections:
            del self.active_connections[user_id]
    
    async def send_msg(self , user_id:int , msg: str) -> bool:
        if user_id in self.active_connections:
            websocket = self.active_connections[user_id]
            try:
                await websocket.send_text(msg)
                return True
            except Exception as e:
                print(f"Failed to send message to user {user_id}: {e}")
                self.disconnect(user_id)
                return False
        else:
            print(f"User {user_id} not connected")
            return False

manager = ConnectionManager()



