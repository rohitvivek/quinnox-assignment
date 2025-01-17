import boto3
import json

# Configure the SQS client with Localstack endpoint and dummy credentials
sqs_client = boto3.client(
    "sqs",
    endpoint_url="http://localhost:4566/",  # Localstack endpoint
    region_name="us-east-1",               # Specify region
    aws_access_key_id="dummy",            # Dummy access key
    aws_secret_access_key="dummy"         # Dummy secret key
)

# Fetch or create the queue
queue_name = "order-events"
queue_url = sqs_client.create_queue(QueueName=queue_name)["QueueUrl"]

# Sample orders
orders = [
    {
        "order_id": "ORD1234",
        "user_id": "U5678",
        "order_value": 99.99,
        "items": [
            {"product_id": "P001", "quantity": 2, "price_per_unit": 20.00},
            {"product_id": "P002", "quantity": 1, "price_per_unit": 59.99},
        ],
        "shipping_address": "123 Main St, Springfield",
        "payment_method": "CreditCard"
    },
    {
        "order_id": "ORD1235",
        "user_id": "U1234",
        "order_value": 49.99,
        "items": [
            {"product_id": "P003", "quantity": 1, "price_per_unit": 49.99},
        ],
        "shipping_address": "MF 17 BTM",
        "payment_method": "COD"
    },
      {
        "order_id": "ORD1236",
        "user_id": "U1233",
        "order_value": 49.99,
        "items": [
            {"product_id": "P003", "quantity": 1, "price_per_unit": 49.99},
        ],
        "shipping_address": "MF 17 BTM",
        "payment_method": "CreditCard"
    },
]

# Populate the queue
for order in orders:
    sqs_client.send_message(QueueUrl=queue_url, MessageBody=json.dumps(order))
    print(f"Sent order to SQS: {order['order_id']}")

