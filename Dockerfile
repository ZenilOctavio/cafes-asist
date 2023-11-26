FROM python:3.11
WORKDIR /project
COPY ./app /project

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

WORKDIR /project/app
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8181"]