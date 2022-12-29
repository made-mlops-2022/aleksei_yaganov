import pickle
from typing import Dict, Union

import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from sklearn.pipeline import Pipeline

ClassificationModel = Union[RandomForestClassifier, XGBClassifier]


def predict_model(
    model: Pipeline, features: pd.DataFrame
) -> np.ndarray:
    predicts = model.predict(features)
    return predicts


def evaluate_model(
    predicts: np.ndarray, target: pd.Series, model_type: str,
) -> Dict[str, float]:
    return {
        "accuracy_score": accuracy_score(target, predicts),
        "precision_score": precision_score(target, predicts),
        "recall_score": recall_score(target, predicts),
        "f1_score": f1_score(target, predicts),
    }


def create_inference_pipeline(
    model: ClassificationModel, transformer: ColumnTransformer
) -> Pipeline:
    return Pipeline([("feature_part", transformer), ("model_part", model)])


def serialize_model(model: object, output: str) -> str:
    with open(output, "wb") as f:
        pickle.dump(model, f)
    return output


def load_model(
    model_path: str
) -> ClassificationModel:
    model = pickle.load(open(model_path, 'rb'))
    return model