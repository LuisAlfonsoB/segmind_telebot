FROM python:3.8

WORKDIR /segmind_telebot

COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "main.py"]
