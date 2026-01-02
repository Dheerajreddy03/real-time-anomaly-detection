# Real-Time Anomaly Detection System

## Project Overview

This project demonstrates a **real-time data processing pipeline** that detects anomalies from continuously generated sensor data.
The system streams data using **Kafka**, processes it in real time with **Apache Spark Structured Streaming**, and stores the processed results in **Elasticsearch** for fast querying and visualization.

The goal of this project is to show how large-scale streaming systems work together to handle live data and identify abnormal patterns instantly.

---

## What Problem This Project Solves

In real-world systems like IoT devices, monitoring systems, or industrial sensors:

* Data arrives continuously
* Immediate detection of abnormal values is critical
* Batch processing is too slow

This project solves that by:

* Processing data **as it arrives**
* Detecting anomalies **in real time**
* Making results immediately searchable

---

## Technologies Used (with purpose)

### Docker & Docker Compose

* Used to run all services in isolated containers
* Ensures consistent setup across systems

### Apache Kafka

* Acts as the real-time data pipeline
* Receives continuous sensor data from the producer

### Apache Spark Structured Streaming

* Reads data from Kafka in real time
* Applies anomaly detection logic
* Sends processed data to Elasticsearch

### Elasticsearch

* Stores processed streaming data
* Enables fast search and analytics

### Kibana

* Used to visualize and explore anomaly data

### Python

* Kafka producer implementation
* Spark streaming logic

---

## 📂 Project Structure

```
real-time-anomaly-detection/
│
├── docker-compose.yml        # Infrastructure setup
├── producer/
│   └── sensor_producer.py   # Kafka data producer
├── spark/
│   └── spark_streaming_job.py  # Spark anomaly detection logic
└── README.md
```

---

## How the System Works (Flow)

1. A Python producer generates random sensor data
2. Data is sent to a Kafka topic
3. Spark reads the Kafka stream continuously
4. Spark checks each record for abnormal values
5. Results are written to Elasticsearch in real time
6. Data can be queried or visualized instantly

---

## Step-by-Step: How to Run the Project

### Step 1: Start Infrastructure

Run this command from the project directory:

```bash
docker compose up -d
```

This starts Kafka, Zookeeper, Spark, Elasticsearch, and Kibana.

---

### Step 2: Run Kafka Producer (keep terminal open)

Open a **new terminal**:

```bash
docker run --rm -it --network real-time-anomaly-detection_default \
 -v ${PWD}/producer:/app python:3.10 \
 bash -c "pip install kafka-python && python /app/sensor_producer.py"
```

You should see continuous output like:

```
Sent: {'sensor_id': 2, 'temperature': 45.6, ...}
```

---

### Step 3: Start Spark Streaming Job (new terminal)

```bash
docker exec -it spark /opt/spark/bin/spark-submit \
 --conf spark.jars.ivy=/tmp/.ivy \
 --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.3.3,\
org.elasticsearch:elasticsearch-spark-30_2.12:8.11.1 \
 /opt/spark/jobs/spark_streaming_job.py
```

Spark will continuously process incoming data.

---

### Step 4: Verify Data in Elasticsearch

```bash
Invoke-RestMethod http://localhost:9200/anomalies/_count
```

If the count increases, the pipeline is working correctly.

---

### Step 5: View Sample Records

```bash
Invoke-RestMethod http://localhost:9200/anomalies/_search?size=5 | ConvertTo-Json -Depth 10
```

---

## Anomaly Detection Logic

The system uses **rule-based detection**:

* If `temperature > 40` **OR**
* If `pressure > 120`

Then:

```
anomaly_score = 1.0
```

Otherwise:

```
anomaly_score = 0.0
```

This approach is simple, stable, and suitable for real-time streaming.

---

## Project Completion Criteria

The project is considered complete when:

* Kafka producer sends data continuously
* Spark job runs without interruption
* Elasticsearch index `anomalies` exists
* Document count increases in real time

---

## Possible Enhancements

* Add machine learning–based anomaly detection
* Create advanced Kibana dashboards
* Store historical trends
* Add alerting mechanisms

---

## Conclusion

This project successfully demonstrates a **scalable, real-time anomaly detection pipeline** using modern big-data technologies. It reflects real-world streaming architectures and is suitable for production-level concepts, interviews, and portfolio projects.
