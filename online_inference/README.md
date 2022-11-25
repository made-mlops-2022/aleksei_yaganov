MLOPS HW2

Build docker image:

docker build -t aleksei_yaganov/online_inference:latest .

Публикация докера:

docker push skienbear/aleksei_yaganov_online_inference:latest

Загрузка докер образа:

docker pull aleksei_yaganov/online_inference:latest

Запуск контейнера:

docker run -p 8000:8000 aleksei_yaganov/online_inference:latest

Запуск сервиса:

python request.py

Тесты:

pytest tests/test.py