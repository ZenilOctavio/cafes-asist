FROM python:3.11
WORKDIR /project
COPY . /project

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

CMD ["uvicorn main:app", "--port 80"]