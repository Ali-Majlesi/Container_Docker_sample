FROM python:3.9

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY http_server.py .

EXPOSE 8000

CMD ["python", "http_server.py"]

