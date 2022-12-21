FROM python:3.10.6-alpine3.16

WORKDIR /

RUN pip install --upgrade pip  

COPY . /

RUN pip install -r requirements.txt  

CMD ["python", "manage.py", "migrate"]

EXPOSE 8000

CMD ["python", "manage.py", "runserver","0.0.0.0:8000"]