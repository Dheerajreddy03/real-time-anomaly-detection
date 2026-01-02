import json
import time
import random
from datetime import datetime
from kafka import KafkaProducer

producer = KafkaProducer(
    bootstrap_servers="kafka:9092",
    api_version=(3, 5, 0),           # 🔑 FIX: explicit API version
    value_serializer=lambda v: json.dumps(v).encode("utf-8"),
    request_timeout_ms=20000,
    retries=5
)

print("Kafka producer started...")

topic = "sensor-data"

while True:
    data = {
        "sensor_id": random.randint(1, 5),
        "temperature": round(random.uniform(20, 60), 2),
        "pressure": round(random.uniform(80, 140), 2),
        "timestamp": datetime.utcnow().isoformat()
    }

    producer.send(topic, data)
    producer.flush()
    print("Sent:", data)
    time.sleep(2)
