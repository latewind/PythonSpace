import tushare as ts
import matplotlib.pyplot as plt
import numpy as np
import mpl_finance as mpf

KLINE_TT_COLS_MINS = ['date', 'open', 'close', 'high', 'low', 'volume']

if __name__ == '__main__':
    import tushare as ts
    import matplotlib.pyplot as plt
    import mpl_finance as mpf
    import numpy as np
    import pandas as pd

    df = pd.DataFrame(list([[1, 11, 22, 33, 8, 100]]),columns=KLINE_TT_COLS_MINS)
    df = df.set_index('date')
    print(df)
    print(df.loc[1])

    dt = pd.DataFrame()
    dt = dt.append(df,ignore_index=True)
    print(dt)

    data = ts.get_k_data('600519', ktype='D', autype='qfq', start='2017-09-17', end='')
    print(data)
    prices = data[['open', 'high', 'low', 'close']]
    dates = data['date']
    # print(data)
    candleData = np.column_stack([list(range(len(dates))), prices])
    # print(candleData)
    fig = plt.figure(figsize=(10, 6))
    ax = fig.add_axes([0.1, 0.3, 0.8, 0.6])
    mpf.candlestick_ohlc(ax, candleData, width=0.5, colorup='r', colordown='b')
    plt.show()
