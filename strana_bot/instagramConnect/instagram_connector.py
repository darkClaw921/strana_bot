from typing import Dict, Any, Optional
import requests
from fastapi import FastAPI, HTTPException, Request, Response
from pydantic import BaseModel
from pprint import pprint
from config import get_settings
import aiohttp

app = FastAPI(title="Instagram Connector")
settings = get_settings()
print(settings.INSTAGRAM_ACCESS_TOKEN)
print(settings.INSTAGRAM_PAGE_ID)
print(settings.WEBHOOK_VERIFY_TOKEN)
print(settings.HANDLER_MESSAGE_URL)

async def request_data(url, params):
    async with aiohttp.ClientSession() as session:
        async with session.post(url=url,json=params) as response:
            return await response.text()

class InstagramConnector:
    def __init__(self):
        self.access_token = settings.INSTAGRAM_ACCESS_TOKEN
        self.page_id = settings.INSTAGRAM_PAGE_ID
        self.base_url = settings.GRAPH_API_URL

    async def send_message(self, user_id: str, message: str) -> Dict[str, Any]:
        """Send a message to a user"""
        url = f"{self.base_url}/{self.page_id}/messages"
        data = {
            "recipient": {"id": user_id},
            "message": {"text": message},
            "messaging_type": "RESPONSE",
            "access_token": self.access_token
        }
        
        response = requests.post(url, json=data)
        pprint({"send_message_response": response.json()})
        return response.json()

    async def handle_message(self, sender_id: str, message_text: str) -> Dict[str, Any]:
        """Handle incoming message"""
        print(f"Handling message from {sender_id}: {message_text}")
        response_text = f"Получено сообщение: {message_text}"
        url=f'http://{settings.HANDLER_MESSAGE_UR}/handler_message'
        params={'chat_id':sender_id, 'text':message_text, 'messanger':'instagram', 'username':sender_id}
        # 1/0
        await request_data(url, params)

        return await self.send_message(sender_id, response_text)

# Initialize the connector
instagram = InstagramConnector()

@app.get("/webhook")
async def verify_webhook(request: Request):
    """Verify webhook for Instagram API"""
    params = request.query_params
    hub_mode = params.get("hub.mode")
    hub_challenge = params.get("hub.challenge")
    hub_verify_token = params.get("hub.verify_token")
    
    pprint({
        "received_params": {
            "hub.mode": hub_mode,
            "hub.challenge": hub_challenge,
            "hub.verify_token": hub_verify_token,
        }
    })
    
    if hub_mode == "subscribe" and hub_verify_token == settings.WEBHOOK_VERIFY_TOKEN:
        if hub_challenge:
            return int(hub_challenge)
    raise HTTPException(status_code=403, detail="Invalid verify token")

@app.post("/webhook")
async def webhook(request: Request):
    """Handle incoming messages from Instagram"""
    data = await request.json()
    pprint({"webhook_data": data})
    
    if data.get('object') != 'instagram':
        raise HTTPException(status_code=404, detail="Not Found")

    for entry in data.get('entry', []):
        # Обработка изменений
        for change in entry.get('changes', []):
            if change.get('field') == 'messages':
                value = change.get('value', {})
                sender_id = value.get('sender', {}).get('id')
                message = value.get('message', {}).get('text')
                
                if sender_id and message:
                    print(f"Processing message from {sender_id}: {message}")
                    await instagram.handle_message(sender_id, message)
    
    return {"status": "EVENT_RECEIVED"}

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5009)
