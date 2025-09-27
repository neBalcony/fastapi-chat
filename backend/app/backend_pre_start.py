from core.db import init_db  # импортируем функцию инициализации базы данных


if __name__ == "__main__":
    print("Running database initialization script...")
    init_db()  # вызываем функцию
    print("Database initialization completed.")