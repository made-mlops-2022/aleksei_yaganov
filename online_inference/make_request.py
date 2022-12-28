import pickle
import os

import click
import numpy as np
import pandas as pd
from sklearn.pipeline import Pipeline
from boto3 import client


def load_object(path: str) -> Pipeline:
    with open(path, "rb") as f:
        return pickle.load(f)


def load_data(s3_bucket: str, remote_path: str, local_path: str):
    s3 = client("s3", aws_access_key_id="admin",
                aws_secret_access_key="password",
                endpoint_url="http://127.0.0.0:9000",
                secure="False", region_name='us-east-1')

    s3.download_file(s3_bucket, remote_path, local_path)


def upload_predictions(s3_bucket: str, local_path: str, s3_path: str):
    s3 = client("s3", aws_access_key_id="admin", aws_secret_access_key="password",
                endpoint_url="http:127.0.0.0:9000", secure="False", region_name='us-east-1')
    s3.upload_file(local_path, s3_bucket, s3_path)


def batch_predict(
        s3_bucket: str,
        path_to_data: str,
        remote_model_path: str,
        output: str,
        local_output: str = "./predicts/predict.csv",
        local_model_path: str = "./model/model.pkl",
        local_data_path: str = "./data/heart_cleveland_upload.csv",
):
    load_data(s3_bucket, remote_model_path, local_model_path)
    load_data(s3_bucket, path_to_data, local_data_path)

    model = load_object(local_model_path)
    data = pd.read_csv(local_data_path)
    ids = data["Id"]

    predicts = np.exp(model.predict(data))
    predict_df = pd.DataFrame(list(zip(ids, predicts)), columns=["Id", "Predict"])
    predict_df.to_csv(local_output, output)


@click.command(name="batch_predict")
@click.argument("PATH_TO_DATA", default=os.getenv("PATH_TO_DATA"))
@click.argument("PATH_TO_MODEL", default=os.getenv("PATH_TO_MODEL"))
@click.argument("OUTPUT", default=os.getenv("OUTPUT"))
@click.argument("S3_BUCKET", default=os.getenv("S3_BUCKET"))
def batch_predict_command(
        path_to_data: str, path_to_model: str, output: str, s3_bucket: str
):
    batch_predict(s3_bucket, path_to_data, path_to_model, output)


if __name__ == "__main__":
    batch_predict_command()
