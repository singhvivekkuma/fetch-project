from confluent_kafka import Consumer, Producer, KafkaError
import json
import datetime
import hashlib

# Kafka Consumer Configuration
consumer_config = {
    'bootstrap.servers': 'localhost:29092',
    'group.id': 'fetch-consumer-group',
    'auto.offset.reset': 'earliest'
}

# Kafka Producer Configuration
producer_config = {
    'bootstrap.servers': 'localhost:29092'
}

# Initialize Kafka Consumer and Producer 
consumer = Consumer(consumer_config)
producer = Producer(producer_config)

# Subscribe to the source topic
consumer.subscribe(['user-login'])

def process_message(data):
    """
    Process incoming kafka message and transform them before writing them to a new kafka topic
    """
    try:
        # Extract and process necessary fields
        user_id = data.get("user_id", "Unknown")
        device_type = data.get("device_type", "Unknown")
        app_version = data.get("app_version", "Unknown")
        ip_address = data.get("ip", "Unknown")
        locale = data.get("locale", "Unknown")
        device_id = data.get("device_id", "Unknown")
        timestamp = data.get("timestamp", "Unknown")

        # Convert timestamp to readable format
        readable_timestamp = datetime.datetime.fromtimestamp(int(timestamp), datetime.timezone.utc).strftime('%Y-%m-%d %H:%M:%S')

        # Hashing User ID for privacy and PII complience
        if user_id != "Unknown":  # Only hash if user_id is present
            hashed_user_id = hashlib.sha256(user_id.encode()).hexdigest()
        else:
            hashed_user_id = "Unknown"

        # Mask IP Address
        masked_ip = ".".join(ip_address.split(".")[:2]) + ".xxx.xxx"

        # Construct processed message
        processed_data = {
            "user_id": hashed_user_id,
            "device_type": device_type,
            "app_version": app_version,
            "ip": masked_ip,
            "locale": locale,
            "device_id": device_id,
            "timestamp": readable_timestamp
        }

        print(f"Processed Message: {json.dumps(processed_data, indent=2)}")
        return processed_data

    except Exception as e:
        print(f"Error processing message: {e}")
        return None
    
def publish_to_kafka(processed_data):
    """
    Publishes processed data to the 'processed-user-login' Kafka topic.
    """
    try:
        producer.produce("processed-user-login", json.dumps(processed_data))
        producer.flush()
        print(f"Published to 'processed-user-login': {json.dumps(processed_data)}")
    except Exception as e:
        print(f"Error publishing message: {e}")

try:
    while True:
        msg = consumer.poll(1.0)

        if msg is None:
            continue
        if msg.error():
            if msg.error().code() == KafkaError._PARTITION_EOF:
                continue
            else:
                print(f"Consumer Error: {msg.error()}")
                break

        data = json.loads(msg.value().decode('utf-8'))
        processed_data = process_message(data)
        if processed_data:
            publish_to_kafka(processed_data)

except KeyboardInterrupt:
    print("\nShutting down consumer...")

finally:
    consumer.close()

