from fastapi import APIRouter
from app.api.deps import SessionDep
from app.models.models import Chat
from app.schemas.schemas import ChatCreate

router = APIRouter(prefix="/chat", tags=["chat"])

@router.post("/create")
def create_chat(chat_in: ChatCreate, session: SessionDep):
	chat = Chat(**chat_in.dict())
	session.add(chat)
	session.commit()
	session.refresh(chat)
	return chat

