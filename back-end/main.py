from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy import create_engine, Column, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from pydantic import BaseModel
from typing import List
import openai
import os
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware

load_dotenv()

app = FastAPI()

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins, you can specify certain domains
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods (GET, POST, PUT, DELETE, etc.)
    allow_headers=["*"],  # Allows all headers
)

# Database setup
SQLALCHEMY_DATABASE_URL = "sqlite:///./chatbot.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class MessageDB(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, index=True)
    content = Column(String, index=True)
    is_user = Column(Boolean, default=True)  # True for user, False for bot
    related_id = Column(Integer, index=True)  # For linking user and bot messages

Base.metadata.create_all(bind=engine)

# Pydantic models
class MessageCreate(BaseModel):
    content: str

class Message(BaseModel):
    id: int
    content: str
    is_user: bool

    class Config:
        orm_mode = True
        from_attributes = True

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_bot_response(user_message: str) -> str:
    openai.api_key = os.getenv("OPENAI_API_KEY")
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": user_message}
        ]
    )

    return response.choices[0].message.content

@app.post("/messages", response_model=List[Message])
async def create_message(message: MessageCreate, db: Session = Depends(get_db)):
    # Create user message
    db_message = MessageDB(content=message.content, is_user=True)
    db.add(db_message)
    db.commit()
    db.refresh(db_message)
    
    # Get bot response
    bot_response = get_bot_response(message.content)
    # Create bot response, related to the user message
    db_bot_message = MessageDB(content=bot_response, is_user=False, related_id=db_message.id)
    db.add(db_bot_message)
    db.commit()
    db.refresh(db_bot_message)
    
    return [
        Message.from_orm(db_message),
        Message.from_orm(db_bot_message)
    ]

@app.get("/messages", response_model=List[Message])
async def get_messages(db: Session = Depends(get_db)):
    messages = db.query(MessageDB).all()
    return [Message.from_orm(message) for message in messages]

@app.put("/messages/{message_id}", response_model=Message)
async def update_message(message_id: int, message: MessageCreate, db: Session = Depends(get_db)):
    db_message = db.query(MessageDB).filter(MessageDB.id == message_id, MessageDB.is_user == True).first()
    if db_message is None:
        raise HTTPException(status_code=404, detail="Message not found or not editable")
    
    # Update the user's message
    db_message.content = message.content
    db.commit()
    db.refresh(db_message)
    
    # Update the corresponding bot response
    db_bot_message = db.query(MessageDB).filter(MessageDB.related_id == message_id, MessageDB.is_user == False).first()
    if db_bot_message:
        bot_response = get_bot_response(message.content)
        db_bot_message.content = bot_response
        db.commit()
        db.refresh(db_bot_message)

    return Message.from_orm(db_message)

@app.delete("/messages/{message_id}")
async def delete_message(message_id: int, db: Session = Depends(get_db)):
    db_message = db.query(MessageDB).filter(MessageDB.id == message_id, MessageDB.is_user == True).first()
    if db_message is None:
        raise HTTPException(status_code=404, detail="Message not found or not deletable")
    
    # Delete the user's message
    db.delete(db_message)
    
    # Delete the corresponding bot response
    db_bot_message = db.query(MessageDB).filter(MessageDB.related_id == message_id, MessageDB.is_user == False).first()
    if db_bot_message:
        db.delete(db_bot_message)
    
    db.commit()
    return {"message": "Message and bot response deleted successfully"}
