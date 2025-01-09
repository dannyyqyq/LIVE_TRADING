from config import config
from loguru import logger
from quixstreams import State

MAX_CANDLES_IN_STATE = config.max_candles_in_state


def update_candles(
    candle: dict,
    state: State,
) -> dict:
    """
    Updates the list of candles we have in our state using the latest candle

    If the latest candle corresponds to a new window, and the total number
    of candles in the state is less than the number of candles we want to keep,
    we just append it to the list.

    If it corresponds to the last window, we replace the last candle in the list.

    Args:
        candle: The latest candle
        state: The state of our application
        max_candles_in_state: The maximum number of candles to keep in the state
    Returns:
        None
    """
    # Get list of candles from the state
    candles = state.get("candles", default=[])

    if not candles:
        # If the state is empty, we just append the latest candle to the list
        candles.append(candle)
    # If the latest candle corroponds to a new window, we just append it to the list
    elif same_window(candle, candles[-1]):
        # Replace the last candle in the list
        candles[-1] = candle
    else:
        # Append the latest candle to the list
        candles.append(candle)

    # If total number of candles in the state is greater than the number of candles we want to keep,
    # we remove the oldest candle
    if len(candles) > MAX_CANDLES_IN_STATE:
        candles.pop(0)

    logger.debug(f"Number of candles in state for {candle["pair"]}: {len(candles)}")

    # Update the state with a new candle
    state.set("candles", candles)


def same_window(candle: dict, last_candle: dict):
    """
    Checks if the latest candle is in the same window as the last candle
    Args:
        candle (dict): The latest candle
        last_candle (dict): The last candle
    Returns:
        bool: True if the candles are in the same window, False otherwise
    """
    is_same_window = (
        candle["window_start_ms"] == last_candle["window_start_ms"]
        and candle["window_end_ms"] == last_candle["window_end_ms"]
        and candle["pair"] == last_candle["pair"]
    )

    return is_same_window
