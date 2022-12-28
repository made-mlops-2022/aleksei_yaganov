MLOPS HW2

Build docker image:
~~~
docker build -t aleksei_yaganov_online_inference:latest .
~~~
Публикация докера:
~~~
docker push skienbear/aleksei_yaganov_online_inference:latest
~~~
Загрузка докер образа:
~~~
docker pull skienbear/aleksei_yaganov_online_inference:latest
~~~
Запуск контейнера:
~~~
docker run -p 8000:8000 aleksei_yaganov_online_inference:latest
~~~
Запуск сервиса:
~~~
python make_request.py
~~~
Тестирование:
~~~
pytest tests/test.py
~~~

В качестве s3 хранилища использовал Minio для хранения данных и модели, развернутый локально.