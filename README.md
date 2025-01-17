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

### 6. Publish the Assignment on GitHub
To complete the assignment:

1. Ensure the repository is public and includes:
   - Full source code.
   - `docker-compose.yml`.
   - Scripts for populating the SQS queue.
   - This detailed `README.md` file.

2. Share the repository link in your assignment reply email.

