FROM python:3.10-slim
WORKDIR /app
RUN pip install --no-cache-dir kafka-python opencv-python-headless
COPY camera_server.py .
CMD ["python", "camera_server.py"]
