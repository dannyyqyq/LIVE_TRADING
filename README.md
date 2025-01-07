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
