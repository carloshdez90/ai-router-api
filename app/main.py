import os
from fastapi import FastAPI, Request, HTTPException
from utils import validate_token
from worker import classify_image, celery, do_tts
from models import ImageParams, TTSParams
from dotenv import load_dotenv

load_dotenv()


def initialize():
    app = FastAPI()

    env_vars = {"sso_url":  os.getenv('sso_url'),
                "sso_realm": os.getenv('sso_realm'),
                "sso_key":  os.getenv('sso_key')}
    return app, env_vars


app, env_vars = initialize()


@app.post('/api/classify-image', status_code=201)
def process_image(request: Request, item: ImageParams):

    # validate if the provided token is valid
    try:
        response = validate_token(item.token, env_vars)
    except:
        raise HTTPException(status_code=400, detail="Invalid provided token")

    if response.status_code != 200 or dict(response.json())['active'] == False:
        raise HTTPException(
            status_code=400, detail="Invalid provided token")
    payload = {
        "url": item.url,
        "lang": item.lang.value,
    }
    task = classify_image.delay(payload)
    return {"task_id": task.id}


@app.post('/api/do-tts', status_code=201)
def request_tts(request: Request, item: TTSParams):

    # validate if the provided token is valid
    try:
        response = validate_token(item.token, env_vars)
    except:
        raise HTTPException(status_code=400, detail="Invalid provided token")

    if response.status_code != 200 or dict(response.json())['active'] == False:
        raise HTTPException(
            status_code=400, detail="Invalid provided token")
    payload = {
        "voice": item.voice,
        "text": item.text,
        "quality": item.quality,
        "candidate": item.candidate,
        "api_mode": True
    }
    task = do_tts.delay(payload)
    return {"task_id": task.id}


@app.get("/api/tasks/{task_id}")
def get_status(task_id):
    task_result = celery.AsyncResult(task_id)
    result = {
        "task_id": task_id,
        "task_status": task_result.status,
        "task_result": task_result.result
    }
    return result
