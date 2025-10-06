from fastapi import APIRouter, HTTPException
from app.schemas.massage import MessageCreate
from app.api.deps import CurrentUser, SessionDep
from app.models.models import Chat, Message
from sqlalchemy import and_, or_

router = APIRouter(tags=["massage"])

@router.post("/{chat_id}/message/")
def create_message(chat_id: int, msg: MessageCreate, session: SessionDep, user: CurrentUser):
    chat = session.get(Chat, chat_id)
    if not chat:
        raise HTTPException(status_code=404, detail="Chat not found")
    message = Message(
        content=msg.content,
        chat_id=chat.id,
        user_id=user.id
    )
    print(message)
    session.add(message)
    session.commit()
    session.refresh(message)
    return message

@router.get("/{chat_id}/message/")
def get_messages(
    session: SessionDep,
    chat_id: int,
    limit: int = 50,
    cursor: int|None = None,
    ):
    
    # 1) Проверяем чат
    chat = session.get(Chat, chat_id)
    if not chat:
        raise HTTPException(status_code=404, detail="Chat not found")

    # 2) Базовый запрос — только сообщения этого чата
    q = session.query(Message).filter(Message.chat_id == chat.id)

    # 3) Если курсор указан — найдём сообщение с этим id и ограничим выборку "старее" этого курсора
    if cursor is not None:
        cursor_msg = session.get(Message, cursor)
        if not cursor_msg or cursor_msg.chat_id != chat.id:
            # либо можно молча игнорировать курсор и продолжить от latest,
            # но лучше информировать клиента об ошибочном курсоре
            raise HTTPException(status_code=400, detail="Invalid cursor (message not found in this chat)")

        # Выбираем сообщения, у которых created_at < cursor.created_at
        # или created_at == cursor.created_at и id < cursor.id
        q = q.filter(
            or_(
                Message.created_at < cursor_msg.created_at,
                and_(Message.created_at == cursor_msg.created_at, Message.id < cursor_msg.id),
            )
        )

    # 4) Сортируем по created_at desc, затем id desc, берём limit
    q = q.order_by(Message.created_at.desc(), Message.id.desc()).limit(limit)

    messages = q.all()

    # 5) Вычисляем следующий курсор — id последнего сообщения в ответе (или None)
    next_cursor = messages[-1].id if messages else None

    return {"messages": messages, "next_cursor": next_cursor}