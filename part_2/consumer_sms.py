import pika
from model_contacts import Contacts
import time
import json
import os
import sys

root_folder = os.path.abspath(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(root_folder)

import part_1.connection


credentials = pika.PlainCredentials('guest', 'guest')
connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost', port=5672, credentials=credentials))
channel = connection.channel()

channel.queue_declare(queue='for_sms', durable=True)
print(' [*] SMS consumer activated.\nWaiting for messages. To exit press CTRL+C')


def callback(ch, method, properties, body):
    json_obj = json.loads(body)
    doc = Contacts.from_json(json_obj)
    print(f" [x] Received {doc.id} - {doc.fullname}")
    time.sleep(1)
    doc.sent_message = True
    doc.save()
    print(f" [x] Done: {method.delivery_tag}")
    ch.basic_ack(delivery_tag=method.delivery_tag)


channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue='for_sms', on_message_callback=callback)


if __name__ == '__main__':
    channel.start_consuming()