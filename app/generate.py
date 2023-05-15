from kafka import KafkaProducer
from kafka.errors import KafkaError, NoBrokersAvailable, NodeNotReadyError
from kafka.admin import KafkaAdminClient, NewTopic
from faker import Faker
import json
import random
import time
import os
from random import choice

bootstrap_servers = os.environ.get('KAFKA_BOOTSTRAP_SERVERS')
topic_name = os.environ.get('KAFKA_TOPIC_NAME')
topic_config =  {'retention.ms': str(os.environ.get('KAFKA_TOPIC_RETENTION_MS'))}
num_partitions = 1
replication_factor = 1

fake = Faker()

def wait_for_kafka(bootstrap_servers):
    while True:
        try:
            admin_client = KafkaAdminClient(bootstrap_servers=bootstrap_servers)
            print('Kafka broker is available')
            break
        except NodeNotReadyError:
            print('Waiting for node to become available...')
            time.sleep(1)

def create_topic_if_not_exists():
    try:
        admin_client = KafkaAdminClient(bootstrap_servers=bootstrap_servers)
        topic_list = admin_client.list_topics()
        if topic_name not in topic_list:
            topic = NewTopic(name=topic_name, num_partitions=num_partitions, replication_factor=replication_factor, topic_configs=topic_config)
            admin_client.create_topics(new_topics=[topic], validate_only=False)
            print(f'Created topic: {topic_name}')
        admin_client.close()
    except Exception as e:
        print(e)
    except NodeNotReadyError:
        print("Node is not ready yet")

def generate_traffic():
    """
    Generates a random internet traffic record using Faker.
    """
    flags = [0, 1, 1]  # bias towards slowloris style attacks 
    o = {}
    o['bytes_sent'] = random.randint(1000, 1000000)
    o['timestamp'] = fake.date_time_this_month(before_now=True, after_now=False).strftime("%Y-%m-%d %H:%M:%S")
    o['ip'] = {}
    o['ip']['source_ip'] = fake.ipv4() 
    o['ip']['dest_ip'] = "10.1.1.{}".format(random.randint(1, 255)) 
    o['flags'] = {}
    o['flags']['tcp_flags_ack'] = choice(flags)
    o['flags']['tcp_flags_reset'] = choice(flags)
    return o

def generate_bad_user_login():
    """
    Generates a login attempt
    """
    users = ['Postgres', 'MySQL', 'FTPUser', 'Root', 'smbuser', 'ubuntu']
    o = {}
    o['msg'] = "Invalid user login attempt: {}".format(choice(users))
    o['port'] = fake.port_number()
    o['ip'] = {}
    o['ip']['source_ip'] = fake.ipv4() 
    o['ip']['dest_ip'] = "10.1.1.{}".format(random.randint(1, 255))
    return o

def generate_bad_password_attempt():
    """
    Generate a bad password attempt
    """
    users = ['Postgres', 'MySQL', 'FTPUser', 'Root', 'smbuser', 'ubuntu']
    o = {}
    o['msg'] = "Bad password for user: {}".format(choice(users))
    o['port'] = fake.port_number()
    o['ip'] = {}
    o['ip']['source_ip'] = fake.ipv4() 
    o['ip']['dest_ip'] = "10.1.1.{}".format(random.randint(1, 255)) 
    return o 

def main():
    wait_for_kafka(bootstrap_servers)
    create_topic_if_not_exists()
    producer = KafkaProducer(
                bootstrap_servers=bootstrap_servers,
                value_serializer=lambda m: json.dumps(m).encode('ascii')
    )
    while True:
        fns = [generate_traffic, 
               generate_bad_user_login, 
               generate_bad_password_attempt,
               generate_traffic,
               generate_traffic,
               generate_traffic,
               generate_traffic]
        record = choice(fns)()
        try:
            producer.send(topic_name, record)
            producer.flush()
            print(f'Message successfully written to Kafka topic.')
        except NoBrokersAvailable:
            print(f'No brokers available. Waiting...')
            time.sleep(5)
        time.sleep(1)  

if __name__ == "__main__":
    main()
