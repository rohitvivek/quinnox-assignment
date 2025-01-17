# README

## Getting Started

### 1. Clone the Repository
To begin, clone the repository to your local machine:

```bash
git clone <repository-link>
cd <repository-folder>
```

### 2. Start Services with Docker Compose
Run the following command to start all required services:

```bash
docker-compose up
```

### 3. Populate the SQS Queue with Sample Data
Use the provided Python script to send messages to the Localstack SQS queue:

```bash
python scripts/populate_sqs.py
```

### 4. Verify the Worker Processes Messages
The worker service automatically reads messages from the SQS queue, processes them, and updates Redis.

### 5. Test the API Endpoints
Verify functionality by testing the following API endpoints:

- **User Stats Endpoint:**

  ```bash
  curl http://localhost:8000/users/U5678/stats
  ```

- **Global Stats Endpoint:**

  ```bash
  curl http://localhost:8000/stats/global
  ```

### 6. Block Diagram
![image](https://github.com/user-attachments/assets/68ae9217-2f48-4867-8ac8-4b0c4fab7135)

Description of the Flow

1. **SQS to Consumer:** Messages are published to the SQS queue, and the Python-based SQS consumer reads and processes them.
2. **Consumer to Redis:** Validated and aggregated data is stored in Redis for user-specific and global statistics.
3. **Redis Interaction:** Redis serves as the data cache, interacting with the consumer and API.
4. **FastAPI and User:** The FastAPI service exposes REST endpoints to retrieve data from Redis for users and global statistics.


