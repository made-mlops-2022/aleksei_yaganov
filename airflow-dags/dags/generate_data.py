from datetime import timedelta

from airflow import DAG
from airflow.providers.docker.operators.docker import DockerOperator
from airflow.utils.dates import days_ago
from docker.types import Mount

default_args = {
    "owner": "airflow",
    "email": ["airflow@example.com"],
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}

HOST_DIR = r"/Users/skienbear/Desktop/Made/mlops/hw1/project1/airflow-dags/data"
DATA_RAW_PATH = "/data/raw/{{ ds }}"


with DAG(
    "generate_data",
    default_args=default_args,
    schedule_interval="@daily",
    start_date=days_ago(5),
) as dag:
    mount = Mount(source=HOST_DIR, target="/data", type='bind')
    generate = DockerOperator(
        image="airflow-generate",
        command=f"-s {DATA_RAW_PATH}",
        network_mode="bridge",
        task_id="docker-airflow-generate",
        do_xcom_push=False,
        mount_tmp_dir=False,
        mounts=[mount]
    )

    generate