#!/bin/python3
from kafka import KafkaProducer
from faker import Faker
import json
import random

fake = Faker()

producer = KafkaProducer(
    bootstrap_servers=['localhost:9092'],
    value_serializer=lambda m: json.dumps(m).encode('ascii')
)

def send_message(topic, message):
    try:
        producer.send(topic, message.encode('utf-8'))
        producer.flush()
        print('Message successfully written to Kafka topic.')
    except KafkaError as e:
        print(f'Failed to write message to Kafka topic: {e}')
    finally:
        producer.close()

def generate_ip_address():
    """
    Generates a random IP address using Faker.
    """
    return fake.ipv4()

def generate_traffic():
    """
    Generates a random internet traffic record using Faker.
    """
    o = {}
    o['source_ip'] = generate_ip_address()
    o['destination_ip'] = generate_ip_address()
    o['bytes_sent'] = random.randint(1000, 1000000)
    o['timestamp'] = fake.date_time_this_month(before_now=True, after_now=False).strftime("%Y-%m-%d %H:%M:%S")
    o['tcp_flags_ack'] = 0
    o['tcp_flags_reset'] = 0
    return o

def main():
    # Generate 10 random internet traffic records
    while True:
        record = generate_traffic()
        #send_message("traffic", record)
        print(record)

if __name__ == "__main__":
    main()
