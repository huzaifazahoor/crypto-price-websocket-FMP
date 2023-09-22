# Real-Time Crypto Price Extractor

This Python script allows you to extract real-time cryptocurrency price data from the Financial Modeling Prep (FMP) websocket, transform it into a structured format, and then load it into an Amazon S3 bucket as JSON files. It's a useful tool for keeping track of cryptocurrency price movements in real-time and storing historical data for analysis.

## Features

- Connects to the FMP websocket to receive live cryptocurrency price data.
- Transforms the raw JSON data into a structured format for easy analysis.
- Stores the transformed data as JSON files in an Amazon S3 bucket.
- Customizable with your API key, crypto ticker symbol, and S3 bucket name.

## Prerequisites

Before you can use this script, you'll need the following:

- Python 3 installed on your system.
- An API key from Financial Modeling Prep (FMP). You can get one [here](https://financialmodelingprep.com/developer/docs/websocket-api/) if you don't have one already.
- An Amazon S3 bucket where you want to store the data.

## Usage

1. Clone this repository to your local machine:

   ```
   git clone https://github.com/yourusername/realtime-crypto-price-extractor.git
   cd realtime-crypto-price-extractor
   ```

2. Install the required Python libraries:

   ```pip install websocket-client boto3```

3. Set up your API key and S3 bucket name as environment variables or replace the default values in the main function:

   ```
   api_key = os.getenv("API_KEY")
   ticker = "btcusd"
   s3_bucket = "YOUR_S3_BUCKET_NAME"
   ```

4. Install the required Python libraries:

   ```pip install -r requirements.txt```

4. Run the script:

   ```python crypto_price_extractor.py```

The script will connect to the FMP websocket, retrieve real-time data, transform it, and save it to your specified S3 bucket.