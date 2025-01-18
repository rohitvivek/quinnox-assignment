import boto3
import json
import redis
from botocore.config import Config
import config
from etl_testing import Logger
from datetime import datetime
from apscheduler.schedulers.blocking import BlockingScheduler


class Test:
    def __init__(self, queue_url, sqs_client, redis_client):
        self.redis_client = redis_client
        self.sqs_client = sqs_client
        self.queue_url = queue_url

    def get_data(self):
        """
        Consume messages from the SQS queue.
        """
        try:
            response = self.sqs_client.receive_message(QueueUrl=self.queue_url, MaxNumberOfMessages=10,
                                                       WaitTimeSeconds=5)
            for message in response.get("Messages", []):
                order = json.loads(message["Body"])
                if self.transform_validate(order):
                    self.load(order)
                else:
                    logger.log(f"Invalid order skipped: {order}", level=logger.ERROR, exception=True)
                self.sqs_client.delete_message(QueueUrl=self.queue_url, ReceiptHandle=message["ReceiptHandle"])
        except Exception as e:
            logger.log(f"Error processing message: {e}", level=logger.ERROR, exception=True)

    def transform_validate(self, order):
        """
        Validate the order data.
        :param order:Dictionary containing info for each order placed by a user
        :type order:Dict
        :return:Validates the order_value against total_calculated & return a boolean value
        :rtype:Boolean
        """
        try:
            # check required fields are present/not
            assert all(k in order for k in ["user_id", "order_id", "order_value", "items"])

            # type casting
            order['order_value'] = None if order.get('order_value') is None else float(order.get('order_value'))
        
            # check that order_value equals the sum of (quantity * price_per_unit)
            total_calculated = sum(
                item["quantity"] * item["price_per_unit"] for item in order["items"]
            )
            # Validate & corrects the order_value
            if total_calculated != order.get("order_value"):
                order['order_value'] = total_calculated
            return True

        except (AssertionError, ValueError) as e:
            logger.log(f"Error validating the order: {e}", level=logger.ERROR, exception=True)
            return False

    def load(self, order):
        """
        Loads Redis with order data.
        :param order:Dictionary containing info for each order placed by a user
        :type order:Dict
        """

        user_key = f"user:{order.get('user_id')}"
        global_key = "global:stats"

        # Update user-level stats
        self.redis_client.hincrby(user_key, "order_count", 1)
        self.redis_client.hincrbyfloat(user_key, "total_spend", order.get("order_value"))

        # Update global stats
        self.redis_client.hincrby(global_key, "total_orders", 1)
        self.redis_client.hincrbyfloat(global_key, "total_revenue", order.get("order_value"))

        # Get the order by date
        order_date = datetime.strptime(order['order_timestamp'], "%Y-%m-%dT%H:%M:%SZ")
        dt = f"{order_date.year}:{order_date.month:02d}"

        # User-level monthly stats
        user_date_key = f"{user_key}:{dt}"
        logger.log(f"{user_date_key}", level=logger.DEBUG, exception=True)
        self.redis_client.hincrby(user_date_key, "order_count", 1)
        self.redis_client.hincrbyfloat(user_date_key, "total_spend", order["order_value"])


if __name__ == "__main__":
    config = config.load_config()
    aws_access_key_id = config.get("access_key")
    aws_secret_access_key = config.get("secret_key")
    local_stack_endpoint = config.get("sqs_endpoint_url")
    redis_host = config.get("redis_host")
    redis_port = config.get("redis_port")
    local_stack_queue = config.get("sqs_queue_name")
    local_stack_region = config.get("sqs_region_name")

    # logger
    logger = Logger(threshold_level=Logger.DEBUG)

    # Initialize SQS and Redis
    sqs_client = boto3.client("sqs", endpoint_url=local_stack_endpoint, config=Config(region_name=local_stack_region),
                              aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key)
    redis_client = redis.StrictRedis(host=redis_host, port=redis_port, decode_responses=True)
    queue_url = sqs_client.create_queue(QueueName=local_stack_queue)["QueueUrl"]
    etl_test = Test(queue_url, sqs_client, redis_client)

    sched = BlockingScheduler()
    sched.add_job(etl_test.get_data, "interval", seconds=3)
    sched.start()
