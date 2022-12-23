import os
from datetime import timedelta

from airflow import DAG
from airflow.providers.docker.operators.docker import DockerOperator
from airflow.sensors.filesystem import FileSensor
from airflow.utils.dates import days_ago
from docker.types import Mount

default_args = {
    "owner": "airflow",
    "email": ["airflow@example.com"],
    "retries": 1,
    "retry_delay": timedelta(minutes=1),
}

HOST_DIR = r"Users\skienbear\Desktop\Made\mlops\hw1\project1\airflow-dags\data"
DATA_RAW_PATH = "/data/raw/{{ ds }}"
PREDICTIONS_PATH = "/data/predictions/{{ ds }}"

MODEL_PATH = "/data/models/2022-12-08"

with DAG(
        "predict",
        default_args=default_args,
        schedule_interval="@daily",
        start_date=days_ago(5),
) as dag:
    data_sensor = FileSensor(
        task_id="data_sensor",
        poke_interval=10,
        retries=100,
        filepath="/opt/airflow/data/raw/{{ ds }}"
    )


    predict = DockerOperator(
        image="airflow-predict",
        command=f"-l {DATA_RAW_PATH} -m {MODEL_PATH} -s {PREDICTIONS_PATH}",
        # docker_url='unix://var/run/docker.sock',
        task_id="airflow-predict",
        do_xcom_push=False,
        mount_tmp_dir=False,
        mounts=[Mount(source=HOST_DIR, target="/data", type='bind')]
    )

    data_sensor >> predict