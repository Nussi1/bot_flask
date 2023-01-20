FROM python:3.9-alphine

EXPOSE 5000/tcp

WORKDIR /app
COPY requirements.txt ./
RUN pip install --no-cache-dir requirements.txt
COPY . .

RUN rm -rf .env

CMD ["python", "./app.py"]