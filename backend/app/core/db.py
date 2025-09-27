from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session

from core.config import settings
from models.models import Base

# создаём движок
engine = create_engine(str(settings.SQLALCHEMY_DATABASE_URI))

def init_db():
    # создаём все таблицы
    Base.metadata.create_all(bind=engine)