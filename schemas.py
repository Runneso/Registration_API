from pydantic import BaseModel, ConfigDict
from datetime import datetime

class User(BaseModel):
    user_id: int
    user_login: str
    user_password: str
    user_datetime_registration: datetime
    model_config = ConfigDict(from_attributes=True)


class NewUser(BaseModel):
    user_login: str
    user_password: str
    model_config = ConfigDict(from_attributes=True)