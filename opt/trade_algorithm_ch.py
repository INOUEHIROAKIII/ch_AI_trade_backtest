#_*_ coding: utf-8 _*_

import pandas as pd
import datetime
import numpy as np
import math
from dataclasses import dataclass
from sklearn.linear_model import LinearRegression
import debug_matplot
import fromcsvtodf
from setting import channel_info_set, inifile, channel_ctrl
from setting import setting as se
                                                                    # ★　save_pointの運用がよくわからない。あとでしっかりすること
class channel_describe:

    def __init__(self):
        # インスタンス生成
        self.csvread = fromcsvtodf.csv_to_df()
        self.debug = debug_matplot.debug_plot()
        self.ch_info = channel_info_set()
        self.previous_ch_info = channel_info_set()
        self.cc = channel_ctrl()
        
        # 計算プロセスで必要なtempファイル
        self.ch_max, self.ch_2_max, self.ch_min, self.ch_2_min = [], [], [], []
        self.tmp_ch = {
            'max': self.ch_max,
            'max2': self.ch_2_max,
            'min': self.ch_min,
            'min2': self.ch_2_min
        }
        self.dx = 0 # localの距離計算point格納用
        self.magic = [self.ch_info.max_channel2, self.ch_info.min_channel2, self.ch_info.max_channel, self.ch_info.min_channel]

        # INIファイル読み込み
        self.INI = inifile()
        self.debug_val = self.INI.set['debug']
        self.f_simu = self.INI.set['simulation']['f_simu']
        self.CHANNEL_PLOT_INTERVAL = self.INI.set['setting']['channel_plot_interval']

        # 初期設定 これいらない。★★後でsettingとがっちゃんこさせる
        self.cc.loop_count = 0
        self.cc.save_df_start_date = datetime.datetime.strptime('20180101', '%Y%m%d') # 初期化
        self.cc.save_df_start_point = 0


    def raise_fall_detection(self, df_candlestick: pd.DataFrame, candle_intarval, f_state_judge: list, f_check: list, i):
        '''
        # 急騰落チェック（毎回）
        # 渡されたデータ（◇◇➀足）で全体チャートの内、現価格の〇〇➀％の急騰落と、それ以外に分類する
            # 上昇の場合 : 前日のlowを当日のlowが超えない(= ➁何日間のlowを下回る)。超えてもcloseが陽線ならまだ上昇と考える。当日のlowが前日のlowを超え、陰線の場合、上昇は終了と考える。
            # 下落の場合 : 前日のhighを当日のhighが超えない(= ➁何日間のhighを上回る)。超えてもcloseが陰線ならまだ下落と考える。当日のhighが前日のhighを超え、陽線の場合、下落は終了と考える。
        # return 配列f_state_judge（レンジ = 0、急騰 = 2、急落= -2）
        注意:必ず0:00から始まるデータであること(1分足から日足へ加工する場合)。
        '''

        # 複数の時間足に対応 ※intとかはつけなくても良いが一応
        candle_num  =  int(se.candle_num[se.CANDLE_INTARVAL[str(candle_intarval)]])
        raise_value =  int(se.raise_value[se.CANDLE_INTARVAL[str(candle_intarval)]])
        fluc_term   =  int(se.fluc_term[se.CANDLE_INTARVAL[str(candle_intarval)]])
        # ↓は、やり方がクソ過ぎるのでいつかやり方分かったら変更したい
        a1, a2, a3, a4, a5 = 0, 0, 0, 0, 0 # ★★この初期化いらないかも。出来る可能性ある
        for i, a in enumerate(['a1', 'a2', 'a3', 'a4', 'a5']):
            exec("{} = float(se.raise_rate[i][se.CANDLE_INTARVAL[str(candle_intarval)]])".format(a))

        # 急峻を判定。１，繋がっていて、２，一定以上に変動があること
        if (i >= candle_num):
            change_val_high = max(df_candlestick["high"][i - candle_num + 1 : i + 1])
            change_val_low  = min(df_candlestick["low"][i - candle_num + 1 : i + 1])
            xp = df_candlestick["close"][i - candle_num]
            
            if change_val_high - change_val_low > a1 * xp ** (5) + a2 * xp ** (4) + a3 * xp ** (3) + a4 * xp ** (2) + a5 * xp + raise_value:
                max_index = np.argmax(df_candlestick["high"][i - candle_num + 1 : i + 1])
                min_index = np.argmin(df_candlestick["low"][i - candle_num + 1 : i + 1])
                self.ch_info.renge["rf_value"] = change_val_high - change_val_low

                if   max_index > min_index:
                    # 急騰と判断。上書き禁止風  ★★ただし、上がって下がっての可能性も全然ありえるので、必ずどちらか一つであろう3毎に分けて判断。対応必要ないかも
                    
                    for j in range(max_index - min_index + 1):
                        f_state_judge[i - candle_num + min_index + j + 1] = 2 if f_state_judge[i - candle_num + min_index + j + 1] == 0 and f_check[i - candle_num + min_index + j + 1] == 0 else f_state_judge[i - candle_num + min_index + j + 1]

                elif max_index < min_index:
                    # 急落と判断。上書き禁止風 

                    for j in range(min_index - max_index + 1):
                        f_state_judge[i - candle_num + max_index + j + 1] = -2 if f_state_judge[i - candle_num + max_index + j + 1] == 0 and f_check[i - candle_num + min_index + j + 1] == 0 else f_state_judge[i - candle_num + max_index + j + 1]

                elif max_index == min_index:
                    # ハイボラティリティ、openとcloseから陽線か陰線かを特定
                    if f_state_judge[i - candle_num + max_index + 1] == 0 and f_check[i - candle_num + min_index + j + 1] == 0:
                        f_state_judge[i - candle_num + max_index + 1] = -2 if df_candlestick["open"][i - candle_num + max_index + 1] > df_candlestick["close"][i - candle_num + max_index + 1] else 2
    

            # 上昇、下落の終了を判断する
            # 上昇の場合：前日のlowを当日のlowが超えない。超えてもcloseが陽線ならまだ上昇と考える。当日のlowが前日のlowを超え、陰線の場合、上昇は終了と考える。
            if f_state_judge[i-1] == 2 and f_state_judge[i] == 0:
                
                low         = min([price for price in df_candlestick["low"][i-fluc_term:i]])  # 一つ前までに結果
                close_min   = min([price for price in df_candlestick["close"][i-fluc_term:i]])
                
                if df_candlestick["low"][i] < low and df_candlestick["close"][i] < close_min:
                    f_state_judge[i] = 0
                    # f_state_judge = self.judge_renge_for_rf_detect(df_candlestick, f_state_judge, self.ch_info.renge["rf_value"])　# 妥当性検証は次のチャネル引く際に包含する
                elif  not (df_candlestick["low"][i] < low) or not (df_candlestick["close"][i] < close_min):
                    f_state_judge[i] = 2

            # 下落の場合：前日のhighを当日のhighが超えない。超えてもcloseが陰線ならまだ下落と考える。当日のhighが前日のhighを超え、陽線の場合、下落は終了と考える。
            elif f_state_judge[i-1] == -2 and f_state_judge[i] == 0:

                high        = max([price for price in df_candlestick["high"][i-fluc_term:i]]) # 一つ前までに結果
                close_max   = max([price for price in df_candlestick["close"][i-fluc_term:i]])
                
                if df_candlestick["high"][i] > high and df_candlestick["close"][i] > close_max:
                    f_state_judge[i] = 0
                    # f_state_judge = self.judge_renge_for_rf_detect(df_candlestick, f_state_judge, self.ch_info.renge["rf_value"])　# 妥当性検証は次のチャネル引く際に包含する
                elif  (df_candlestick["high"][i] < high) or (df_candlestick["close"][i] < close_max):
                    f_state_judge[i] = -2

        return f_state_judge
        
    
    def raise_fall_detection_ctrl(self,df_candlestick: pd.DataFrame, candle_intarval, df_f_state_judge: pd.DataFrame):
        '''
        逐一実行用。df_state_judgeは、はじめは、500の空のデータフレームを引数に入力する必要あり。以降は返却値を再度引数に指定するだけ。追加の部分だけやる。
        '''
        # リストに変更
        f_state_judge   = df_f_state_judge['state_judge'].to_list()
        f_check         = df_f_state_judge['check'].to_list() # f_checkは、急落の妥当性確認結果。0は正常、1はレンジと判断。
        # print(f_state_judge)

        if self.cc.loop_count == 0:
            # 起動初期の処理
            # iをdf_candlestickの長さ分回す。# loopでは、500程度。シミュレーションでは、1万以上
            for i in range(len(df_candlestick.index)):
                f_state_judge = self.raise_fall_detection(df_candlestick, candle_intarval, f_state_judge, f_check, i)
        else:
            # 2ループ目以降
            # 先頭を削除し、1ずらす。最後尾に0を入れる
            f_state_judge.pop(0)
            f_state_judge.append(0)
            f_check.pop(0)
            f_check.append(0)

            # iに最後尾の値を代入
            self.cc.save_process_date = df_candlestick['time'][len(df_candlestick.index) - 1]
            self.cc.save_process_point = df_candlestick[df_candlestick['time'] == self.cc.save_process_date].index[0] 
            f_state_judge = self.raise_fall_detection(df_candlestick, candle_intarval, f_state_judge, f_check, i = self.cc.save_process_point)
        
        df_f_state_judge = pd.DataFrame({'state_judge': f_state_judge, 'check': f_check})

        return df_f_state_judge


    def channel_describe(self, start_num, last_num, df_candlestick_forfirst: pd.DataFrame, df_candlestick: pd.DataFrame, df_candlestick_marge: pd.DataFrame, f_side ,candle_intarval):
        '''
        ローソク足が更新される度に、チャネルを引き直す
        '''
        # # ---------------ローカル極値を格納する--------------------------
        # # 急変動終了時に、最高値もしくは、最安値を見つける # ★★df_candleは所望の場所も取り込めている？
        # if self.local_ext_value["local_side"] == [] : # ★★初期化対象 distanceも
        #     if f_side == 2:
        #         self.local_ext_value["local_side"].append("high")
        #         self.local_ext_value["y_value"].append(max(df_candlestick_forfirst["high"]))
        #         self.local_ext_value["index"].append(0) # ★★ 確認
        #         self.local_ext_value["length"] = len(df_candlestick_forfirst)
        #         self.local_ext_value["first_index"] = df_candlestick_forfirst["high"].idxmax() # ★low minの間違いでは？
        #     else:
        #         self.local_ext_value["local_side"].append("low")
        #         self.local_ext_value["y_value"].append(min(df_candlestick_forfirst["low"]))
        #         self.local_ext_value["index"].append(0)
        #         self.local_ext_value["length"] = len(df_candlestick_forfirst)
        #         self.local_ext_value["first_index"] = df_candlestick_forfirst["low"].idxmax() # ★high minの間違いでは？
        # else:
        #     # レンジ開始以降のローカル極値をジャッジ(retrun:値とside,index。ない場合は0,"None"が返却。ローソク足が更新されるたびに後ろから計算するので重複はない)
        #     local_value, local_side, x_index = self.find_local_ext_value(df_candlestick, candle_intarval)

        #     if x_index >= 0:
        #         self.local_ext_value["local_side"].append(local_side)
        #         self.local_ext_value["y_value"].append(local_value)
        #         self.local_ext_value["index"].append(x_index + self.local_ext_value["length"] - self.local_ext_value["first_index"] + 1) # このまま配列に代入して良い値
        # # --------------------------------------------------------------
        # print(self.local_ext_value)

        # -----------------------最小二乗法------------------------------
        # ローカル極値の数が○○個以上になったら最小二乗法で傾きと切片を計算。y=ax+b
        if self.local_ext_value["local_side"].count("high") >= se.ch_start_point and self.local_ext_value["local_side"].count("low") >= se.ch_start_point:
            self.line_regression.slope, self.line_regression.intercept, r2 = self.linear_regression(df_candlestick, self.local_ext_value["length"] - self.local_ext_value["first_index"])
            print(self.line_regression.slope)
            print(self.line_regression.intercept)
            print(r2)
        # --------------------------------------------------------------


        # -----------------------点と線の距離 ＆ チャネル計算------------------------------
        # local極値の中でy=ax+bからの距離が一番遠い点を探し、格納する
        # 点(x0,y0)との距離は、|ax0+by0+c|/sqrt(a*a+b*b) ★★毎回一から計算するのは違う。
        length_df = len(self.local_ext_value["local_side"])  # ★★長さちゃんと観れているか？

        if self.line_regression.slope or self.line_regression.intercept:
            
            for n in np.arange(self.dx, length_df, 1): # ★★ self.dxは初期化対象。 length.dfは最後尾を表している
                if self.local_ext_value["local_side"][n] == "high":
                    x0 = self.local_ext_value["index"][n]
                    # x0 = self.local_ext_value["index"][n] + (self.local_ext_value["length"] - self.local_ext_value["index"][0]) if n != 0 else 0 # 最初の極値まで含む計算式にしている。x0は配列に代入する値。0から数えて。。
                    y0 = self.local_ext_value["y_value"][n]
                    self.distance_high["value"] = np.append(self.distance_high["value"], abs(-self.line_regression.slope * x0 + 1 * y0 + (-self.line_regression.intercept)) / math.sqrt(self.line_regression.slope ** (2) + 1 ** (2))) # ★★self.local_ext_valueのnの位置がおかしい
                    self.distance_high["index"] = np.append(self.distance_high["index"], x0)

                if self.local_ext_value["local_side"][n] == "low":
                    x0 = self.local_ext_value["index"][n]
                    # x0 = self.local_ext_value["index"][n] + (self.local_ext_value["length"] - self.local_ext_value["index"][0]) if n != 0 else 0 # 最初の極値まで含む計算式にしている。x0は配列に代入する値。0から数えて。。
                    y0 = self.local_ext_value["y_value"][n]
                    self.distance_low["value"] = np.append(self.distance_low["value"], abs(-self.line_regression.slope * x0 + 1 * y0 + (-self.line_regression.intercept)) / math.sqrt(self.line_regression.slope ** (2) + 1 ** (2)))
                    self.distance_low["index"] = np.append(self.distance_low["index"], x0)
            self.dx = length_df

            # -------------------- 第１チャネルを計算する ------------------------------
            
            # max側
            self.max_channel.x0         =   self.distance_high["index"][np.argmax(self.distance_high["value"])]
            self.max_channel.y0         =   df_candlestick_marge["high"][self.max_channel.x0 + self.local_ext_value["first_index"]+1]
            self.max_channel.slope      =   self.line_regression.slope
            self.max_channel.intercept  =   self.max_channel.y0 - self.max_channel.x0 * self.max_channel.slope

            # min側
            self.min_channel.x0         =   self.distance_low["index"][np.argmax(self.distance_low["value"])]
            self.min_channel.y0         =   df_candlestick_marge["low"][self.min_channel.x0 + self.local_ext_value["first_index"]+1]
            self.min_channel.slope      =   self.line_regression.slope
            self.min_channel.intercept  =   self.min_channel.y0 - self.min_channel.x0 * self.min_channel.slope


            # --------------------第２チャネルを計算する-----------------------------------
            # 一番端から検索し、local極値が0.6%の間に2個以上重なるチャネルを格納する
            second_channel_search_rate = float(self.ch_val["second_channel_search_rate"])
            
            magic =["max", "min"]
            candle_column = {"max": "high", "min": "low"}
            distance_magic = {"max": self.distance_high, "min": self.distance_low}
            channel_magic = {"max": self.second_max_channel, "min": self.second_min_channel, "max1": self.max_channel, "min1": self.min_channel}
            second_do = {"max": False, "min": False}
            
            for j in magic:
                df1 = pd.DataFrame({j: distance_magic[j]["value"], "idx": distance_magic[j]["index"]})
                df1.sort_values(by = j, ascending = False)

                for n in range(len(df1.index) - 2):
                    # second_do[j] = False
                    if df1[j][n] - df1[j][n + 1] <= df_candlestick["close"][n] * second_channel_search_rate:
                        channel_magic[j].x0         =   df1["idx"][n]
                        channel_magic[j].y0         =   df_candlestick_marge[candle_column[j]][channel_magic[j].x0 + self.local_ext_value["first_index"] +1]
                        channel_magic[j].slope      =   self.line_regression.slope
                        channel_magic[j].intercept  =   channel_magic[j].y0 - channel_magic[j].x0 * channel_magic[j].slope
                        second_do[j] = True
                        break
                print(second_do[j])
                if channel_magic[j].x0 == 0 or second_do[j] == False:
                    name = str(j) + "1"
                    channel_magic[j].x0         =   channel_magic[name].x0 
                    channel_magic[j].y0         =   channel_magic[name].y0 
                    channel_magic[j].slope      =   channel_magic[name].slope
                    channel_magic[j].intercept  =   channel_magic[name].intercept                    

        return (self.max_channel, self.min_channel, self.second_max_channel, self.second_min_channel, self.local_ext_value["first_index"])


    def one_renge_channel_describe_forback(self, df_f_state_judge: pd.DataFrame, df_candlestick: pd.DataFrame, candle_intarval, number_in_progress):
        '''
        シミュレーション用。1レンジのみ計算する関数。discribeでloopさせ、一定期間実施するよう組み合わせる必要あり。
        '''
        # 古い方から急騰落を見つける
        i = number_in_progress
        plot_number = 0
            
        rf_start_num, _                 =   self.find_raise_or_fall_forwardprocess(df_f_state_judge, "start", i)
        rf_last_num, _                  =   self.find_raise_or_fall_forwardprocess(df_f_state_judge, "last", rf_start_num)
        rf_second_start_num, end_judge  =   self.find_raise_or_fall_forwardprocess(df_f_state_judge, "start", rf_last_num) # 最後の場合は、最後の値を返却
        # print(df_f_state_judge)
        # print(rf_start_num)
        # print(rf_last_num)
        # print(rf_second_start_num)
        # print(df_f_state_judge['state_judge'][rf_last_num - 1])


        for i in range(rf_second_start_num - rf_last_num):
            current_num = rf_last_num + 1 + i # 最新にするには＋１が必要かも
            self.max_channel, self.min_channel, self.second_max_channel, self.second_min_channel, back_number_ofDF = self.channel_describe(0, (rf_last_num - rf_start_num), df_candlestick[rf_start_num + 1: rf_last_num].reset_index(), df_candlestick[rf_last_num + 1: current_num].reset_index(), df_candlestick[rf_start_num: current_num].reset_index(), df_f_state_judge['state_judge'][rf_last_num - 1], candle_intarval)
            # # ★本当に一番後ろからtry_num目から取れているか確認すること。一つずらした時に-2 or 2なら〇

            self.ch_max.append(self.max_channel)
            self.ch_2_max.append(self.second_max_channel)
            self.ch_2_min.append(self.second_min_channel)
            self.ch_min.append(self.min_channel)

            # matplotlibでチャネル表示 debug_modeの時のみ
            # if self.debug_val["channel_plot"] == True and plot_number < int(self.debug_val["plot_number"]): # ★★typeはどんな感じ？
            # print(self.max_channel)
            # print(self.second_max_channel)
            # print(self.second_min_channel)
            # print(self.min_channel)
            start_point = rf_start_num + back_number_ofDF + 1
            # print(df_candlestick[back_number_ofDF: current_num])
            self.debug.debug_channel_plot(str(i), df_candlestick[start_point: current_num].reset_index(), self.max_channel, self.second_max_channel, self.second_min_channel, self.min_channel)
            # print(df_candlestick[back_number_ofDF: current_num].reset_index())
            plot_number += 1

        # 最後、self変数の初期化
        # self.local_ext_valueの初期化がいる

        return (rf_second_start_num, end_judge, self.ch_max, self.ch_2_max, self.ch_2_min, self.ch_min)
    

    def find_raise_or_fall_forwardprocess(self, df_f_state_judge: pd.DataFrame, find_side, num_in_progress):
        '''
        df_fのデータを前から検索していき、急落とその以外の箇所を格納する。
        '''
        rf_judge = False
        num = num_in_progress

        while not rf_judge:
            num += 1
            
            if num >= len(df_f_state_judge.index) - 1:  # lenの結果に-1すると最後尾を表示することになる
                return (len(df_f_state_judge.index) - 1, True)
            
            if find_side == "start":
                rf_judge = True if abs(df_f_state_judge['state_judge'][num]) > 1 else False
            elif find_side == "last":
                rf_judge = True if abs(df_f_state_judge['state_judge'][num]) == 0 else False
        return (num, False)


    def linear_regression(self, df_candlestick: pd.DataFrame, x1):

        if (len(df_candlestick.index) >= 1): 
            # 回帰分析　線形
            mod = LinearRegression()
            df_x = pd.DataFrame(pd.Series(df_candlestick.index, index=df_candlestick.index))
            df_y = pd.DataFrame(pd.Series(df_candlestick["close"], index=df_candlestick.index))

            # 線形回帰モデル、予測値、R^2を評価
            mod_lin = mod.fit(df_x, df_y)
            y_lin_fit = mod_lin.predict(df_x)
            r2_lin = mod.score(df_x, df_y)

            slope = y_lin_fit[1] - y_lin_fit[0]
            yb = y_lin_fit[0] - slope * x1

            return (slope, yb, r2_lin)

        return (1, 1, 1)


    def find_first_local_ext_value(self, df_candlestick_forfirst: pd.DataFrame, df_f_state_judge: pd.DataFrame, i):
        ##  急落最初のローカル極値を見つける  ##

        # ★★iの位置が適当。save_countはおかしいかもなので、何か考える。
            if df_f_state_judge['state_judge'][i] == 2:
                self.ch_info.local_value.side.append("high")
                self.ch_info.local_value.y_value.append(max(df_candlestick_forfirst["high"]))
                self.ch_info.local_value.index.append(0) # ★★ 確認  
                self.ch_info.local_value.first_index = df_candlestick_forfirst["low"].idxmin() # ★low minの間違いでは？
            elif df_f_state_judge['state_judge'][i] == -2:
                self.ch_info.local_value.side.append("low")
                self.ch_info.local_value.y_value.append(min(df_candlestick_forfirst["low"]))
                self.ch_info.local_value.index.append(0)
                self.ch_info.local_value.first_index = df_candlestick_forfirst["high"].idxmax() # ★high minの間違いでは？
            self.ch_info.local_value.length = len(df_candlestick_forfirst)
    
    def find_local_ext_value(self, df_candlestick: pd.DataFrame, candle_intarval):
        '''
        ローカル極値を見つける
        '''
        # 複数の時間足に対応
        local_term_after  = int(se.local_term['after'][se.CANDLE_INTARVAL[str(candle_intarval)]])
        local_term_before = int(se.local_term['before'][se.CANDLE_INTARVAL[str(candle_intarval)]])
        x_index = len(df_candlestick.index) - (local_term_after + 1)

        if len(df_candlestick.index) >= local_term_after + local_term_before + 1:
            # 最新足のlocal_term_after本前がローカル極値か判定する
            if df_candlestick.iloc[- local_term_after - 1]["high"] >= max(df_candlestick.iloc[- (local_term_after + local_term_before + 1):]["high"]):
                return (df_candlestick.iloc[- local_term_after - 1]["high"], "high", x_index)
            
            if df_candlestick.iloc[- local_term_after - 1]["low"] <= min(df_candlestick.iloc[- (local_term_after + local_term_before + 1):]["low"]):
                return (df_candlestick.iloc[- local_term_after - 1]["low"], "low", x_index)
            # print(len(df_candlestick.index))
            # print(df_candlestick.iloc[- local_term_after - 1]["high"])
            # print(max(df_candlestick.iloc[- (local_term_after + local_term_before + 1):]["high"]))
        return (0, "none", x_index)


    def re_channel_ctrl(self, rf_start_num, rf_last_num, df_f_state_judge: pd.DataFrame, i, df_candlestick: pd.DataFrame, candle_intarval):
        ## 現チャネルの引き直しを制御 ##
        
        # ---------------ローカル極値を格納する--------------------------
        # 急変動終了時に、最高値もしくは、最安値を見つける # ★★df_candleは所望の場所も取り込めている？
        if self.ch_info.local_value.side == [] and self.previous_ch_info.ch_big_break_date != None: # ★★ i=save_countもしっかりすること★★初期化対象 distanceも★★previousが正しいか全然みていない
            self.find_first_local_ext_value(df_candlestick_forfirst = df_candlestick[rf_start_num + 1: rf_last_num].reset_index())
        
        # レンジ開始以降のローカル極値をジャッジ(retrun:値とside,index。ない場合は0,"None"が返却。ローソク足が更新されるたびに後ろから計算するので重複はない)。急落後からのキャンドルデータを使用する
        local_value, local_side, x_index = self.find_local_ext_value(df_candlestick[rf_last_num + 1: i + 1].reset_index(), candle_intarval) # ★★iの妥当性確認しなさい

        if local_side != 'none': # ★★このままだとNoneの時も格納するが良いか？ # x_indexが0以下の場合、ローカルを計算する本数にdfの数が足りていない
            self.ch_info.local_value.side.append(local_side)
            self.ch_info.local_value.y_value.append(local_value)
            self.ch_info.local_value.index.append(x_index + self.ch_info.local_value.length - self.ch_info.local_value.first_index + 1) # このまま配列に代入して良い値
        # --------------------------------------------------------------

        self.ch_info.f_4_comp = True if len(self.ch_info.local_value.side) >= 4 else False # ★★Noneを格納している今だとおかしくなる
        self.ch_info.f_re_ch = True if len(self.ch_info.local_value.side) <= 9 else False

        # extendメソッドの為にも返り値が必要
        return self.ch_info.local_value.side, self.ch_info.local_value.y_value, self.ch_info.local_value.index

    
    def extend_and_compare_channel(self, df_candlestick: pd.DataFrame, i):
        ##  現チャネルを伸ばし、現行valueと比較  ##
        i = self.cc.save_df_start_point
        ch = [self.ch_info, self.previous_ch_info]
        tmp = 0

        if self.ch_info.f_4_comp:
            # chのmax,min
            self.ch_info.renge['just_max'] = self.ch_info.max_channel.slope * i + self.ch_info.max_channel.intercept
            self.ch_info.renge['just_min'] = self.ch_info.min_channel.slope * i + self.ch_info.min_channel.intercept

        elif not(self.ch_info.f_4_comp) and self.previous_ch_info.f_4_comp:
            # previous_chのmax,min
            self.previous_ch_info.renge['just_max'] = self.previous_ch_info.max_channel.slope * i + self.previous_ch_info.max_channel.intercept
            self.previous_ch_info.renge['just_min'] = self.previous_ch_info.min_channel.slope * i + self.previous_ch_info.min_channel.intercept
            tmp = 1
        # f_channel_out：チャネルの外か中かを判定
        max_condition = ch[tmp].renge['just_max'] < df_candlestick['high'][i]
        min_condition = ch[tmp].renge['just_min'] > df_candlestick['low'][i]
        ch[tmp].f_channel_out = True if (max_condition or min_condition) else False

        # chを割ったか否かで、その日にち、向き等をtmpに格納。初期化も実施
        if ch[tmp].f_channel_out: 
            self.ch_info.tmp_ch_break_date.append(df_candlestick['time'][i]) # ★★合っているか要確認
            ct = self.ch_info.temp_ch
            ct.side, ct.y_value, ct.index = self.re_channel_ctrl() # temp_chにも格納。re_channel_ctrlでch_infoにも格納済
        else:
            ct = self.ch_info.temp_ch
            ct.side, ct.y_value, ct.index = "None", 0, 0 # temp_ch初期化


    def channel_position_ctrl(self, rf_start_num, rf_last_num, df_candlestick: pd.DataFrame, df_f_state_judge: pd.DataFrame, i):
        ## チャネル計算の場所を決める ##
        if self.cc.save_df_start_date > previous_ch_info
        
        
        self.channel_describe(0, (rf_last_num - rf_start_num), df_candlestick[rf_start_num + 1: rf_last_num].reset_index(), df_candlestick[rf_last_num + 1: current_num].reset_index(), df_candlestick[rf_start_num: current_num].reset_index(), df_f_state_judge['state_judge'][rf_last_num - 1], candle_intarval)
        def channel_describe(self, start_num, last_num, df_candlestick_forfirst: pd.DataFrame, df_candlestick: pd.DataFrame, df_candlestick_marge: pd.DataFrame, f_side ,candle_intarval):
        
            pass


    
    def check_rf_result(self, rf_start_num, rf_last_num, df_candlestick: pd.DataFrame, df_f_state_judge: pd.DataFrame, i):
        ## チャネルの式から、急落が正しいか判断する ##
        
        if self.ch_info.f_4_comp:
            
            width_value = self.ch_info.renge["renge_width"] # 現chのレンジ幅

            # 特殊条件定義
            condition_B = df_candlestick["low"][rf_last_num] < self.ch_info.renge["just_min"] - width_value/3 # min_value,max_value_just_beforeを毎回格納するようにする
            condition_C = df_candlestick["high"][rf_last_num] > self.ch_info.renge["just_max"] + width_value/3 # ★★3の数字はいじれるように変更すること

            if not condition_B or not condition_C:
                # 急騰落はレンジの中と判断して、f_state_judgeの該当箇所を0へ変更
                for n in np.arange(rf_start_num + 1, rf_last_num + 1, 1):
                    df_f_state_judge['state_judge'][n] = 0
                    df_f_state_judge['check'][n] = 1

        else:
            
            width_value = self.previous_ch_info.renge["renge_width"] # 前chのレンジ幅

            # 特殊条件定義
            condition_A = self.ch_info.renge["rf_value"] > width_value

            if not condition_A:
                # 急騰落はレンジの中と判断して、f_state_judgeの該当箇所を0へ変更
                for n in np.arange(rf_start_num + 1, rf_last_num + 1, 1):
                    df_f_state_judge['state_judge'][n] = 0
                    df_f_state_judge['check'][n] = 1

        return df_f_state_judge


    def Channel_all_judge_ctrl(self, df_candlestick: pd.DataFrame, df_f_state_judge: pd.DataFrame, i):
        ## チャネルの方向性を決定する ##

        # 条件式(A,B合わせて急騰落が終了したタイミングとなる)
        A = df_f_state_judge['state_judge'][i] == 0 # 最新が0であること
        B = abs(df_f_state_judge['state_judge'][i - 1]) > 1 # 最新のひとつ前が急騰落であること

        if A and B:
            # 古い方から急騰落を見つける ★★★★このsave_pointの位置ちゃんとして
            s = 0 if self.ch_info.rf_last_date else df_candlestick[df_candlestick['time'] == self.ch_info.rf_last_date].index[0]
            
            # find_raise_or_fall_forwardprocessは、引数sを加えた状態でnumを計算する。 
            rf_start_num, end_judge  =   self.find_raise_or_fall_forwardprocess(df_f_state_judge, "start", s)
            rf_last_num, end_judge   =   self.find_raise_or_fall_forwardprocess(df_f_state_judge, "last", rf_start_num)
            # rf_second_start_num, end_judge  =   self.find_raise_or_fall_forwardprocess(df_f_state_judge, "start", rf_last_num) # 最後の場合は、最後の値を返却
            if end_judge: # 最後尾判定の場合は計算が中途半端になるので以降の処理はしない
                self.ch_info.rf_start_date  = df_candlestick['time'][rf_start_num]
                self.ch_info.rf_last_date   = df_candlestick['time'][rf_last_num]
                self.check_rf_result(rf_start_num, rf_last_num, df_candlestick, df_f_state_judge, i)

        self.channel_position_ctrl(rf_start_num, rf_last_num, df_candlestick, df_f_state_judge, i)


    def channel_describe_ctrl(self, i):
        pass


    def channel_ctrl(self, df_candle_200: pd.DataFrame, df_f_state_judge: pd.DataFrame):
        # セーブポイントからのchannel関数 全体制御 
        if self.cc.loop_count == 0:
            for i in range(len(df_candle_200.index) - 1):
                self.Channel_all_judge_ctrl(df_candle_200, df_f_state_judge, i) # 注意： iは0からスタート
                self.channel_describe_ctrl(i)
        else:
            self.Channel_all_judge_ctrl(df_candle_200, df_f_state_judge, i = self.cc.save_df_start_point)
            self.channel_describe_ctrl(i = self.cc.save_df_start_point)


    def data_ctrl(self, full_df_candlestick: pd.DataFrame):
        # 最新のキャンドル情報を取得 + dfを最新に更新。
        save_point = full_df_candlestick[full_df_candlestick['time'] == self.cc.save_df_start_date].index[0] # ★このindex[0]は数値を抽出する為のもの　★★2週目以降もこれで良いかはあとで確認すること。
        if self.f_simu and len(full_df_candlestick.index) >= save_point + se.INITIAL_DF_SIZE: # ★★ lenと[:]ではずれるので、200個取れる所までの条件は>なのか、>=なのかどうかチェックしなさい
            df = full_df_candlestick.iloc[save_point: save_point + se.INITIAL_DF_SIZE, :]
            return df, save_point
        elif self.f_simu and len(full_df_candlestick.index) < save_point + se.INITIAL_DF_SIZE:
            df = full_df_candlestick.iloc[ - se.INITIAL_DF_SIZE:, :]
            return df, save_point
        else:
            return df, save_point


    def one_action_start(self, full_df_candlestick: pd.DataFrame, df_f_state_judge: pd.DataFrame):
        # データの最新化
        df_candle_200 , self.cc.save_df_start_point = self.data_ctrl(full_df_candlestick)
        セーブポイントは、df_candlestick_200の始めの位置とする。名前変えるのと、save_pointやdateが違う使われ方してないか確認する。iは処理の現在値としたいし、処理のsave_pointも作るべき
        # 急落判定(2ループ目以降は、1ずらした値が返却される)
        df_f_state_judge = self.raise_fall_detection_ctrl(df_candle_200, self.CHANNEL_PLOT_INTERVAL, df_f_state_judge)

        # チャネル引き
        self.channel_ctrl(df_candle_200, df_f_state_judge)
        
        # 結果をcsvに残しておく。→ これをdbに残しておくのもあり？？
        # f_state_judgeに、time情報をがっちゃんこさせる
        # ★★結果は時刻を元に重複なく、がっちゃんこさせること。f_state_judgeは前後範囲分は上書きする

        # リアルタイム、シミュレーションどっちでも1ループごとに機械学習、予測までやるべき
        self.cc.save_df_start_date = full_df_candlestick['time'][0]

    def all_channel_ctrl(self, df_f_state_judge):
        '''
        チャネルを引いて、売買判断をするロジック。自動売買シミュレーションスタート
        '''
        if self.f_simu:
            # シミュレーション機能
            if self.cc.loop_count == 0:
                # 所望の足のローソク足データをcsvから取得
                full_df_candlestick = self.csvread.prepare_candledata_fromcsv(self.INI.set['csv_read']['filename'], self.CHANNEL_PLOT_INTERVAL)
            
            self.cc.save_df_start_date = full_df_candlestick['time'][0] if self.cc.loop_count == 0 else full_df_candlestick['time'][self.cc.loop_count]

        else:
            # リアルタイム用
            # データ取得APIにて、リアルタイムにデータ取得

            self.cc.save_df_start_date = full_df_candlestick['time'][0]

        self.one_action_start(full_df_candlestick, df_f_state_judge)
        self.cc.loop_count += 1

