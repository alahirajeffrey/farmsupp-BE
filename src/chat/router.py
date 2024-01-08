import models
from auth import utils as auth_utils
from sqlalchemy.orm import Session
from database import get_db
from fastapi import APIRouter, status, Depends, HTTPException, Query
from chat import schemas
from uuid import UUID
from chat import utils as chat_utils

router = APIRouter()

@router.post("", status_code=status.HTTP_201_CREATED, response_model=schemas.ConversationReturnSchema)
async def start_conversation(
    db: Session = Depends(get_db),
    payload: dict = Depends(auth_utils.validate_access_token)
    ):

    ## convert user id from payload to UUID
    user_id_from_token = UUID(payload.get('sub'))
    profile = db.query(models.Profile).filter(models.Profile.user_id == user_id_from_token).first()

    new_conversation = models.Conversation(
        profile_id= profile.id
    )
    
    db.add(new_conversation)
    db.commit()
    db.refresh(new_conversation)

    return new_conversation

@router.get("/{conversation_id}", status_code=status.HTTP_200_OK)
async def get_conversation(
    db: Session = Depends(get_db),
    payload: dict = Depends(auth_utils.validate_access_token),
    page: int = Query(1, description="Page number", gt=0),
    page_size: int = Query(10, description="Items per page", gt=0, le=100)):

    offset = (page - 1) * page_size

    ## convert user id from payload to UUID
    user_id_from_token = UUID(payload.get('sub'))
    profile = db.query(models.Profile).filter(models.Profile.user_id == user_id_from_token).first()

    conversation = db.query(models.Conversation).filter(models.Conversation.profile_id == profile.id).first()
    if not conversation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User has not yet started a conversation"
        )

    messages = db.query(
        models.Message
        ).filter(models.Message.conversation_id == conversation.id
        ).order_by(models.Message.created_at.desc()
        ).offset(offset
        ).limit(page_size
        ).all()

    return { conversation, messages}

@router.post("/message", status_code=status.HTTP_201_CREATED, response_model=schemas.MessageReturnSchema)
async def send_message(
    data: schemas.CreateMessageSchema,
    db: Session = Depends(get_db),
    payload: dict = Depends(auth_utils.validate_access_token)):

    ## convert user id from payload to UUID
    user_id_from_token = UUID(payload.get('sub'))
    profile = db.query(models.Profile).filter(models.Profile.user_id == user_id_from_token).first()

    conversation = db.query(models.Conversation).filter(models.Conversation.profile_id == profile.id).first()
    if not conversation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User has not yet started a conversation"
        )
    
    message = models.Message(
        user_message= data.user_message,
        conversation_id= conversation.id
    )

    db.add(message)
    db.commit()

    ## generate openai response and remove newlines
    response = await chat_utils.generate_openai_response(data.user_message)
    updated_response = chat_utils.remove_newlines(response)

    ## update message 
    message.chatbot_response = updated_response

    db.commit()
    db.refresh(message)

    return message



