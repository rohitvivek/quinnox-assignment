FROM python:3.9-slim
WORKDIR /home/rohit/quin-assignment/worker
COPY . /home/rohit/quin-assignment/worker
RUN pip install --no-cache-dir boto3 redis
CMD ["python", "main.py"]

