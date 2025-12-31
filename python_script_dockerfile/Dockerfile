FROM python:3.10-slim

WORKDIR /app
COPY train_mnist.py /app/train_mnist.py

RUN pip install --no-cache-dir torch torchvision numpy

ENTRYPOINT ["python3", "/app/train_mnist.py"]
