FROM python:3.6

RUN pip install spotipy

WORKDIR /app

COPY app/main.py .
COPY env.py .
# RUN pip install -r requirements.txt

CMD [ "python", "-u", "main.py" ]