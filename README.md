# Trading Bot

A Python-based trading bot that implements various trading strategies including bond trading, ETF arbitrage, and moving average strategies.

## Features

- Real-time market data processing
- Multiple trading strategies
- Position management
- Performance logging and monitoring
- Error handling and recovery

## Setup

1. Clone the repository:
```bash
git clone <repository-url>
cd trading-bot
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Configure environment variables:
```bash
cp .env.example .env
# Edit .env with your configuration
```

## Usage

Run the trading bot:
```bash
python main.py
```

The bot will:
- Connect to the exchange
- Execute trading strategies
- Log trades and performance
- Handle errors gracefully

## Project Structure

```
trading-bot/
├── main.py                 # Entry point
├── strategies/             # Trading strategies
│   ├── bond_bot.py        # Bond trading strategy
│   ├── arbitrage_bot.py   # ETF arbitrage strategy
│   └── ma_bot.py          # Moving average strategy
├── utils/                  # Utility modules
│   ├── api.py             # Exchange API client
│   └── logger.py          # Logging utility
├── config/                 # Configuration
│   └── settings.json
└── data/                   # Logs and data
    └── logs.csv
```

## Logging

The bot logs:
- Trade executions
- Performance metrics
- Error messages

Logs are stored in the `data/` directory:
- `trades.csv`: Trade history
- `performance.csv`: Performance metrics

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

MIT License