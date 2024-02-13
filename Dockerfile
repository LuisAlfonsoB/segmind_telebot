FROM python:3.8

WORKDIR /segmind_telebot

RUN pip install -r requirements.txt

CMD ["python", "main.py"]
