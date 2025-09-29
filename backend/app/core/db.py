from sqlalchemy import create_engine

from app.core.config import settings
from app.models.models import Base

# создаём движок
engine = create_engine(str(settings.database_url))

def init_db():
    # создаём все таблицы
    Base.metadata.create_all(bind=engine)