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
    "retries": 2,
    "retry_delay": timedelta(minutes=5),
}

HOST_DIR = r"Users\skienbear\Desktop\Made\mlops\hw1\project1\airflow-dags\data"
GENERATED_DATA_PATH = "/data/raw/{{ ds }}"
DATA_PREPROCESS_PATH = "/data/processed/{{ ds }}"
DATA_SPLIT_PATH = "/data/split/{{ ds }}"
MODEL_PATH = "/data/models/{{ ds }}"

with DAG(
    "train",
    default_args=default_args,
    schedule_interval="@weekly",
    start_date=days_ago(10),
) as dag:
    data_sensor = FileSensor(
        task_id="data_sensor",
        poke_interval=10,
        retries=100,
        filepath="/opt/airflow/data/raw/{{ ds }}"
    )

    preprocess = DockerOperator(
        image="airflow-preprocess",
        command=f"-l {GENERATED_DATA_PATH} -s {DATA_PREPROCESS_PATH} -t {MODEL_PATH}",
        # docker_url='unix://var/run/docker.sock',
        task_id="airflow-preprocess",
        do_xcom_push=False,
        mount_tmp_dir=False,
        mounts=[Mount(source=HOST_DIR, target="/data", type='bind')]
    )

    split = DockerOperator(
        image="airflow-split",
        command=f"-l {DATA_PREPROCESS_PATH} -s {DATA_SPLIT_PATH}",
        # docker_url='unix://var/run/docker.sock',
        task_id="split",
        do_xcom_push=False,
        mount_tmp_dir=False,
        mounts=[Mount(source=HOST_DIR, target="/data", type='bind')]
    )

    train = DockerOperator(
        image="airflow-train",
        command=f"-l {DATA_SPLIT_PATH} -m {MODEL_PATH}",
        # docker_url='unix://var/run/docker.sock',
        task_id="train",
        do_xcom_push=False,
        mount_tmp_dir=False,
        mounts=[Mount(source=HOST_DIR, target="/data", type='bind')]
    )

    validation = DockerOperator(
        image="airflow-validation",
        command=f"-l {DATA_SPLIT_PATH} -m {MODEL_PATH}",
        # docker_url='unix://var/run/docker.sock',
        task_id="validation",
        do_xcom_push=False,
        mount_tmp_dir=False,
        mounts=[Mount(source=HOST_DIR, target="/data", type='bind')]
    )

    data_sensor >> preprocess >> split >> train >> validation