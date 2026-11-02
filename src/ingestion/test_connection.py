
import os

from dotenv import load_dotenv
from sqlalchemy import create_engine, URL, text

load_dotenv()

url = URL.create(
    drivername="postgresql+psycopg2",
    username=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    host=os.getenv("DB_HOST"),
    port=int(os.getenv("DB_PORT", "5432")),
    database=os.getenv("DB_NAME"),
)

engine = create_engine(url)

try:
    with engine.connect() as connection:
        version = connection.execute(
            text("SELECT version()")
        ).scalar_one()

        print("PostgreSQL connection successful!")
        print(version)

except Exception as error:
    print("Connection failed. Check your .env settings.")
    print(error)

finally:
    engine.dispose()
