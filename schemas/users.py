from pydantic import BaseModel

class UserOut(BaseModel):
    id: int
    username: str
    telegram_id: int