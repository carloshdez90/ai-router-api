import os
import requests
from celery import Celery
from dotenv import load_dotenv

load_dotenv()

REDIS_HOST = os.getenv('redis_host')
REDIS_PORT = os.getenv('redis_port')
REDIS_PASSWORD = os.getenv('redis_password')
CLASSIFY_IMAGE_URL = os.getenv('classify_image_url')
DO_TTS_URL = os.getenv('do_tts_url')
TEXT_SIMILARITY_URL = os.getenv('text_similarity_url')
COLORING_SIMILARITY_URL = os.getenv('coloring_similarity_url')


celery = Celery(
    'AI API Queue tasks',
    broker=f'redis://:{REDIS_PASSWORD}@{REDIS_HOST}:{REDIS_PORT}/0',
    backend=f'redis://:{REDIS_PASSWORD}@{REDIS_HOST}:{REDIS_PORT}/0',
)


@celery.task(name="Classify imagen")
def classify_image(payload):

    response = requests.post(CLASSIFY_IMAGE_URL, json=payload)

    return response.json()


@celery.task(name="Do TTS")
def do_tts(payload):

    response = requests.post(DO_TTS_URL, json=payload)

    return response.json()


@celery.task(name="Text Similarity")
def text_similarity(payload):

    response = requests.post(TEXT_SIMILARITY_URL, json=payload)

    return response.json()


@celery.task(name="Coloring Similarity")
def coloring_similarity(payload):

    response = requests.post(COLORING_SIMILARITY_URL, json=payload)

    return response.json()
