from typing import List
from fastapi import APIRouter, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import joinedload
from app.api.deps import CurrentUser, SessionDep
from app.models.models import Chat, User
from app.schemas.chat import ChatAddUsers, ChatCreate, ChatRead, ChatRemoveUsers, ChatUpdate

router = APIRouter(prefix="/chat", tags=["chat"])

@router.get("/", response_model=List[ChatRead])
def get_avalible_chats(session: SessionDep, user: CurrentUser):
    chats = session.execute(select(Chat).where(Chat.users.contains(user))).scalars().all()
    return [ChatRead.model_validate(chat) for chat in chats]


@router.get("/{chat_id}", response_model=ChatRead)
def get_chat_info(chat_id: int, session: SessionDep, user: CurrentUser):
    stmt = select(Chat).options(joinedload(Chat.users)).where(Chat.id == chat_id)
    chat = session.execute(stmt).scalars().first()
    if not chat:
        raise HTTPException(status_code=404, detail="Chat not found")
    if user not in chat.users:
        raise HTTPException(status_code=403, detail="Not authorized")
    return ChatRead.model_validate(chat)

@router.post("/", response_model=ChatRead)
def create_chat(chat_in: ChatCreate, session: SessionDep, current_user: CurrentUser):
    if current_user is None:
        raise HTTPException(status_code=403, detail="Not authorized")
    # Check user existence
    user_ids = chat_in.users
    found_users = []
    if user_ids:
        stmt = select(User).where(User.id.in_(user_ids))
        found_users = session.scalars(stmt).all()
        found_ids = {u.id for u in found_users}
        missing_ids = [uid for uid in user_ids if uid not in found_ids]
        if missing_ids:
            raise HTTPException(status_code=404, detail=f"Users not exist: {missing_ids}")
    

    if chat_in.type == "dm":
        if len(chat_in.users) != 1:
            raise HTTPException(status_code=400, detail="Direct messages must have one user")
        else:
            if chat_in.users[0] == current_user.id:
                raise HTTPException(status_code=400, detail="You cannot message yourself")


    users = session.execute(select(User).where(User.id.in_(chat_in.users))).scalars().all()
    
    if current_user.id not in chat_in.users:
        users.append(current_user)
    

    chat = Chat(
        title=chat_in.title,
        description=chat_in.description,
        type=chat_in.type,
        users=users
    )
    session.add(chat)
    session.commit()
    session.refresh(chat)
    return ChatRead.model_validate(chat)



@router.put("/{chat_id}", response_model=ChatUpdate)
async def update_chat(chat_id: int, chat_update: ChatUpdate, session: SessionDep, user: CurrentUser):
    chat = session.get(Chat, chat_id)
    if chat is None:
        raise HTTPException(status_code=404, detail="Chat not found")
    if user not in chat.users:
        raise HTTPException(status_code=403, detail="Not authorized")

    chat.title = chat_update.title
    chat.description = chat_update.description
    session.add(
        chat
    )
    session.commit()

    return ChatUpdate.model_validate(chat)

#TODO: Make schems for return
@router.delete("/{chat_id}/user", response_model=ChatRemoveUsers)
async def remove_users_from_chat(chat_id:int ,user_ids: List[int], session: SessionDep, user: CurrentUser):
    stmt = select(Chat).options(joinedload(Chat.users)).where(Chat.id == chat_id)
    chat = session.execute(stmt).scalars().first()
    
    if not chat:
        raise HTTPException(status_code=404, detail="Chat not found")
    if user not in chat.users:
        raise HTTPException(status_code=403, detail="Not authorized")

    chat_users_id = [user.id for user in chat.users]
    not_in_chat = [uid for uid in user_ids if uid not in chat_users_id]
    # Check all users in chat
    if  not_in_chat:
        raise HTTPException(status_code=404, detail=f"Users id not founded {not_in_chat}")
    if not user_ids:
        return {"users_removed": []}


    chat.users = [u for u in chat.users if u.id not in user_ids]
    session.commit()


    return ChatRemoveUsers(removed_users=user_ids)
    
@router.patch("/{chat_id}/user", response_model=ChatAddUsers)
async def add_users(chat_id:int ,user_ids: List[int], session: SessionDep, user: CurrentUser):

    # Get chat with users
    stmt = select(Chat).options(joinedload(Chat.users)).where(Chat.id == chat_id)
    chat = session.execute(stmt).scalars().first()
    
    if not chat:
        raise HTTPException(status_code=404, detail="Chat not found")

    if user not in chat.users:
        raise HTTPException(status_code=403, detail="Not authorized")

    # Get users from user_ids
    stmt = select(User).where(User.id.in_(user_ids))
    found_users = session.scalars(stmt).all()
    
    found_ids = {u.id for u in found_users}
    
    ## Check for missing users
    missing_ids = [uid for uid in user_ids if uid not in found_ids]
    if missing_ids:
        raise HTTPException(status_code=404, detail=f"Users not exist: {missing_ids}")

    # Check existing users
    current_user_ids = [user.id for user in chat.users]
    already_in_chat = [uid for uid in user_ids if uid in current_user_ids]
    if already_in_chat:
        raise HTTPException(status_code=400, detail=f"Users already in chat: {already_in_chat}")

    chat.users.append(*found_users)
    session.commit()

    return ChatAddUsers(added_users=[user.id for user in found_users])
