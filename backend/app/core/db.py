from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session

from app.core.config import settings
from app.models.models import User

# создаём движок
engine = create_engine(str(settings.database_url))

def init_db():
    # создаём все таблицы
    # Base.metadata.create_all(bind=engine) alembic создает таблицы
    with Session(engine) as session:    
        #TODO: implement
        user = session.execute(select(User)).first()
        if not user:
            user = User(
                username = "username",
                hashed_password = "hashed_password", 
            )
            
            session.add(user)
            session.commit()