import logging
import os
import sys
from typing import List

import numpy as np
import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel

from make_request import load_object


logger = logging.getLogger(__name__)
handler = logging.StreamHandler(sys.stdout)
logger.setLevel(logging.INFO)
logger.addHandler(handler)


s3_bucket = None
model = None


class DataModel(BaseModel):
    data: List[List[float]]


class PredictResponse(BaseModel):
    heart_disease: int


app = FastAPI()


@app.get("/")
def read_root():
    return "Hello! It is entry point of your predicter"


@app.on_event("startup")
def get_s3():
    global s3_bucket
    s3_bucket = os.getenv("S3_BUCKET")
    if s3_bucket is None:
        err = f"S3_BUCKET {s3_bucket} is None"
        logger.error(err)
        raise RuntimeError(err)


@app.on_event("startup")
def load_model():
    global model
    path_to_model = "model/" + os.getenv("PATH_TO_MODEL")

    if path_to_model is None:
        err = f"PATH_TO_MODEL {path_to_model} is None"
        logger.error(err)
        raise RuntimeError(err)

    model = load_object(path_to_model)


@app.get("/health")
def health() -> bool:
    return not (model is None) and \
           not (s3_bucket is None)


@app.post("/predict/", response_model=List[PredictResponse])
def predict(request: DataModel) -> List[PredictResponse]:
    predictions = model.predict(np.array(request.data))
    return [PredictResponse(heart_disease=p) for p in predictions]


if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port="8000")
