from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Session


class Base(DeclarativeBase):
    pass


db_url = "postgresql://localhost/chougodno"
engine = create_engine(db_url)
session = Session(engine)
