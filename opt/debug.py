# _*_ coding: utf-8 _*_
import configparser
import trade_algorithm2
import algrithm_to_back
import fromcsvtodf
import create_csv
import pandas as pd
import numpy
from dataclasses import dataclass
import debug_matplot

CANDLE_INTARVAL = {
        "1440" : "days",
        "240" : "four_hour",
        "60" : "one_hour",
        "15" : "fifteen_minutes",
        "1" : "one_minutes"
    } 

@dataclass
class trend_channel:
    y0:         float
    x0:         float
    slope:      float
    intercept:  float

config = configparser.ConfigParser()
trade = trade_algorithm2.trade_algorithm_2()
convert = algrithm_to_back.df_create_for_back()
csvread = fromcsvtodf.csv_to_df()
csv = create_csv.csv()
debug = debug_matplot.debug_plot()

'''
データを加工し、急騰落を検知
'''

# # ----------------- csvからローソクデータを取り込む ------------------------------
# fileName = "BTCUSDT_2年_2022_8_10_15.csv"
# candleStick = csvread.readDataFromFile(fileName)
# # ------------------------------------------------------------------------------
 
# # ----------------- 取得したローソク足データをデータフレームへ変換 ----------------
# print("DFに変換します")
# df_candleStick = csvread.fromListToDF(candleStick)
# print("DF変換完了しました")
# # ------------------------------------------------------------------------------

# # -------------1分足のデータを違う足のローソク足データへdf変換---------------------
# df = convert.df_convert_for_back(df_candleStick,1440)
# # df2 = convert.df_convert_for_debug(df_candleStick,1440)


# # ---------------------------------急騰落を判断----------------------------------
# f_state_judge = [0 for i in range(len(df.index))] # 何用かに関わらず、ここでf_state_judgeを準備する
# df_f_state_judge = pd.DataFrame({'state_judge': f_state_judge})

# df_f_state_judge = trade.raise_fall_detection_ctrl(df, 1440, df_f_state_judge)

# # df_f_state_judge = trade.raise_fall_detection(df,1440,f_state_judge)
# # ------------------------------------------------------------------------------


# # ---------------------------------csv出力--------------------------------------
# df_f_state_judge.index = df.index
# df_a = pd.merge(df, df_f_state_judge, how='outer', left_index = True, right_index = True)
# csv.get_candlestick_and_create_csv(df_a,"急騰落検知結果10")
# # ------------------------------------------------------------------------------

print(111)

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

# # リストを1ずらす動作確認
# list2 = [6,10,8,2,10,6,15,13]
# d = 1
# c = list2[d:]
# d = [0]
# print(c+d)



# # numpyリストで追加する動作確認
# distance_high, distance_low = {"index": numpy.empty(0),"value": numpy.empty(0)},{"index": numpy.empty(0),"value": numpy.empty(0)}
# distance_low["index"] = []
# print(distance_low["index"])
# for i in range(10):
#     distance_low["index"] = numpy.append(distance_low["index"], 11)
#     print(distance_low["index"])




# # データフレームのお勉強用
# list1 = [3,4,5,6,7,8,9,0]
# list2 = [6,7,8,9,10,11,12,13]

# test_df =  list(zip(list1, list2))
# new_df = pd.DataFrame(test_df, columns = ['iti', 'ni'])

# # print(new_df.iloc[-3:]["ni"])
# # print(new_df.iloc[-3]["ni"])


# print(max(new_df["iti"]))







# print(abs(5))
# print(type(abs(5)))









# distance_high, distance_low = {"index": numpy.zeros(5),"value": numpy.zeros(5)},{"index": numpy.zeros(5),"value": numpy.zeros(5)}
# print(distance_low["index"][1])





# def judge_renge_for_rf_detect(self, df_candlestick: pd.DataFrame, f_state_judge: list):
#         '''
#         急騰落の判定後に、その妥当性を判断し、レンジと判断した場合は修正する。
#         '''
#         # 急騰落の位置を特定       
#         df_f_state_judge = pd.DataFrame({'state_judge': f_state_judge})
            
#         rf_last_num, _ , double_judge, flug         =   self.find_raise_or_fall_backprocess(df_f_state_judge, "last", len(df_f_state_judge.index) - 1, 0) # 必ず最後尾1個手前になるはず
#         rf_start_num, _ , double_judge, flug        =   self.find_raise_or_fall_backprocess(df_f_state_judge, "start", rf_last_num, flug)
#         rf_last_num_before, _ , double_judge, flug  =   self.find_raise_or_fall_backprocess(df_f_state_judge, "last", rf_start_num, flug) # ない場合は0が代入される

#         # # レンジ幅の計算ただし、rf_last_num_beforeとrf_start_numの間が1の場合はエラーが起きるので、更に一つ前で考える
#         if rf_last_num_before - rf_start_num > 1 and double_judge == False:
            
#             r_max_just_before, r_min_just_before, r_width = self.culculate_renge(df_candlestick, rf_last_num_before, rf_start_num)
#             f_state_judge = self.renge_condition(df_candlestick, rf_last_num, rf_start_num, r_min_just_before, r_max_just_before, r_width, f_state_judge, 0)
        
#         elif rf_last_num_before - rf_start_num <= 1 or double_judge:
#             rf_last_num_1, _ , _ , flug         =   self.find_raise_or_fall_backprocess(df_f_state_judge, "last", rf_last_num_before, 0) # 必ず最後尾1個手前になるはず
#             double_judge = True
#             while double_judge: 
#                 rf_start_num_1, _ , double_judge, flug        =   self.find_raise_or_fall_backprocess(df_f_state_judge, "start", rf_last_num_1, flug)
#                 if double_judge: rf_last_num_1 = rf_start_num_1
#                 double_judge2 = True
#             while double_judge2:
#                 rf_last_num_before_1, _ , double_judge2, flug  =   self.find_raise_or_fall_backprocess(df_f_state_judge, "last", rf_start_num_1, flug) # ない場合は0が代入される
#                 if double_judge2: rf_start_num_1 = rf_last_num_before_1

#             r_max_just_before, r_min_just_before, r_width = self.culculate_renge(df_candlestick, rf_last_num_before_1, rf_start_num_1)
#             f_state_judge = self.renge_condition(df_candlestick, rf_last_num, rf_start_num, r_min_just_before, r_max_just_before, r_width, f_state_judge, 1)
        
#         return f_state_judge




















# config.read("set.ini",encoding="utf-8")

# candle_num = config['raise_fall_detection']

# name = "candle_num_" + CANDLE_INTARVAL["15"]

# print(int(candle_num[name]) + int(candle_num[name]))