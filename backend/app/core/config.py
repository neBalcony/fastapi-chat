from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    database_url: str = "postgresql://appuser:secretpassword@localhost/appdb"




settings = Settings()

if __name__ == "__main__":
    print(settings.database_url)