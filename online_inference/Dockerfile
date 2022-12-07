FROM python:3.9.4-buster

RUN mkdir app

WORKDIR .

#COPY requirements.txt requirements.txt

COPY ./ ./

RUN pip install -r requirements.txt

#COPY make_request.py make_request.py

#RUN pip install --no-cache-dir --upgrade -r requirements.txt

ENV PATH_TO_MODEL="model.pkl"

ENV PATH_TO_DATA="heart_cleveland_upload.csv"

ENV OUTPUT="predicts/output.csv"

ENV S3_BUCKET="data"

EXPOSE 8000

#CMD ["python", "make_request.py"]

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]