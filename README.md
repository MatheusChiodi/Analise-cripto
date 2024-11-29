
# Cryptocurrency Monitoring

This is a web application that allows real-time monitoring of cryptocurrency prices and provides recommendations based on price analysis and market variations. Ideal for investors and cryptocurrency enthusiasts.

## Features

- **Real-time monitoring**: View updated prices and variations of major cryptocurrencies.
- **Purchase recommendations**: Suggestions based on the current price, history, and volatility.
- **Profit/loss calculation**: Based on the average purchase price and the current price.
- **Portfolio totals visualization**: Total expenditure and updated portfolio value.
- **Cryptocurrency descriptions**: Brief information about each cryptocurrency.

## Technologies Used

- **Backend**:
  - [Flask](https://flask.palletsprojects.com/): Web framework for backend development.
  - [CoinGecko API](https://www.coingecko.com/en/api): API used to fetch cryptocurrency prices and variations.

- **Frontend**:
  - HTML and CSS for page structure and styling.

- **Other**:
  - [Python](https://www.python.org/): Programming language used for the application.
  - [Pycoingecko](https://github.com/man-c/pycoingecko): Library for integrating with the CoinGecko API.

## Requirements

- **Python 3.8 or higher**
- **Required libraries**: 
  - Flask
  - Pycoingecko

To install the dependencies, run:
```bash
pip install flask pycoingecko
```

## How to Use

1. Clone this repository:
   ```bash
   git clone <REPOSITORY_URL>
   cd <REPOSITORY_NAME>
   ```

2. Run the application:
   ```bash
   python app.py
   ```

3. Access the application in your browser at:
   ```
   http://127.0.0.1:5000
   ```

## License

This software is copyrighted. Usage is allowed only with attribution to the brand. See the `LICENSE` file for more information.
