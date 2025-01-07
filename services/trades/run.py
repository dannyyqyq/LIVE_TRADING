from typing import Union

from kraken_api.mock import KrakenMockAPI
from kraken_api.websocket import KrakenWebsocketAPI
from loguru import logger
from quixstreams import Application


def main(
    kafka_broker_address: str,
    kafka_topic: str,
    kraken_api: Union[KrakenWebsocketAPI, KrakenMockAPI],
):
    """
    It does 2 things:
    1. Reads trades from kraken API
    2. Pushes them to Kafka topic

    Args:
        kafka_broker_address: str
        kafka_topic: str
        kraken_api: Union[KrakenWebsocketAPI, KrakenMockAPI]
    Returns:
        None
    """
    logger.info("Start the trades services!")

    # Initialize the quix-stream application
    # Handles low level data and connect to Kafka
    app = Application(
        broker_address=kafka_broker_address,
    )

    # Define a topic where we will push the trades to
    topic = app.topic(name=kafka_topic, value_serializer="json")

    with app.get_producer() as producer:
        while True:
            trades = kraken_api.get_trades()
            for trade in trades:
                # serialize the trade as bytes

                # push the serialized message to the topic
                message = topic.serialize(
                    key=trade.pair.replace("/", "_"), value=trade.to_dict()
                )
                producer.produce(topic=topic.name, value=message.value, key=message.key)

                logger.info(f"Pushed to Kafka: {trade}")


if __name__ == "__main__":
    from config import config

    kraken_api = KrakenWebsocketAPI(pairs=config.pairs)
    # kraken_api = KrakenMockAPI(pair=config.pairs[0])

    main(
        kafka_broker_address=config.kafka_broker_address,
        kafka_topic=config.kafka_topic,
        kraken_api=kraken_api,
    )
