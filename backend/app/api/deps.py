from collections.abc import Generator
from typing import Annotated

from fastapi import Depends
from sqlalchemy import select
from app.core.db import engine
from sqlalchemy.orm import Session
from app.models.models import User


def get_db() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_db)]


def get_current_user(session:SessionDep) -> User:
    user = session.execute(select(User)).scalars().first()  # TODO: get user from token
    return user


CurrentUser = Annotated[User, Depends(get_current_user)]