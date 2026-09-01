import json
import asyncio
from app.core.redis import redis_client, CHANNEL
from app.websocket.manager import manager
from app.db.session import session_local
from app.models.notification import Notification

async def redis_subscriber():
    pubsub = redis_client.pubsub()
    await pubsub.subscribe(CHANNEL)

    try:
        async for message in pubsub.listen():
            if message["type"] != "message":
                continue
                
            try:
                data = json.loads(message["data"])
                user_id = data["user_id"]
                msg = data["message"]
                notif_id = data["id"]

                # send it via socket if user is online
                delivered = await manager.send_msg(user_id, msg)

                # Only mark delivered if it was actually delivered over socket
                if delivered:
                    async with session_local() as session:
                        notif = await session.get(Notification, notif_id)
                        if notif:
                            notif.is_delivered = True
                            await session.commit()
            except Exception as e:
                print(f"Error processing subscriber message: {e}")
                    
    except asyncio.CancelledError:
        print("Subscriber shutting down...")
        await pubsub.unsubscribe(CHANNEL)
        raise
    except Exception as e:
        print(f"Redis subscriber crashed: {e}")


