from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import pymysql

# Ensure pymysql is used as the MySQL driver
pymysql.install_as_MySQLdb()

# Connection format: mysql+pymysql://<username>:<password>@<host>/<dbname>
# Update this with your actual credentials if different.
# If 'exam_ai' doesn't exist, we should create it first (handled in main.py startup).
SQLALCHEMY_DATABASE_URL = "mysql+pymysql://root:1234@localhost/exam_ai"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
