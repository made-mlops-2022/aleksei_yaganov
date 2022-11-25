import pandas as pd
from fastapi.testclient import TestClient

from app.main import app
from app.prepare_data_utils import prepare_data, make_features, PredictPipelineParams
from app.get_data_utils import get_model, get_transformer, \
    get_config_for_prediction, read_config_params


DATA_FOR_TEST = pd.DataFrame(data={'Age': [40, 37], 'Sex': ['M', 'M'],
                                   'ChestPainType': ['ATA', 'ATA'], 'RestingBP': [140, 130],
                                   'Cholesterol': [289, 283], 'FastingBS': [0, 0],
                                   'RestingECG': ['Normal', 'ST'], 'MaxHR': [172, 98],
                                   'ExerciseAngina': ['N', 'N'], 'Oldpeak': [0, 0],
                                   'ST_Slope': ['Up', 'Up'], 'HeartDisease': [0, 0]})

EXPECTED_TARGET = pd.Series([0, 0], copy=False)

CONFIG_PATH = 's3_config.yaml'


def test_entrypoint():
    with TestClient(app) as client:
        response = client.get('/')
        assert 200 == response.status_code, f'Entrypoint test failed: {response.status_code}'


def test_healthpoint():
    with TestClient(app) as client:
        response = client.get('/health')
        assert 200 == response.status_code, f'Healthtest test failed: {response.status_code}'
        assert response.json() is True, f'Bad response: {response.json()}'
