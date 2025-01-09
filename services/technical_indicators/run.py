from loguru import logger
from quixstreams import Application


def main(
    kafka_broker_address: str,
    kafka_input_topic: str,
    kafka_output_topic: str,
    kafka_consumer_group: str,
    max_candles_in_state: int,
):
    """
    3 steps:
    1. Ingests candles from the kafka input topic
    2. Computes technical indicators
    3. Sends the technical indicators to the kafka output topic

    Args:
        kafka_broker_address: The address of the kafka broker
        kafka_input_topic: The topic to ingest candles from
        kafka_output_topic: The topic to send technical indicators to
        kafka_consumer_group: The consumer group for the kafka consumer
        max_candles_in_state: The maximum number of candles to keep in the state
    Returns:
        None
    """
    logger.info("Hello from technical-indicators!")

    app = Application(
        broker_address=kafka_broker_address,
        consumer_group=kafka_consumer_group,
    )

    # Define the input and output topics of our streaming application
    input_topic = app.topic(
        name=kafka_input_topic,
        value_deserializer="json",
    )
    output_topic = app.topic(
        name=kafka_output_topic,
        value_serializer="json",
    )
    # Create a Streaming DataFrame so we can start transforming data in real time
    sdf = app.dataframe(topic=input_topic)

    sdf = sdf.update(lambda value: logger.debug(f"Final message: {value}"))

    # Send the final messages to the output topic
    sdf = sdf.to_topic(output_topic)

    app.run()


# def main(
#     kafka_broker_address: str,
#     kafka_input_topic: str,
#     kafka_output_topic: str,
#     kafka_consumer_group: str,
#     num_candles_in_state: str,
# ):
#     """
#     3 Steps:
#     1. Ingest candles from kafka input topic
#     2. Computes the technical indicators
#     3. Sends the technical indicators to kafka output topic

#     Args:
#         kafka_broker_address (str): Kafka broker address
#         kafka_input_topic (str): Kafka input topic
#         kafka_output_topic (str): Kafka output topic
#         kafka_consumer_group (str): Kafka consumer group
#     Returns:
#         None
#     """
#     logger.info("Starting technical indicators service")

#     # Initialize the quix stream application
#     app = Application(
#         broker_address=kafka_broker_address,
#         consumer_group=kafka_consumer_group,
#     )

#     # Define input and output topics of our streaming application
#     input_topic = app.topic(
#         name=kafka_input_topic,
#         value_deserializer="json",
#     )

#     output_topic = app.topic(
#         name=kafka_output_topic,
#         value_deserializer="json",
#     )

#     # Create a Streaming DataFrame so we can start transforming data in real time
#     sdf = app.dataframe(topic=input_topic)

#     sdf = sdf.update(lambda value: logger.info(f"Candle: {value}"))

#     sdf = sdf.to_topic(topic=output_topic)

#     app.run()


if __name__ == "__main__":
    from config import config

    main(
        kafka_broker_address=config.kafka_broker_address,
        kafka_input_topic=config.kafka_input_topic,
        kafka_output_topic=config.kafka_output_topic,
        kafka_consumer_group=config.kafka_consumer_group,
        max_candles_in_state=config.max_candles_in_state,
    )
