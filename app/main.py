from typing import List
from fastapi import FastAPI, BackgroundTasks, Depends
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from pydantic import BaseModel
from sqlalchemy.orm import sessionmaker, Session

DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Define SQLAlchemy model
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)

Base.metadata.create_all(bind=engine)

# Pydantic model for User
class UserCreate(BaseModel):
    name: str

app = FastAPI()

# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/user/", response_model=List[UserCreate])
async def get_users(db: Session = Depends(get_db)):
    users = db.query(User).all()
    return [{"name": user.name} for user in users]

@app.post("/user/")
async def create_user(user: UserCreate, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    db_user = User(name=user.name)
    db.add(db_user)
    db.commit()
    background_tasks.add_task(print_message, user.name)
    return {"name": user.name, "message": "User created successfully"}

async def print_message(name: str):
    print(f"User {name} created successfully!")
