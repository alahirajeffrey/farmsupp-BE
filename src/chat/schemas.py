from datetime import datetime
from pydantic import BaseModel, UUID4

class ConversationReturnSchema(BaseModel):
    id: UUID4
    profile_id: UUID4
    created_at: datetime
    updated_at: datetime
    # messages: []

class CreateMessageSchema(BaseModel):
    user_message: str

class MessageReturnSchema(CreateMessageSchema):
    id: UUID4
    conversation_id: UUID4
    chatbot_resonse: str
    created_at: datetime
    updated_at: datetime

