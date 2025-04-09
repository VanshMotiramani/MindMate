from sqlalchemy import create_engine, engine_from_config
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import psycopg2
from psycopg2.extras import RealDictCursor
from .config import settings


SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

# Ensure all old connections are closed
def drop_all_connections():
    conn = psycopg2.connect(f"dbname=postgres user={settings.database_username} password={settings.database_password} host={settings.database_hostname} port={settings.database_port         }")
    conn.autocommit = True
    cur = conn.cursor()
    cur.execute("""
        SELECT pg_terminate_backend(pg_stat_activity.pid)
        FROM pg_stat_activity
        WHERE pg_stat_activity.datname = 'health'
        AND pid <> pg_backend_pid();
    """)
    cur.close()
    conn.close()

# Drop old connections before creating a new engine
drop_all_connections()


SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


# while True:
#     try:
#         conn = psycopg2.connect(host='localhost', database='health', user='postgres', 
#                         password='1968', cursor_factory=RealDictCursor)
#         cursor = conn.cursor()
#         print("Database connection successful")
#         break
#     except Exception as error:
#         print(f"Database connection unsuccessful {error}")
#         time.sleep(2)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
