import uvicorn
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
import json
from database import save_message, set_user_online
import asyncio

app = FastAPI(title="ChirpApp Backend")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Храним активные соединения: {username: websocket}
clients = {}

@app.websocket("/ws/{username}")
async def websocket_endpoint(websocket: WebSocket, username: str):
    await websocket.accept()
    clients[username] = websocket
    print(f"✅ Пользователь {username} подключился.")
    set_user_online(username, True)
    
    try:
        while True:
            # Ждем сообщение от пользователя
            data = await websocket.receive_text()
            message_data = json.loads(data)
            
            target = message_data.get("target")
            content = message_data.get("content")
            msg_type = message_data.get("type", "message")  # message, status, typing
            
            if msg_type == "message":
                # Сохраняем в БД
                save_message(username, target, content, is_encrypted=True)
                
                # Если получатель в сети — пересылаем ему
                if target in clients:
                    # Отправляем сообщение в формате {from: ..., content: ...}
                    await clients[target].send_text(json.dumps({
                        "from": username,
                        "content": content,
                        "type": "message",
                        "timestamp": str(__import__('datetime').datetime.now())
                    }))
                    print(f"📨 Переслано от {username} к {target}")
                else:
                    print(f"⚠️ Пользователь {target} не в сети.")
                    
            elif msg_type == "typing":
                # Отправляем уведомление о печати
                if target in clients:
                    await clients[target].send_text(json.dumps({
                        "from": username,
                        "type": "typing"
                    }))
                    
            elif msg_type == "status":
                # Отправляем обновление статуса
                broadcast_message = json.dumps({
                    "from": username,
                    "type": "status",
                    "is_online": content
                })
                for client_username, client_socket in clients.items():
                    if client_username != username:
                        try:
                            await client_socket.send_text(broadcast_message)
                        except:
                            pass
                    
    except WebSocketDisconnect:
        print(f"❌ Пользователь {username} отключился.")
        del clients[username]
        set_user_online(username, False)
    except Exception as e:
        print(f"⚠️ Ошибка: {e}")
        if username in clients:
            del clients[username]

@app.get("/health")
async def health():
    return {"status": "ok", "online_users": len(clients)}

if __name__ == "__main__":
    print("🚀 ChirpApp Backend запущен на ws://localhost:8000")
    uvicorn.run(app, host="0.0.0.0", port=8000)
