from pydantic.main import BaseModel


class BaseModelORM(BaseModel):
    class Config:
        orm_mode = True