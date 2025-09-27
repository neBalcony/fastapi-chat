from fastapi import APIRouter
from api.deps import SessionDep
from models.models import Chat
from schemas.schemas import ChatCreate

router = APIRouter(prefix="/chat", tags=["chat"])

@router.post("/create")
def create_chat(chat_in: ChatCreate, session: SessionDep):
	chat = Chat(**chat_in.dict())
	session.add(chat)
	session.commit()
	session.refresh(chat)
	return chat

