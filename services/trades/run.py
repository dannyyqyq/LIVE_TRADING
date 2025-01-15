from kraken_api.base import TradesAPI
from kraken_api.mock import KrakenMockAPI
from kraken_api.websocket import KrakenWebsocketAPI
from loguru import logger
from quixstreams import Application


def main(
    kafka_broker_address: str,
    kafka_topic: str,
    trades_api: TradesAPI,
):
    """
    It does 2 things:
    1. Reads trades from kraken API
    2. Pushes them to Kafka topic

    Args:
        kafka_broker_address: str
        kafka_topic: str
        TradesAPI: 2 methods to read trades and push to Kafka: get_trades and is_done
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
        while not trades_api.is_done():
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

    # Initialize the Kraken API dependencies
    if config.data_source == "live":
        kraken_api = KrakenWebsocketAPI(pairs=config.pairs)
    elif config.data_source == "historical":
        # TODO: remove this once we are done debugging the KrakenRestAPISinglePair
        # kraken_api = KrakenRestAPI(pairs=config.pairs)
        from kraken_api.rest import KrakenRestAPISinglePair

        kraken_api = KrakenRestAPISinglePair(
            pair=config.pairs[0], last_n_days=config.last_n_days
        )
    else:
        kraken_api = KrakenMockAPI(pairs=config.pairs)

    main(
        kafka_broker_address=config.kafka_broker_address,
        kafka_topic=config.kafka_topic,
        trades_api=kraken_api,
    )
