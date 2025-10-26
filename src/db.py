from sqlmodel import SQLModel, create_engine
from sqlmodel import Session
from pathlib import Path

DATABASE_URL = f"sqlite:///{Path(__file__).parent.parent / 'data' / 'dev.db'}"

# create uploads/data dir
db_path = Path(__file__).parent.parent / 'data'
db_path.mkdir(parents=True, exist_ok=True)

engine = create_engine(DATABASE_URL, echo=False)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session
