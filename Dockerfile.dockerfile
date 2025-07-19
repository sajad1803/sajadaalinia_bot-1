FROM python:3.9-slim
WORKDIR /app
COPY . .
RUN pip install --upgrade pip && \
    pip install setuptools==68.2.2 && \
    pip install -r requirements.txt
CMD ["python", "main.py"]