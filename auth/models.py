from typing import Optional
from pydantic import BaseModel


class User(BaseModel):
    sub: str
    iss: str
    name: Optional[str]
    email: Optional[str]
    picture: Optional[str]

    @property
    def id(self):
        return self.sub