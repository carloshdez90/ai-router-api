from enum import Enum
from typing import Union
from pydantic import BaseModel


class Language(str, Enum):
    es = "es"
    en = "en"


class ImageParams(BaseModel):
    url: str
    lang: Union[Language, None] = Language.en
    token: str


class TTSParams(BaseModel):
    voice: str
    text: str
    quality: str
    candidate: Union[int, None] = 1
    api_mode: Union[bool, None] = True
    token: str


class SimilarityParams(BaseModel):
    expected_response: str
    student_response: str
    token: str
