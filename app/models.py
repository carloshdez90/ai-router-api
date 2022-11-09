from enum import Enum
from typing import Union
from pydantic import BaseModel
import uuid


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


class ColoringParams(BaseModel):
    expected_image: str
    student_response: str
    quark_id: uuid.UUID
    token: str


class STTParams(BaseModel):
    audio_source: str
    token: str
