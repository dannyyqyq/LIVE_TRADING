from loguru import logger
from quixstreams import Application
from quixstreams.sinks.core.csv import CSVSink


def main(
    kafka_broker_address: str,
    kafka_input_topic: str,
    kafka_consumer_group: str,
    feature_group_name: str,
    feature_group_version: int,
):
    """
    Do 2 things:
    1. Reads messages from kafka topic
    2. Push messages to feature store
    """
    logger.info("Staring feature store service!")

    app = Application(
        broker_address=kafka_broker_address,
        consumer_group=kafka_consumer_group,
    )

    input_topic = app.topic(
        name=kafka_input_topic,
        value_serializer="json",
    )

    # Push messages to feature store
    # TODO: implement feature store push (quixstreams Sinks)
    # Testing https://quix.io/docs/quix-streams/connectors/sinks/csv-sink.html#delivery-guarantees

    csv_sink = CSVSink(
        path="technical_indicators.csv",
    )

    sdf = app.dataframe(input_topic)

    # To do some pre-processing here...
    # We need to extract the features we want to push to feature store

    # Sink data to csv file
    sdf.sink(csv_sink)

    app.run()


if __name__ == "__main__":
    from config import config

    main(
        kafka_broker_address=config.kafka_broker_address,
        kafka_input_topic=config.kafka_input_topic,
        kafka_consumer_group=config.kafka_consumer_group,
        feature_group_name=config.feature_group_name,
        feature_group_version=config.feature_group_version,
    )
