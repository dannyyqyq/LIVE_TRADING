from datetime import timedelta
from typing import Any, List, Optional, Tuple

from loguru import logger
from quixstreams.models import TimestampType


def init_candle(trade: dict) -> dict:
    """
    Initialize the candle with the first trade
    """
    return {
        "open": trade["price"],
        "high": trade["price"],
        "low": trade["price"],
        "close": trade["price"],
        "volume": trade["volume"],
    }


def update_candle(candle: dict, trade: dict) -> dict:
    """
    Update the candle with the new trade
    """
    candle["high"] = max(candle["high"], trade["price"])
    candle["low"] = min(candle["low"], trade["price"])
    candle["close"] = trade["price"]
    candle["volume"] += trade["volume"]
    return candle


def custom_ts_extractor(
    value: Any,
    headers: Optional[List[Tuple[str, bytes]]],
    timestamp: float,
    timestamp_type: TimestampType,
) -> int:
    """
    Specifying a custom timestamp extractor to use the timestamp from the message payload
    instead of Kafka timestamp.
    """
    # breakpoint()
    return value["timestamp_ms"]  # depends on the message payload


def main(
    kafka_broker_address: str,
    kafka_input_topic: str,
    kafka_output_topic: str,
    kafka_consumer_group: str,
    candle_seconds: int,
):
    """
    3 Steps:
    1. Ingest trades from kafka
    2. Generates candles using tumbling window
    3. Outputs candles to kafka

    Args:
        kafka_broker_address (str): Kafka broker address
        kafka_input_topic (str): Kafka input topic
        kafka_output_topic (str): Kafka output topic
        kafka_consumer_group (str): Kafka consumer group
        candle_seconds (int): Candle duration in seconds
    """
    logger.info("Starting candles service")

    from quixstreams import Application

    # Initialize the quix stream application
    app = Application(
        broker_address=kafka_broker_address,
        consumer_group=kafka_consumer_group,
    )

    # Define input and output topics
    input_topic = app.topic(
        name=kafka_input_topic,
        value_deserializer="json",
        timestamp_extractor=custom_ts_extractor,
    )

    output_topic = app.topic(
        name=kafka_output_topic,
        value_deserializer="json",
    )

    # Create a streaming dataframe
    sdf = app.dataframe(input_topic)

    # Define a tumbling window
    sdf = sdf.tumbling_window(
        duration_ms=timedelta(seconds=candle_seconds),
    )

    # Define the aggregation (transformation)
    sdf = sdf.reduce(
        reducer=update_candle,
        initializer=init_candle,
    )

    # Emit all intermediate candles to make system more responsive
    # Candles will be recomputed everytime a new trade arrives
    sdf = sdf.current()

    """
    Emit the final candle only after the window ends
    sdf_final = sdf.final()
    """

    # Push the candles to the output topic
    sdf = sdf.to_topic(topic=output_topic)

    # Start the application
    app.run()


if __name__ == "__main__":
    from config import config

    main(
        kafka_broker_address=config.kafka_broker_address,
        kafka_input_topic=config.kafka_input_topic,
        kafka_output_topic=config.kafka_output_topic,
        kafka_consumer_group=config.kafka_consumer_group,
        candle_seconds=config.candle_seconds,
    )
