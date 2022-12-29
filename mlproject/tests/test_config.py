import os

from pytest import fixture
# from os.path import curdir

@fixture
def dataset_path():
    curdir = os.path.dirname(__file__)
    return os.path.join(curdir, "fake_dataset.csv")



@fixture
def target_col():
    return "condition"


@fixture
def categorical_features() -> list[str]:
    return [
        "sex",
        "cp",
        "fbs",
        "restecg",
        "exang",
        "slope",
        "ca",
        "thal",
    ]


@fixture
def numerical_features() -> list[str]:
    return [
        "age",
        "trestbps",
        "chol",
        "thalach",
        "oldpeak",
    ]


@fixture
def features_to_drop() -> list[str]:
    return [""]