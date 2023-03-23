FROM python:latest

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt
RUN python -m pip install python-dotenv

COPY . /app

EXPOSE 8000

