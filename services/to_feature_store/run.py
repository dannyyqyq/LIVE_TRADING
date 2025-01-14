from loguru import logger
from quixstreams import Application
from sinks import HopsWorksFeatureStoreSink


def main(
    kafka_broker_address: str,
    kafka_input_topic: str,
    kafka_consumer_group: str,
    output_sink: HopsWorksFeatureStoreSink,
):
    """
    Do 2 things:
    1. Reads messages from kafka topic
    2. Push messages to feature store
    """
    logger.info("Starting feature store service!")

    app = Application(
        broker_address=kafka_broker_address,
        consumer_group=kafka_consumer_group,
    )

    input_topic = app.topic(
        name=kafka_input_topic,
        value_serializer="json",
    )

    # Testing https://quix.io/docs/quix-streams/connectors/sinks/csv-sink.html#delivery-guarantees

    # Initializse CSV with a file path
    # csv_sink = CSVSink(
    #     path="technical_indicators.csv",
    # )

    sdf = app.dataframe(input_topic)

    # To do some pre-processing here...
    # We need to extract the features we want to push to feature store

    # Sink data to csv file
    # sdf.sink(csv_sink)

    # Sink data to feature store
    sdf.sink(output_sink)

    app.run()


if __name__ == "__main__":
    from config import config, hopsworks_credentials

    # Sink to save data to the feature store
    hopsworks_sink = HopsWorksFeatureStoreSink(
        # Hopsowrks credentials
        api_key=hopsworks_credentials.hopsworks_api_key,
        project_name=hopsworks_credentials.hopsworks_project_name,
        # Feature store config
        feature_group_name=config.feature_group_name,
        feature_group_version=config.feature_group_version,
        feature_group_primary_keys=config.feature_group_primary_keys,
        feature_group_event_time=config.feature_group_event_time,
    )

    main(
        kafka_broker_address=config.kafka_broker_address,
        kafka_input_topic=config.kafka_input_topic,
        kafka_consumer_group=config.kafka_consumer_group,
        output_sink=hopsworks_sink,
    )
