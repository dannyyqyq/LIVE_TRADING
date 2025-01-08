# Kafka and quixstream
1. Kafka Topics = Pipes in QuixStreams
Kafka organizes streams of messages into topics. Think of topics as channels where data is published and subscribed to.
In QuixStreams, you work with pipes, which are like streams of data flowing between the application and storage or processing layers. QuixStreams hides the raw Kafka complexities behind a higher-level abstraction.
2. Kafka Producers and Consumers = QuixStreams Publishers and Subscribers
In Kafka, you write data to a topic using a producer and read data from a topic using a consumer.
QuixStreams provides similar functionality but simplifies the experience. You publish data to streams and subscribe to streams, but QuixStreams comes with built-in utilities like real-time processing and support for structured data via DataFrames.
3. Offset Management = Event-Driven Streaming in QuixStreams
Kafka is great for maintaining offsets (bookmarks) in a stream of events, allowing consumers to restart from specific points.
QuixStreams uses a similar concept but makes it easier for developers by managing this under the hood. You can replay streams or process real-time data in a declarative, event-driven manner.
4. Schema Management
Kafka relies on schema registries (e.g., Avro or JSON schemas) for managing the structure of data in topics.
QuixStreams goes a step further by integrating schema management directly into its data pipelines. It enables you to work with typed streams and columns in a dataframe-like structure (closer to Pandas) for both time-series and tabular data.
5. Real-Time Dataframes vs Kafka’s Binary Payloads
Kafka deals with raw data (binary blobs), and it’s your responsibility to encode/decode messages.
QuixStreams brings high-level support for dataframes (like Pandas DataFrames), which are tabular representations of data, designed for easy analysis and transformation of real-time data.
6. Use Case Perspective
Kafka is best suited for distributed message processing, log aggregation, and high-throughput applications where low-level control of message streams is required.
QuixStreams is ideal for real-time machine learning, IoT applications, or data-intensive pipelines where developers want to focus more on data manipulation and time-series processing rather than managing Kafka’s details.
Example Workflow in Terms of Kafka and QuixStreams:
Kafka:
A producer sends sensor data as JSON to a Kafka topic.
A consumer subscribes to the topic and deserializes the JSON payload to process it.
Custom logic or additional layers (like Flink or Spark) are needed to aggregate or filter data streams.
QuixStreams:
Data arrives on a stream (backed by Kafka), and you directly read it into a dataframe.
Perform transformations using Python-based operations (e.g., filtering, aggregating).
Publish the processed stream downstream to another system or topic, using the QuixStreams abstraction.

# https://quix.io/docs/quix-streams/producer.html#configuration

Open source the ability to connect, transform and process data in real time

# Redpanda Kafka Ports

# Local development (no Docker)
run-local:
    KAFKA_BROKER_ADDRESS=localhost:19092
    uv run python run.py

# Docker container run
run-docker: build
    docker run -it \
        --network redpanda_network \
        -e KAFKA_BROKER_ADDRESS=redpanda:9092 \
        trades

# Container-to-container
run-internal: build
    docker run -it \
        --network redpanda_network \
        -e KAFKA_BROKER_ADDRESS=redpanda:29092 \
        trades


# pre commit hooks
https://stefaniemolin.com/articles/devx/pre-commit/setup-guide/

# Session 3
# Redpanda and QuixStream: Partitioning and Message Keys

## 1. Partitions in Redpanda

In **Redpanda** (a Kafka-compatible event streaming platform), data is divided into **partitions**. Each partition is an ordered, immutable sequence of messages, and each message within a partition has an **offset**. Partitions enable **parallel processing** of data, improving scalability and fault tolerance.

### Partitioning Logic:
- **Single Key**: Messages with the same key are directed to the same partition, ensuring message order within that key.
- **No Key**: Redpanda uses a round-robin strategy or another hashing mechanism to assign messages to partitions.

## 2. Message Keys in Redpanda

A **message key** is a piece of data associated with each message and determines the partition to which the message belongs.

### Single Message Key:
- A single key (e.g., `user_id` or `order_id`) ensures that all messages with the same key are directed to the same partition.
- This guarantees **message order** for a particular key.
  
#### Example:
- **Key**: `user_id`
- All messages with `user_id=123` will be sent to the same partition, ensuring sequential processing.

### Multiple Message Keys:
- With **multiple keys**, the partition assignment can be more complex.
- **Composite Key**: Multiple fields can be combined into a single key to ensure data is partitioned based on a combination of attributes.

#### Example:
- **Composite Key**: `user_id_transaction_id`
- Messages with different `user_id` and `transaction_id` combinations are assigned to partitions based on the composite key.

## 3. QuixStream and Partitioning with Keys

**QuixStream** allows you to build real-time streaming applications and integrates with **Redpanda** as the backend for event streaming. You can control how data is partitioned based on **message keys** in QuixStream.

### Single Message Key in QuixStream:
- Use a **single key** to ensure that related messages are processed together.
  
#### Example:
```python
from quixstreaming import *

# Create a message with a single key
message = Message(key="user_id", value="order details")

# Send the message to a topic (using QuixStream's producer)
producer.send("order-topic", message)
