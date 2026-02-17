FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY ./myapi . 
EXPOSE 5000
# Al estar main.py en la raíz de /app, el comando debe ser main:app
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "5000", "--reload"]