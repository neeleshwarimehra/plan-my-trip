from sqlalchemy import text
from app.core.database import engine

try:
    with engine.connect() as connection:
        result = connection.execute(
            text("SELECT current_database(), current_user")
        )

        database, user = result.fetchone()

        print("Database connected successfully!")
        print("Database:", database)
        print("User:", user)

finally:
    engine.dispose()