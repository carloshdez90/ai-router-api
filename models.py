from enum import Enum
from typing import Union
from pydantic import BaseModel


class Language(str, Enum):
    es = "es"
    en = "en"


class Item(BaseModel):
    url: str
    lang: Union[Language, None] = Language.en
    token: str
