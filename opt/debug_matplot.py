import pandas as pd
import matplotlib.pyplot as plt
from mplfinance.original_flavor import candlestick_ohlc
import matplotlib.dates as dates
# from matplotlib import dates as mdates
# import mplfinance as mpf

class debug_plot:
    
    def __init__(self):
        pass

    def debug_channel_plot(self, filename, df_candlestick: pd.DataFrame, max_channel, second_max_channel, second_min_channel, min_channel):
        '''
        dfからローソク足チャートを、channelデータからチャネル直線を画像に残す。df2のtimeは"19206.375"のような感じになっているが、"2022-07-02 09:00:00"への直し方がいまいち分からなかった。ただdebug用でそこまで重要ではないので、そのまま
        '''
        magic = [second_max_channel, second_min_channel, max_channel, min_channel]
        convert = ['time', 'open', 'high','low','close']
        convert_list = {'time' : [], 'open' : [], 'high' : [], 'low' : [], 'close' : []}
        y = [0,0]
        x = [0,0]
        plt.figure(figsize=(20,18))
        # FigureにAxesを１つ追加
        ax = plt.subplot()

        # チャネルを引く
        # 時間軸設定
        ax.xaxis.set_major_formatter(dates.DateFormatter('%Y/%m/%d'))
        for i in range(len(magic)):     
            y[0] = magic[i].slope * 0 + magic[i].intercept
            x[0] = df_candlestick["time"][0]

            y[1] = magic[i].slope * (len(df_candlestick.index) - 1) + magic[i].intercept
            x[1] = df_candlestick["time"][len(df_candlestick.index)-1]
            
            ax.plot(x,y, color = "blue") if i <= 1 else ax.plot(x,y, color = "green")
            # ax.text(19.0, 0.6, '$ R^{2} $=' + str(round(r2_lin, 4)))
            # plt.plot(df_x, y_lin_fit, color = '#000000', linewidth=0.5)


        # # ローソク足描写。mpl_financeのメソッドを仕様（描画幅やチャートの色などを指定)
        # df2を作成し直す
        for n in range(len(convert)):
            convert_list[convert[n]] = df_candlestick[convert[n]].to_list()
        df_2 =  zip(dates.date2num(convert_list["time"]), convert_list["open"], convert_list["high"], convert_list["low"], convert_list["close"])

        candlestick_ohlc(ax, df_2, colorup='g', colordown='r')

        # チャート上部のテキスト
        plt.title(filename)

        # チャートをpng形式で保存
        plt.savefig('data/debug_channel/' + str(filename) + '.png')