
import pandas as pd
from matplotlib import pyplot as plt   
from pandas.plotting import register_matplotlib_converters

register_matplotlib_converters()

QQQ_FP = 'Data/QQQ.csv'
SPY_FP = 'Data/SPY.csv'

def select_data(data, start, end):  
    data['Date'] = pd.to_datetime(data['Date'])  
    mask = ( data['Date'] >= start ) & ( data['Date'] <= end )
    data = data.loc[mask, :]
    return data

def sma(data, window = 5):
    """
    Simple Moving Average
    """
    sma = data['Adj Close'].rolling(window=window).mean().bfill()
    price_sma_ratio = (data['Adj Close']/sma) - 1

    return sma, price_sma_ratio

def bb(data, window = 5):
    """
    Bollinger Bands
    """
    sma = data['Adj Close'].rolling(window=window).mean().bfill()
    rolling_std = data['Adj Close'].rolling(window=window).std().bfill()
    bb_ratio = (data['Adj Close'] - sma) / (2 * rolling_std)

    return bb_ratio, rolling_std

def plot_asset(data, asset, window):

    fig = plt.figure()
    plt.title(asset)
    plt.xlabel('Date')
    plt.ylabel('Normalized Portfolio Value (USD)')

    plt.plot(data['Date'], data['Adj Close'], '-', color='green', label=asset)
    plt.plot(data['Date'], data['sma'], '-', color='purple', label=f'sma{window}')
    plt.plot(data['Date'], data['sma'] + (2*data['rolling_std']), color='red', label=f'bb{window}')
    plt.plot(data['Date'], data['sma'] - (2*data['rolling_std']), color='red')
    plt.grid()
    plt.legend(loc='best')
    plt.xticks(rotation=30)

    filepath = 'Graphs/{}'.format(asset)
    fig.tight_layout()

    plt.savefig(filepath)

if __name__ == '__main__':

    window = 30
    portfolio_value = 10000

    data = select_data(pd.read_csv(QQQ_FP), 
                      '2010-07-06', 
                      '2011-07-06')
    
    data = data[['Date', 'Adj Close']]
    data['sma'], data['price_sma_ratio'] = sma(data, window=window)
    data['bb_ratio'], data['rolling_std'] = bb(data, window=window)
    
    plot_asset(data, 'QQQ', window=window)

