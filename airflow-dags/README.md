# airflow-examples
HW3 - Airflow

Для запуска необходимо перейти в папку airflow-ml-base:
~~~
cd images/airflow-ml-base
~~~
Собрать базовый образ:
~~~
docker build -t airflow-ml-base:latestst .cd images/airflow-ml-base
~~~

~~~
# для корректной работы с переменными, созданными из UI
export FERNET_KEY=$(python -c "from cryptography.fernet import Fernet; FERNET_KEY = Fernet.generate_key().decode(); print(FERNET_KEY)")```
docker compose up --build
~~~
Ссылка на документацию по docker compose up

https://docs.docker.com/compose/reference/up/
