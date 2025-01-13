import pandas as pd


def compute_indicators(candle: dict, state: dict) -> dict:
    """
    Compute technical indicators from candles using pandas-ta
    """
    # ta.utils.logger.set_level("INFO")

    # Get candles from state
    candles = state.get("candles", [])

    # Convert candles into a DataFrame
    candles_df = pd.DataFrame(candles)

    # Ensure the candles DataFrame contains necessary columns
    required_columns = ["open", "high", "low", "close", "volume"]
    for col in required_columns:
        if col not in candles_df.columns:
            raise ValueError(f"Missing required column: {col}")

    # Initialize an empty dictionary for indicators
    indicators = {}

    # Compute the technical indicators

    # 1. RSI (Relative Strength Index) at 9, 14, 21
    indicators["rsi_9"] = candles_df.ta.rsi(length=9)
    indicators["rsi_14"] = candles_df.ta.rsi(length=14)
    indicators["rsi_21"] = candles_df.ta.rsi(length=21)

    # 2. MACD (Moving Average Convergence Divergence)
    macd = candles_df.ta.macd(fast=10, slow=24, signal=9)
    indicators["macd"] = macd["MACD_10_24_9"]
    indicators["macd_signal"] = macd["MACDs_10_24_9"]
    indicators["macd_hist"] = macd["MACDh_10_24_9"]

    # 3. Bollinger Bands
    bbands = candles_df.ta.bbands(length=20, std=2)
    indicators["bbands_upper"] = bbands["BBU_20_2.0"]
    indicators["bbands_middle"] = bbands["BBM_20_2.0"]
    indicators["bbands_lower"] = bbands["BBL_20_2.0"]

    # 5. ADX (Average Directional Index)
    indicators["adx"] = candles_df.ta.adx(length=14)["ADX_14"]

    # 6. Volume EMA
    indicators["volume_ema"] = candles_df.ta.ema(length=10, close=candles_df["volume"])

    # 9. ATR (Average True Range)
    indicators["atr"] = candles_df.ta.atr(length=10)

    # 10. Price ROC (Rate of Change)
    indicators["price_roc"] = candles_df.ta.roc(length=6)

    # 11. SMA at 7, 14, and 21
    indicators["sma_7"] = candles_df.ta.sma(length=7)
    indicators["sma_14"] = candles_df.ta.sma(length=14)
    indicators["sma_21"] = candles_df.ta.sma(length=21)

    # Merge indicators back into the latest candle ( SPECIALLY FOR PANDA because talib uses STREAM)
    latest_candle = pd.Series(candle)
    for key, value in indicators.items():
        latest_candle[key] = value.iloc[-1] if not value.empty else None

    return latest_candle.to_dict()


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
