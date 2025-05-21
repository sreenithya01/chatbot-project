from fastapi import FastAPI
from pydantic import BaseModel
import random
import re
from typing import List, Dict

app = FastAPI()

class Message(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    message: str
    user_id: str = "default_user"

class ChatResponse(BaseModel):
    response: str
    conversation_history: List[Message]

conversations: Dict[str, List[Message]] = {}

# Common Questions & Answers
responses = {
    r"hi|hello|hey": ["Hello! How can I help you today? 😊"],
    r"donate.*clothes": ["Thank you! You can donate clothes from 10 AM to 6 PM at our center."],
    r"donate.*money|how.*donate": ["We accept monetary donations via GPay (9876543210) or our website donation page."],
    r"visit.*timing|when.*visit": ["You can visit us anytime from 10 AM to 6 PM, Monday to Saturday."],
    r"volunteer|help.*kids|join.*volunteer": ["We welcome volunteers! Fill out our volunteer form on the website or call us at 080-12345678."],
    r"food.*donate|donate.*food": ["We accept packaged food and groceries between 10 AM and 5 PM."],
    r"how.*adopt|adoption": ["Please visit our office for adoption-related queries or call 080-87654321 for guidance."],
    r"location|where.*located": ["We are located at 123 Orphanage Street, Bangalore - 560041."],
    r"contact.*number|phone": ["You can reach us at 080-12345678 or email us at support@orphabot.org."],
    r"bye|goodbye|see you": ["Goodbye! Wishing you a wonderful day! 👋"],
    r"thank you|thanks": ["You're most welcome! 😊"]
}



default_responses = ["I'm not sure how to respond to that. Please try again."]

def generate_bot_response(user_input: str) -> str:
    user_input = user_input.lower()
    for pattern, replies in responses.items():
        if re.search(pattern, user_input):
            return random.choice(replies)
    return random.choice(default_responses)

@app.get("/ping")
def ping():
    return {"message": "Chatbot is online!"}

@app.post("/chat", response_model=ChatResponse)
def chat(req: ChatRequest):
    user_id = req.user_id
    user_msg = Message(role="user", content=req.message)
    bot_msg = Message(role="bot", content=generate_bot_response(req.message))

    if user_id not in conversations:
        conversations[user_id] = []
    conversations[user_id].extend([user_msg, bot_msg])

    return ChatResponse(
        response=bot_msg.content,
        conversation_history=conversations[user_id]
    )

