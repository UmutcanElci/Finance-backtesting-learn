import pandas as pd
import matplotlib.pyplot as plt

# Data setup (same as before)
data = {
    "Date": pd.date_range(start="2023-01-01", periods=10, freq='D'),
    "Close": [100, 102, 104, 103, 105, 107, 106, 108, 110, 109]
}
df = pd.DataFrame(data)
df.set_index("Date", inplace=True)
df['Short_MA'] = df['Close'].rolling(window=3).mean()
df['Long_MA'] = df['Close'].rolling(window=5).mean()
df['Signal'] = 0
df.loc[df['Short_MA'] > df['Long_MA'], 'Signal'] = 1
df.loc[df['Short_MA'] < df['Long_MA'], 'Signal'] = -1
df['Signal'] = df['Signal'].shift()
df['Daily_Return'] = df['Close'].pct_change()
df['Strategy_Return'] = df['Daily_Return'] * df['Signal']
df['Strategy_Return'].fillna(0, inplace=True)
df['Cumulative_Market_Return'] = (1 + df['Daily_Return']).cumprod()
df['Cumulative_Strategy_Return'] = (1 + df['Strategy_Return']).cumprod()

# Visualization
plt.figure(figsize=(14, 7))

# Plot closing price and moving averages
plt.subplot(2, 1, 1)
plt.plot(df.index, df['Close'], label='Close Price', color='black', lw=2)
plt.plot(df.index, df['Short_MA'], label='Short MA (3 days)', color='blue', linestyle='--')
plt.plot(df.index, df['Long_MA'], label='Long MA (5 days)', color='red', linestyle='--')
plt.title('Stock Price and Moving Averages')
plt.legend()

# Mark buy and sell signals
buy_signals = df[df['Signal'] == 1]
sell_signals = df[df['Signal'] == -1]
plt.scatter(buy_signals.index, buy_signals['Close'], label='Buy Signal', marker='^', color='green', s=100)
plt.scatter(sell_signals.index, sell_signals['Close'], label='Sell Signal', marker='v', color='red', s=100)

# Plot cumulative returns
plt.subplot(2, 1, 2)
plt.plot(df.index, df['Cumulative_Market_Return'], label='Market Return', color='black', lw=2)
plt.plot(df.index, df['Cumulative_Strategy_Return'], label='Strategy Return', color='purple', linestyle='--')
plt.title('Cumulative Returns')
plt.legend()

plt.tight_layout()
plt.show()
