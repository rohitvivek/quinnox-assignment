
FROM python:3.9-slim
WORKDIR /home/rohit/quin-assignment/web
COPY . /home/rohit/quin-assignment/web
RUN pip install --no-cache-dir fastapi uvicorn redis
EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

