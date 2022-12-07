FROM python:3.9.4-buster

RUN mkdir app

WORKDIR .


COPY ./ ./

RUN pip install -r requirements.txt


ENV PATH_TO_MODEL="model.pkl"

ENV PATH_TO_DATA="heart_cleveland_upload.csv"

ENV OUTPUT="predicts/output.csv"

ENV S3_BUCKET="data"

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]