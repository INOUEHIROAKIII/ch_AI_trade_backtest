# _*_ coding: utf-8 _*_
import configparser
from curses import savetty
import time
import datetime
import csv
import math
import opt.trade_algorithm_ch as trade_algorithm_ch
import algrithm_to_back
import fromcsvtodf
import create_csv
import pandas as pd
import numpy
from dataclasses import dataclass
import debug_matplot
from setting import setting as se

class simu_ctrl:

    def __init__(self):
        # self.config = configparser.ConfigParser()
        self.trade = trade_algorithm_ch.channel_describe()
        # self.convert = algrithm_to_back.df_create_for_back()
        self.csvread = fromcsvtodf.csv_to_df()
        self.csv = create_csv.csv()
        self.debug = debug_matplot.debug_plot()
        # self.config.read('set.ini',encoding="utf-8")
        self.f_simu = self.config['simulation']['f_simu']
        # self.CHANNEL_PLOT_INTERVAL = self.config['setting']['channek_plot_interval']
        
    def simulation_start(self):
        
        # 初期化
        df_f_state_judge = pd.DataFrame({'state_judge': [0 for i in range(se.INITIAL_DF_SIZE)], 'check': [0 for i in range(se.INITIAL_DF_SIZE)]})


        # ループ
        while True:
            # チャネル引く
            self.trade.all_channel_ctrl(df_f_state_judge)

            # その他、評価指数の計算

            # 強化学習予想

        # バックテスト開始
        backtest.describeResult(entryTerm=backtest.entryTerm, closeTerm=backtest.closeTerm, fileName=fileName , rangeTh=backtest.rangeTh, rangeTerm=backtest.rangeTerm,  originalWaitTerm=backtest.waitTerm, waitTh=backtest.waitTh, candleTerm=backtest.candleTerm,showFigure=True, cost=backtest.cost)
    

    # def pull_rf_data(self, df, ):
    #     # ---------------------------------急騰落を判断----------------------------------
    #     f_state_judge = [0 for i in range(len(df.index))] # 何用かに関わらず、ここでf_state_judgeを準備する
    #     df_f_state_judge = pd.DataFrame({'state_judge': f_state_judge})

    #     df_f_state_judge = self.trade.raise_fall_detection_ctrl(df, self.CHANNEL_PLOT_INTERVAL, df_f_state_judge, True) # 一番始めに全体を準備する=True, f_state_judgeはすでに計算されてあり、最近のものだけを更新する=False

    #     # df_f_state_judge = trade.raise_fall_detection(df,1440,f_state_judge)
    #     # ------------------------------------------------------------------------------

    







# ---------------------------------急騰落結果込みでcsv出力--------------------------------------
df_f_state_judge.index = df.index
df_a = pd.merge(df, df_f_state_judge, how='outer', left_index = True, right_index = True)
csv.get_candlestick_and_create_csv(df_a,"./debug_result/急騰落検知結果_2年_レンジ判断前")
# ------------------------------------------------------------------------------















''' 今回使わない
# # チャネル引く、matplotlib出力
trade.one_renge_channel_describe_forback(df_f_state_judge, df, 1440, 1)
'''

''' 今回使わない
# -----------------------デバックのデバック用matplotlib出力----------------------
max_channel = trend_channel(0, 0, 10, 30000)
second_max_channel = trend_channel(0, 0, 10, 29000)
second_min_channel = trend_channel(0, 0, 10, 28000)
min_channel = trend_channel(0, 0, 10, 27000)

if second_max_channel.slope:
    print(5678890)

debug.debug_channel_plot(1, df, df2, max_channel, second_max_channel, second_min_channel, min_channel)
# ------------------------------------------------------------------------------
'''