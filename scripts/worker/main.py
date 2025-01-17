import boto3
import json
import redis
from botocore.config import Config


class Test:
    def __init__(self, queue_url, sqs_client, redis_client):
        self.redis_client = redis_client
        self.sqs_client = sqs_client
        self.queue_url = queue_url

    def process_message(self, message_body):
        """Process individual messages.
        :param message_body:
        :type message_body:
        :rtype: None
        """
        try:
            order = json.loads(message_body)
            print(order)
            if self.transform_validate(order):
                self.load(order)
            else:
                print(f"Invalid order skipped: {order}")
        except Exception as e:
            print(f"Error processing message: {e}")

    def get_data(self):
        """
        Consume messages from the SQS queue.
        """
        while True:
            print("entry 1")
            response = self.sqs_client.receive_message(QueueUrl=self.queue_url, MaxNumberOfMessages=10, WaitTimeSeconds=5)
            print("entry 2")

            for message in response.get("Messages", []):
                print("entry 3")

                self.process_message(message["Body"])
                self.sqs_client .delete_message(QueueUrl= self.queue_url, ReceiptHandle=message["ReceiptHandle"])

    def transform_validate(self, order):
        """
        Validate the order data.
        :param order:
        :type order:
        :return:
        :rtype:
        """
        try:
            # check required fields are present/not
            assert all(k in order for k in ["user_id", "order_id", "order_value", "items"])

            # check that order_value equals the sum of (quantity * price_per_unit)Validate order_value matches items' total
            total_calculated = sum(
                item["quantity"] * item["price_per_unit"] for item in order["items"]
            )
            if abs(total_calculated - order["order_value"]) > 0.01:
                raise ValueError("Order value mismatch.")
            return True
        except (AssertionError, ValueError):
            return False

    def load(self, order):
        """
        Loads Redis with order data.
        :param order:
        :type order:
        """
        """"""
        user_key = f"user:{order['user_id']}"
        global_key = "global:stats"

        # Update user-level stats
        self.redis_client .hincrby(user_key, "order_count", 1)
        self.redis_client .hincrbyfloat(user_key, "total_spend", order["order_value"])

        # Update global stats
        self.redis_client .hincrby(global_key, "total_orders", 1)
        self.redis_client .hincrbyfloat(global_key, "total_revenue", order["order_value"])


if __name__ == "__main__":
    # Initialize SQS and Redis
    sqs_client = boto3.client("sqs", endpoint_url="http://localstack:4566/", config=Config(region_name="us-east-1"),aws_access_key_id="dummy", aws_secret_access_key="dummy")
    redis_client = redis.StrictRedis(host="redis", port=6379, decode_responses=True)
    queue_url = sqs_client.create_queue(QueueName="order-events")["QueueUrl"]
    etl_test = Test(queue_url, sqs_client, redis_client)
    etl_test.get_data()
