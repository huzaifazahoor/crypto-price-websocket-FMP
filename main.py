import json
import os
import ssl
import time

import boto3

import websocket


def extract_data(api_key, ticker):
    """
    Extracts real-time crypto price data from the Financial Modeling Prep (FMP) websocket.

    Args:
        api_key (str): Your API key for authentication.
        ticker (str): The crypto ticker symbol to subscribe to.

    Yields:
        dict: Raw JSON data from the websocket.
    """
    ws = websocket.WebSocket(sslopt={"cert_reqs": ssl.CERT_NONE})
    ws.connect("wss://crypto.financialmodelingprep.com")

    login = {
        "event": "login",
        "data": {
            "apiKey": api_key,
        },
    }

    subscribe = {
        "event": "subscribe",
        "data": {
            "ticker": ticker,
        },
    }

    ws.send(json.dumps(login))
    time.sleep(1)
    ws.send(json.dumps(subscribe))

    while True:
        yield json.loads(ws.recv())


def transform_data(raw_data):
    """
    Transforms the raw JSON data into a structured format.

    Args:
        raw_data (dict): Raw JSON data from the websocket.

    Returns:
        dict: Transformed JSON data.
    """
    transformed_data = {
        "ticker": raw_data.get("s", ""),
        "timestamp": raw_data.get("t", 0),
        "exchange": raw_data.get("e", ""),
        "trade_type": raw_data.get("type", ""),
        "last_price": raw_data.get("lp", 0),
        "volume_traded": raw_data.get("ls", 0),
    }
    return transformed_data


def load_data_to_s3(data, s3_bucket):
    """
    Loads the transformed data into an S3 bucket as a JSON file.

    Args:
        data (dict): Transformed JSON data.
        s3_bucket (str): The name of the S3 bucket.

    Returns:
        None
    """
    s3_client = boto3.client("s3")

    file_name = f"{data['exchange']}/{data['ticker']}_{data['timestamp']}.json"

    try:
        s3_client.put_object(Body=json.dumps(data), Bucket=s3_bucket, Key=file_name)
        print(f"Data saved to S3: {file_name}")
    except Exception as e:
        print(f"Error saving data to S3: {str(e)}")


def main():
    api_key = os.getenv("API_KEY")
    ticker = "btcusd"  # Crypto ticker symbol
    s3_bucket = "realtime-crypto-prices-bucket"  # S3 bucket name

    for raw_data in extract_data(api_key, ticker):
        if "s" in raw_data.keys():
            transformed_data = transform_data(raw_data)
            load_data_to_s3(transformed_data, s3_bucket)
        else:
            print(str(raw_data))


if __name__ == "__main__":
    main()
