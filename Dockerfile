FROM python:3.6

WORKDIR /app

COPY automate.py .
COPY secrets.py .
COPY client_secret.json .
COPY requirements.txt .
RUN pip3 install -r requirements.txt

CMD [ "python3", "-u", "automate.py" ]