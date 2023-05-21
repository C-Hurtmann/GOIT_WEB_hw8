import pika
from faker import Faker
import os
import sys
import random
import json

root_folder = os.path.abspath(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(root_folder)

import part_1.connection
from part_2.model_contacts import Contacts


credentials = pika.PlainCredentials('guest', 'guest')
connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost', port=5672, credentials=credentials))
channel = connection.channel()

channel.exchange_declare(exchange='main', exchange_type='direct')
channel.queue_declare(queue='for_sms', durable=True)
channel.queue_declare(queue='for_email', durable=True)

channel.queue_bind(exchange='main', queue='for_sms')
channel.queue_bind(exchange='main', queue='for_email')


def generate_random_document() -> str:
    fake = Faker()

    fullname = fake.name()
    email = fake.email()
    address = fake.address()
    phone = fake.phone_number()
    how_to_contact = random.choice(('sms', 'email'))
    doc = Contacts(fullname=fullname,
                   email=email,
                   address=address,
                   phone=phone,
                   how_to_contact=how_to_contact)
    doc.save()
    return doc

def run_producer(times: int = 1) -> None:
    for _ in range(times):
        doc = generate_random_document()
        queue = doc.how_to_contact
        message = doc.to_json()
        channel.basic_publish(exchange='main', routing_key=f'for_{queue}', body=json.dumps(message),
                              properties=pika.BasicProperties(delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE))
    print(f" [x] Sent to {queue}")
    connection.close()


if __name__ == '__main__':
    run_producer()
