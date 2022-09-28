import os
from fastapi import FastAPI, Request, HTTPException
from utils import validate_token
from worker import celery, classify_image, do_tts, text_similarity, coloring_similarity
from models import ImageParams, TTSParams, SimilarityParams, ColoringParams
from dotenv import load_dotenv

load_dotenv()


def initialize():
    app = FastAPI()

    env_vars = {"sso_url":  os.getenv('sso_url'),
                "sso_realm": os.getenv('sso_realm'),
                "sso_key":  os.getenv('sso_key')}
    return app, env_vars


def check_token(token):
    # validate if the provided token is valid
    try:
        response = validate_token(token, env_vars)
    except:
        raise HTTPException(status_code=400, detail="Invalid provided token")

    if response.status_code != 200 or dict(response.json())['active'] == False:
        raise HTTPException(
            status_code=400, detail="Invalid provided token")

    return


app, env_vars = initialize()


@app.post('/api/classify-image', status_code=201)
def process_image(request: Request, item: ImageParams):

    check_token(item.token)
    payload = {
        "url": item.url,
        "lang": item.lang.value,
    }
    task = classify_image.delay(payload)
    return {"task_id": task.id}


@app.post('/api/do-tts', status_code=201)
def request_tts(request: Request, item: TTSParams):

    check_token(item.token)
    payload = {
        "voice": item.voice,
        "text": item.text,
        "quality": item.quality,
        "candidate": item.candidate,
        "api_mode": True
    }
    task = do_tts.delay(payload)
    return {"task_id": task.id}


@app.post('/api/text-similarity', status_code=201)
def check_text_similarity(request: Request, item: SimilarityParams):

    check_token(item.token)
    payload = {
        "expected_response": item.expected_response,
        "student_response": item.student_response,
    }
    task = text_similarity.delay(payload)
    return {"task_id": task.id}


@app.post('/api/coloring-similarity', status_code=200)
def check_coloring_similarity(request: Request, item: ColoringParams):

    check_token(item.token)
    payload = {
        "expected_image": item.expected_image,
        "student_response": item.student_response,
        "quark_id": str(item.quark_id)
    }

    response = coloring_similarity.run(payload)  # Run task sychronous

    return response


@app.get("/api/tasks/{task_id}")
def get_status(task_id):
    task_result = celery.AsyncResult(task_id)
    result = {
        "task_id": task_id,
        "task_status": task_result.status,
        "task_result": task_result.result
    }
    return result
