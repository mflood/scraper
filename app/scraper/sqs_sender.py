"""
    send_sqs_messages.py

    Send messages from STDIN to sqa stream

    Usage:

        source venv/bin/activate
        # send messages we captured from staging to dev
        python send_sqs_messages.py -c dev.yml < bodies.staging

"""
import argparse
import logging
import os
import sys

import mylogging
import boto3
from scraper.aws_factory import build_sqs_client

DEFAULT_REGION_NAME = 'us-east-1'

def parse_args(argv=None):
    """
        Parse command line args
    """
    parser = argparse.ArgumentParser(description="Send message to SQS queue")

    parser.add_argument('-v', action="store_true", dest="verbose",
                        required=False,
                        help="Debug output")

    results = parser.parse_args(argv)
    return results


def send_queue_message(sqs_queue_url, message):
    logger = logging.getLogger(mylogging.LOGNAME)
    logger.debug("Sending message: %s", message)

    sqs_api = build_sqs_client()

    # Send message to SQS queue
    response = sqs_api.send_message(
        QueueUrl=sqs_queue_url,
        MessageBody=message
    )

    logger.debug(response)

def main(sqs_queue_url):
    """
        Main program
    """
    arg_object = parse_args()

    if arg_object.verbose:
        mylogging.init(loglevel=logging.DEBUG)
    else:
        mylogging.init(loglevel=logging.INFO)

    message = sys.stdin.readline().strip()
    send_queue_message(sqs_queue_url=sqs_queue_url, message=message)

if __name__ == "__main__":

    sqs_queue_url = os.getenv("SQS_QUEUE_URL")
    main(sqs_queue_url=sqs_queue_url)
