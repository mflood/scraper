
"""
    sqs_processor.py

    read getstream events from SQS and dump into snowflake
"""
import logging
import os

import mylogging
from scraper.aws_factory import build_sqs_client
from scraper.sqs_message import SQSMessage

class SqsReader():
    """
        Read a message from SQS
    """

    def __init__(self, sqs_queue_url, sqs_client):

        self._sqs_api = sqs_client
        self._sqs_queue_url = sqs_queue_url
        self._logger = logging.getLogger('aaptiv')
        self._visibility_timeout_seconds = 20
        self._max_messages_per_read = 10
        self._skip_delete = False

        assert 1 <= self._max_messages_per_read <= 10

    def num_messages_in_queue(self):
        """
            Reads the SQS Queue Metadata to see if there are messages to process
            The api call returns the number of messages in the queue
        """
        response = self._sqs_api.get_queue_attributes(
            QueueUrl=self._sqs_queue_url,
            AttributeNames=[
                'All'
            ]
        )

        approximate_count = int(response['Attributes']['ApproximateNumberOfMessages'])
        self._logger.debug("There are approximately %d messages in the queue", approximate_count)
        return approximate_count

    def _get_sqs_messages(self):
        """
            Makes an API call to SWS to grab up to 10 messages
            from the Queue
        """

        # Receive message from SQS queue
        self._logger.info("Hitting SQS Api to find up to 10 messages")
        response = self._sqs_api.receive_message(
            QueueUrl=self._sqs_queue_url,
            AttributeNames=[
                'All'
            ],

            # Max allowed is 10
            MaxNumberOfMessages=self._max_messages_per_read,
            MessageAttributeNames=[
                'All'
            ],
            # give ourselves 20 seconds to process the message
            VisibilityTimeout=self._visibility_timeout_seconds
        )

        response_code = response['ResponseMetadata']['HTTPStatusCode']
        if response_code != 200:
            raise Exception("bad response %s" % response)

        self._logger.debug("SQS Metatdata Response: %s", response)
        messages = response.get('Messages', [])

        #for message in response['Messages']:
        #    receipt_handle = message['ReceiptHandle']
        #    #print("Receipt handle: %s" % receipt_handle)
        #    print('Received message: %s' % message)

        return messages


    def delete(self, message):

        if self._skip_delete:
            self._logger.warning("SKIPPING Draining message %s", message['ReceiptHandle'])
            return

        self._logger.debug("Draining message %s", message['ReceiptHandle'])
        receipt_handle = message['ReceiptHandle']
        try:
            self._sqs_api.delete_message(
                QueueUrl=self._sqs_queue_url,
                ReceiptHandle=receipt_handle
            )
        except Exception as error:
            self._logger.error(error)
            raise

    def read_queue(self):
        """
            Look for a batch of work to do and do it
        """
        return_messages = []
        messages = self._get_sqs_messages()
        if messages:
            for message in messages:
#               sqs_message = SQSMessage(message)
                return_messages.append(message)
                #self._delete_message(message)

        return return_messages


if __name__ == "__main__":
    mylogging.init(loglevel=logging.DEBUG)
    sqs_queue_url = os.getenv("SQS_QUEUE_URL")
    reader = SqsReader(sqs_queue_url=sqs_queue_url, sqs_client=build_sqs_client())
    num = reader.num_messages_in_queue()
    print(num)
    messages = reader.read_queue()
    for m in messages:
        print("Message: {}".format(m))
        print("Body: {}".format(m['Body']))
        reader.delete(m)


# end
