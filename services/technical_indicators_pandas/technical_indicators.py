import pandas as pd
import pandas_ta as ta
from quixstreams import State


def compute_indicators(
    candle: dict,
    state: State,
) -> dict:
    """
    Compute technical indicators from candles
    """
    candles = state.get("candles", [])

    # Convert candle data into a DataFrame
    df = pd.DataFrame(candles)

    # Ensure that the DataFrame has the correct column names
    df["high"] = df["high"].astype(float)
    df["low"] = df["low"].astype(float)
    df["close"] = df["close"].astype(float)
    df["volume"] = df["volume"].astype(float)

    # Initialize a dictionary for the indicators
    indicators = {}

    # Compute the technical indicators using pandas_ta

    # 1. RSI (relative strength index) at 9, 14, 21
    indicators["rsi_9"] = ta.rsi(df["close"], length=9)
    indicators["rsi_14"] = ta.rsi(df["close"], length=14)
    indicators["rsi_21"] = ta.rsi(df["close"], length=21)

    # 11. SMA at 7, 14, and 21
    indicators["sma_7"] = ta.sma(df["close"], length=7)
    indicators["sma_14"] = ta.sma(df["close"], length=14)
    indicators["sma_21"] = ta.sma(df["close"], length=21)

    # Create the final message with the latest candle and computed indicators
    final_message = {**candle, **indicators}

    return final_message


# def compute_indicators(candle: dict, state: State) -> dict:
#     candles = state.get("candles", [])

#     # Convert candles to a pandas DataFrame
#     df = pd.DataFrame(candles)

#     if df.empty:
#         logger.debug("No candles available to compute df")
#         return candle  # Return the original candle if there are no previous candles

#     # Ensure required columns exist
#     required_columns = ["open", "high", "low", "close", "volume"]
#     if not all(col in df.columns for col in required_columns):
#         logger.error(f"Missing required columns: {set(required_columns) - set(df.columns)}")
#         raise ValueError(f"Missing required columns: {set(required_columns) - set(df.columns)}")

#     # Compute the RSI
#     df["rsi_9"] = ta.rsi(df["close"], length=9)
#     df["rsi_14"] = ta.rsi(df["close"], length=14)
#     df["rsi_21"] = ta.rsi(df["close"], length=21)

# # 3. Bollinger Bands
#     bbands = ta.bbands(df["close"], length=20, std=2)
#     df = pd.concat([df, bbands], axis=1)

#     # 4. Stochastic RSI
#     stochrsi = ta.stochrsi(df["close"], length=10, rsi_length=10, k=5, d=3)
#     df = pd.concat([df, stochrsi], axis=1)

#     # Extract the latest row of df to merge with the current candle
#     latest_df = df.iloc[-1].to_dict()

#     # Log the extracted df
#     logger.debug(f"Latest df: {latest_df}")

#     # Combine the latest candle data with the computed df
#     final_message = {
#         **candle,
#         **{key: value for key, value in latest_df.items() if not pd.isna(value)},
#     }

#     # Log the final message to check if df are included
#     logger.debug(f"Final message with df: {final_message}")

#     return final_message
