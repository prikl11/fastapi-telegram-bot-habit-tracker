from sqlalchemy.orm import Session
from models import Users

def read_users(db: Session):
    users = db.query(Users).all()
    if not users:
        return {"message": "No users found"}

    return users