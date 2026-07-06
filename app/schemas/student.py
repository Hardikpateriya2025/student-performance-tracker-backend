from pydantic import BaseModel


class StudentCreate(BaseModel):
    user_id: int
    roll_number: str
    class_name: str


class StudentOut(BaseModel):
    id: int
    user_id: int
    roll_number: str
    class_name: str

    class Config:
        from_attributes = True
