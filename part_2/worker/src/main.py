import time
import json
import boto3
import heapq
from collections import defaultdict
import logging
from src.aws import get_sqs_client, get_s3_client
from src.config import get_config
from botocore.exceptions import ClientError

logger = logging.getLogger(__name__)


def read_csv(debts: str) -> list:
    data = []
    for row in debts.split("\n")[:-1]:
        debtor, creditor, amount = row.split(",")
        data.append((debtor, creditor, int(amount)))
    return data


def download_debts(debts_id: str) -> str:
    config = get_config()
    s3_client = get_s3_client()

    try:
        response = s3_client.get_object(
            Bucket=config.debts_bucket_name,
            Key=debts_id,
        )
        print(f"Downloaded debts {debts_id} from S3")
        return response["Body"].read().decode("utf-8")
    except ClientError as error:
        logger.exception(f"Couldn't download debts {debts_id} from S3")
        raise error


def process_debts():
    config = get_config()
    sqs_client = get_sqs_client()
    s3_client = get_s3_client()

    try:
        response = sqs_client.receive_message(
            QueueUrl=config.worker_queue_url,
            MaxNumberOfMessages=10,
            WaitTimeSeconds=5,
        )
        for msg in response.get("Messages", []):
            print("Received message: %s: %s", msg["MessageId"], msg["Body"])
            msg_body = json.loads(msg["Body"])
            debts_id = msg_body["debts_id"]
            debts = download_debts(debts_id)
            debts = read_csv(debts)

            optimized_transactions = simplify_debts(debts)

            output = "\n".join([",".join(map(str, row)) for row in optimized_transactions])
            s3_client.put_object(
                Bucket=config.debts_bucket_name,
                Key=f"{debts_id}_results",
                Body=output,
            )

    except:
        logger.exception("Couldn't receive messages from queue")


def simplify_debts(transactions):
    total = defaultdict(int)

    for giver, receiver, amount in transactions:
        total[giver] -= amount
        total[receiver] += amount

    credit = []
    debit = []

    for name, amount in total.items():
        # if amount is positive, append to credit else append to debit
        if amount > 0:
            credit.append((-amount, name))
        if amount < 0:
            debit.append((amount, name))

    heapq.heapify(credit)
    heapq.heapify(debit)
    answer = []

    while credit and debit:
        # pop the smallest value from credit and debit
        credit_value, credit_name = heapq.heappop(credit)
        debit_value, debit_name = heapq.heappop(debit)

        if credit_value < debit_value:
            # if credit value is smaller than debit value, append the credit value to answer
            amount_left = credit_value - debit_value
            answer.append((credit_name, debit_name, -1 * debit_value))
            heapq.heappush(credit, (amount_left, credit_name))

        elif debit_value < credit_value:
            # if debit value is smaller than credit value, append the debit value to answer
            amount_left = debit_value - credit_value
            answer.append((credit_name, debit_name, -1 * credit_value))
            heapq.heappush(debit, (amount_left, debit_name))

        else:
            answer.append((credit_name, debit_name, -1 * credit_value))

    return answer


if __name__ == "__main__":
    while True:
        process_debts()
