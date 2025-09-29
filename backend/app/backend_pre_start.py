import logging
from sqlalchemy import Engine, text
from sqlalchemy.orm import Session
from tenacity import after_log, before_log, retry, stop_after_attempt, wait_fixed

from app.core.db import engine

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

max_tries = 60 * 5  # 5 minutes
wait_seconds = 1



@retry(
    stop=stop_after_attempt(max_tries),
    wait=wait_fixed(wait_seconds),
    before=before_log(logger, logging.INFO),
    after=after_log(logger, logging.WARN),
)
def wait_for_db(db_engine: Engine) -> None:
    """Ждём, пока БД будет готова отвечать."""
    try:
        with Session(db_engine) as session:
            session.execute(text("SELECT 1"))
    except Exception as e:
        logger.error(f"Database not ready: {e}")
        raise e




if __name__ == "__main__":
    print("Running database initialization script...")
    wait_for_db(engine)  # ждём, пока БД будет готова
    print("Database initialization completed.")
