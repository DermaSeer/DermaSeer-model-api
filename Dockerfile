FROM python:3.12.7-slim

WORKDIR /app

COPY requirements.txt /app/

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY . /app/

CMD ["python", "app.py"]