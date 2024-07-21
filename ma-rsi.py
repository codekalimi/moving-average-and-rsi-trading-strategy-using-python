import pandas as pd
import numpy as np
import ta
import yfinance as yf

# Load historical data for a stock (e.g., SBIN.NS)
data = yf.download('^NSEBANK', start='2023-01-01', end='2024-07-19')  # Extended data period

# Calculate moving averages
data['SMA50'] = data['Close'].rolling(window=50).mean()
data['SMA200'] = data['Close'].rolling(window=200).mean()

# Calculate RSI
data['RSI'] = ta.momentum.RSIIndicator(data['Close'], window=14).rsi()

# Drop rows with NaN values
data = data.dropna()

# Initialize columns for signals and positions
data['Buy_Signal'] = 0
data['Sell_Signal'] = 0

# Generate buy and sell signals
for i in range(len(data)):
    if data['SMA50'].iloc[i] > data['SMA200'].iloc[i] and data['RSI'].iloc[i] < 70:
        data['Buy_Signal'].iloc[i] = 1
    elif data['SMA50'].iloc[i] < data['SMA200'].iloc[i] and data['RSI'].iloc[i] > 30:
        data['Sell_Signal'].iloc[i] = 1

# Simulate trading with risk management
initial_balance = 10000  # Initial capital
balance = initial_balance
position = 0
stop_loss = 0
take_profit = 0

for i in range(len(data)):
    # Buy logic
    if data['Buy_Signal'].iloc[i] == 1 and position == 0:
        position = balance / data['Close'].iloc[i]
        stop_loss = data['Close'].iloc[i] * 0.98
        take_profit = data['Close'].iloc[i] * 1.04
        print(f"Buying at {data['Close'].iloc[i]} on {data.index[i]}")

    # Sell logic
    elif (data['Sell_Signal'].iloc[i] == 1 or data['Close'].iloc[i] <= stop_loss or data['Close'].iloc[i] >= take_profit) and position > 0:
        balance = position * data['Close'].iloc[i]
        position = 0
        print(f"Selling at {data['Close'].iloc[i]} on {data.index[i]}")

# Calculate final balance
if position > 0:
    balance = position * data['Close'].iloc[-1]
print(f"Final balance: {balance}")

# Performance metrics
profit = balance - initial_balance
print(f"Total profit: {profit}")
return_percentage = (profit / initial_balance) * 100
print(f"Return on investment: {return_percentage}%")
