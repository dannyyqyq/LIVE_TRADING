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