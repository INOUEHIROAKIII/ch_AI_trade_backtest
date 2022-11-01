#_*_ coding: utf-8 _*_

# ***************************************************************************************************************************************************************************************
# 新アルゴリズム(= チャネルで判断bot)
    
    # 急騰落チェック（毎回）
        # ◇◇➀足で全体チャートの内、現価格の〇〇➀％の急騰落と、それ以外に分類する
            # 上昇の場合：前日のlowを当日のlowが超えない(= 〇〇➁何日間のlowを下回る)。超えてもcloseが陽線ならまだ上昇と考える。当日のlowが前日のlowを超え、陰線の場合、上昇は終了と考える。
            # 下落の場合：前日のhighを当日のhighが超えない(= 〇〇➁何日間のhighを上回る)。超えてもcloseが陰線ならまだ下落と考える。当日のhighが前日のhighを超え、陽線の場合、下落は終了と考える。
    
    
    # チャネル構成：
        # ◇◇➁足で実施
        # 第一チャネル：急騰落～次の急騰落までの間のチャネル
            # 急騰落の日足上下判断で、反発を検知したら、反発まででの急騰ならmax、急落ならminを取得し、１ローカル極値とする
                # その後、次の反発を２極値とする。〇〇➂日(前後2日等)でローカル極地とする
                # その後、３、４ローカル極値が出そろったら
                # １、２、３、４ローカル極値と回帰直線から第一チャネルを作成。

                    # # 第一チャネル構成

                        # A. maxライン(値ではなく、回帰直線に対して一番　＋側に遠いもの)
                        # C. 最頻max値：maxから中心に〇〇➃0.6%づつ近づけて行った時に〇〇➃0.6%の間にローカル極値が2個以上含まれているラインで最も外側
                        # D. 最頻min値：minから中心に〇〇➃0.6%づつ近づけて行った時に〇〇➃0.6%の間にローカル極値が2個以上含まれているラインで最も外側
                        # F. minライン(値ではなく、回帰直線に対して一番　ー側に遠いもの)
                            

                        # 1時間足が更新されるごとに回帰直線を更新する。このチャネルは次の急騰落が起きるまでリセットせずやり続ける。データ票プロットは赤色。
                        # ある程度更新したら固定するのも必要　★★どれくらいで固定するかは試作したい（→ ローカル極値が〇〇➄個以上溜まったら、直近5日間とかは傾きの考慮に入れない）。多分6個でほぼ固定して良さそうにみえる。tradingviewでローカル極値数とチャネルの正確性は実践したい
                                                            
                            
                    # チャネル更新
                    
                        # 極値が更新される度に、場合分けの処理が必要

                            # 極値がチャネルの内側に留まる場合
                                # 最頻ラインの更新   

                            # 極値がチャネルの外側に出る場合
                                # max,minラインの更新
                                # 〇〇➀％の急騰落の動きがない場合は、第一チャネルは捨てない





        # 急騰落は0.1%ｘ3000円　かつ　レンジの幅(直前の急騰落を保存しておいて、それより1.5倍未満の物はチャネル範囲内で急騰落とはしない)
        # 現在地がチャネルの範囲かける1.1倍以内なら急騰落とはしない
        # 抜けた場合、これはなし。。。。。。。。。。。それが急騰落と判定されない場合は、25日線を見て、それが切り返されるまでは継続すると考え,そこまでのmax or minで考える
        # 抜けた場合(急騰落ではない)、(約2日でチャネルに戻ってこない)は再度、チャネルを抜けた箇所からまたチャネルの引き直し処理に移行するしかない。ただし、local valueが〇〇個以下の場合は拡充する。
        # 第２max or minがない場合の対応：max or minと同地とする



# チャネル関連。あらゆる状況を想定した場合
    # localvalueが1～4以下の場合
    # localvalueが4～〇〇以下の場合
    # localvalueが〇〇以上の場合
      # 急騰落があった場合
      # チャネルブレイクがあったが微小な場合
        # 1～2日で戻ってくる場合
        # 2日で戻らない場合
        




        
    # エントリー、クローズロジック
        
        # エントリー
            # 急騰落後に、〇〇➅　４ローカル極値が決定したタイミングからエントリーができるようにする
            # ◇◇➂足　25日線、50日線、75日線の全てが揃っていない場合、ブレイクするとは思わない。逆張りで推進。
            # 3つの全てが揃っている場合は、
                # ◇◇➃足でライン幅の10%戻したら(クローズで考える or ブレイクアウトの考え)、10%の戻りはその時、下まで行かないこともあるからそれに対して10%の戻り。逆張りエントリーとポジションあれば逆張り方向のクローズ。
                # ◇◇➃足でラインを割った。◇◇⑤足でcloseがbreakしていたら、順張り。すでに順張りのポジションを持っている場合は継続して持ち続ける。
            
            # イレギュラー
                # 反発が弱い。
                    # エントリー後にエントリー側2.5割まで回復到達しないで、引き返してきた場合(日足上下判断)、勢いが弱いので、エントリー側を清算して、反対側でエントリー(ドテン)


        # クローズ
            # 逆sideのエントリーが出るタイミングでclose処理を実施。



        # ポジション毎　挙動

            # A,C,D,F共通
        
            # pos == 0
                # buy entry : 
                # sell entry : 
    
            # pos == 1
                # buy close : 

            # pos == -1 
                # sell close : 


        # フラグ
            # 中途半端切り返し対応。エントリー、クローズフラグ
                # 更に細かい足に切り替えて、RSIを計算。30～45%（or 55～70%）に入ったら、下限フラグを立てる。
                # 上限で決済したら、初期化

                # → フラグがTrueの場合、切り返しで決済する。ライン幅が規定以上ならドテンエントリーもする


        # 損切ライン
            # レジサポラインを基準に考える
# ***************************************************************************************************************************************************************************************


import pandas as pd
import numpy as numpy
import configparser
import math
from dataclasses import dataclass
from sklearn.linear_model import LinearRegression
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

class trade_algorithm_2:

    def __init__(self):
        self.config = configparser.ConfigParser()
        self.debug = debug_matplot.debug_plot()
        self.config.read('set.ini',encoding="utf-8")
        self.rf_val = self.config['raise_fall_detection']
        self.ch_val = self.config['channel_describe']
        self.debug_val = self.config['debug']
        self.local_ext_value = {
            "local_side": [],
            "y_value": [],
            "index": [],
            "length": float,
            "first_index": int
        }
        self.line_regression    =   trend_channel(0, 0, 0, 0)
        self.max_channel        =   trend_channel(0, 0, 0, 0)
        self.min_channel        =   trend_channel(0, 0, 0, 0)
        self.second_max_channel =   trend_channel(0, 0, 0, 0)
        self.second_min_channel =   trend_channel(0, 0, 0, 0)
        self.start_channel  =   int(self.ch_val["start_channel"])
        self.ch_max, self.ch_2_max, self.ch_2_min, self.ch_min = [], [], [], []
        self.dx = 0
        self.distance_high, self.distance_low = {"index": numpy.empty(0),"value": numpy.empty(0)},{"index": numpy.empty(0),"value": numpy.empty(0)}
        self.renge = {
            "max": 0.0,
            "min": 0.0,
            "renge_width": 0.0,
            "fall_raise_value": 0.0
        }

    
    def raise_fall_detection(self, df_candlestick: pd.DataFrame, candle_intarval, f_state_judge, i):
        '''
        # 急騰落チェック（毎回）
        # 渡されたデータ（◇◇➀足）で全体チャートの内、現価格の〇〇➀％の急騰落と、それ以外に分類する
            # 上昇の場合 : 前日のlowを当日のlowが超えない(= ➁何日間のlowを下回る)。超えてもcloseが陽線ならまだ上昇と考える。当日のlowが前日のlowを超え、陰線の場合、上昇は終了と考える。
            # 下落の場合 : 前日のhighを当日のhighが超えない(= ➁何日間のhighを上回る)。超えてもcloseが陰線ならまだ下落と考える。当日のhighが前日のhighを超え、陽線の場合、下落は終了と考える。
        # return 配列f_state_judge（レンジ = 0、急騰 = 2、急落= -2）
        注意:必ず0:00から始まるデータであること(1分足から日足へ加工する場合)。
        '''

        # 複数の時間足に対応
        candle_num  =   int(self.rf_val["candle_num_"       +    CANDLE_INTARVAL[str(candle_intarval)]])
        a1          =   float(self.rf_val["raise_rate1_"    +    CANDLE_INTARVAL[str(candle_intarval)]])
        a2          =   float(self.rf_val["raise_rate2_"    +    CANDLE_INTARVAL[str(candle_intarval)]])
        a3          =   float(self.rf_val["raise_rate3_"    +    CANDLE_INTARVAL[str(candle_intarval)]])
        a4          =   float(self.rf_val["raise_rate4_"    +    CANDLE_INTARVAL[str(candle_intarval)]])
        a5          =   float(self.rf_val["raise_rate5_"    +    CANDLE_INTARVAL[str(candle_intarval)]])
        raise_value =   int(self.rf_val["raise_value_"      +    CANDLE_INTARVAL[str(candle_intarval)]])
        fluc_term   =   int(self.rf_val["fluc_term_"        +    CANDLE_INTARVAL[str(candle_intarval)]])

        # 急峻を判定。１，繋がっていて、２，一定以上に変動があること
        
        if (i >= candle_num):
            change_val_high = max(df_candlestick["high"][i - candle_num + 1 : i + 1])
            change_val_low  = min(df_candlestick["low"][i - candle_num + 1 : i + 1])
            xp = df_candlestick["close"][i - candle_num]
            
            if change_val_high - change_val_low > a1 * xp ** (5) + a2 * xp ** (4) + a3 * xp ** (3) + a4 * xp ** (2) + a5 * xp + raise_value:
                max_index = numpy.argmax(df_candlestick["high"][i - candle_num + 1 : i + 1])
                min_index = numpy.argmin(df_candlestick["low"][i - candle_num + 1 : i + 1])
                self.renge["fall_raise_value"] = change_val_high - change_val_low

                if   max_index > min_index:
                    # 急騰と判断。上書き禁止風  ★★ただし、上がって下がっての可能性も全然ありえるので、必ずどちらか一つであろう3毎に分けて判断。対応必要ないかも
                    
                    for j in range(max_index - min_index + 1):
                        f_state_judge[i - candle_num + min_index + j + 1] = 2 if f_state_judge[i - candle_num + min_index + j + 1] == 0 else f_state_judge[i - candle_num + min_index + j + 1]

                elif max_index < min_index:
                    # 急落と判断。上書き禁止風 

                    for j in range(min_index - max_index + 1):
                        f_state_judge[i - candle_num + max_index + j + 1] = -2 if f_state_judge[i - candle_num + max_index + j + 1] == 0 else f_state_judge[i - candle_num + max_index + j + 1]

                elif max_index == min_index:
                    # ハイボラティリティ、openとcloseから陽線か陰線かを特定
                    if f_state_judge[i - candle_num + max_index + 1] == 0:
                        f_state_judge[i - candle_num + max_index + 1] = -2 if df_candlestick["open"][i - candle_num + max_index + 1] > df_candlestick["close"][i - candle_num + max_index + 1] else 2
    

            # 上昇、下落の終了を判断する
            # 上昇の場合：前日のlowを当日のlowが超えない。超えてもcloseが陽線ならまだ上昇と考える。当日のlowが前日のlowを超え、陰線の場合、上昇は終了と考える。
            if f_state_judge[i-1] == 2 and f_state_judge[i] == 0:
                
                low         = min([price for price in df_candlestick["low"][i-fluc_term:i]])  # 一つ前までに結果
                close_min   = min([price for price in df_candlestick["close"][i-fluc_term:i]])
                
                if df_candlestick["low"][i] < low and df_candlestick["close"][i] < close_min:
                    f_state_judge[i] = 0
                    # f_state_judge = self.judge_renge_for_rf_detect(df_candlestick, f_state_judge, self.renge["fall_raise_value"])　# 妥当性検証は次のチャネル引く際に包含する
                elif  not (df_candlestick["low"][i] < low) or not (df_candlestick["close"][i] < close_min):
                    f_state_judge[i] = 2

            # 下落の場合：前日のhighを当日のhighが超えない。超えてもcloseが陰線ならまだ下落と考える。当日のhighが前日のhighを超え、陽線の場合、下落は終了と考える。
            elif f_state_judge[i-1] == -2 and f_state_judge[i] == 0:

                high        = max([price for price in df_candlestick["high"][i-fluc_term:i]]) # 一つ前までに結果
                close_max   = max([price for price in df_candlestick["close"][i-fluc_term:i]])
                
                if df_candlestick["high"][i] > high and df_candlestick["close"][i] > close_max:
                    f_state_judge[i] = 0
                    # f_state_judge = self.judge_renge_for_rf_detect(df_candlestick, f_state_judge, self.renge["fall_raise_value"])　# 妥当性検証は次のチャネル引く際に包含する
                elif  (df_candlestick["high"][i] < high) or (df_candlestick["close"][i] < close_max):
                    f_state_judge[i] = -2

        return f_state_judge
        
    
    def raise_fall_detection_ctrl(self,df_candlestick: pd.DataFrame, candle_intarval, df_f_state_judge: pd.DataFrame, detect_start):
        '''
        逐一実行用。df_state_judgeは、はじめは、500の空のデータフレームを引数に入力する必要あり。以降は返却値を再度引数に指定するだけ。追加の部分だけやる。
        '''
        # リストに変更
        f_state_judge = df_f_state_judge['state_judge'].to_list()
        # print(f_state_judge)

        if detect_start:
            # 値が空欄の場合
            # iをdf_candlestickの長さ分回す。# loopでは、500程度。シミュレーションでは、1万以上
            for i in range(len(df_candlestick.index)):
                f_state_judge = self.raise_fall_detection(df_candlestick, candle_intarval, f_state_judge, i)
        else:
            # 値がある場合
            # 1ずらす
            c = f_state_judge[1:]
            d = [0]
            f_state_judge = c + d

            # iに最後尾の値を代入
            f_state_judge = self.raise_fall_detection(df_candlestick, candle_intarval, f_state_judge, (len(df_candlestick.index) - 1))
        
        df_f_state_judge = pd.DataFrame({'state_judge': f_state_judge})

        return df_f_state_judge

    # ----------------------- 急騰落_妥当性ジャッジ-----------------------------------------------------------------------
    def culculate_renge(self, df_candlestick: pd.DataFrame, rf_last_num_before, rf_start_num):
        '''
        急騰落後のなんちゃってレンジ相場を仮定し、max,minと値幅を算出する。
        '''
        # 傾きのみ計算。切片も要らない。適当に0を代入
        line_regression_slope, _, _ = self.linear_regression(df_candlestick, 0)
        # print(line_regression_slope)
        
        # レンジの中のmin,maxを算出
        max_value = max(df_candlestick["high"][rf_last_num_before + 1: rf_start_num])
        min_value = min(df_candlestick["low"][rf_last_num_before + 1: rf_start_num])
        max_index = numpy.argmax(df_candlestick["high"][rf_last_num_before + 1: rf_start_num])
        min_index = numpy.argmin(df_candlestick["low"][rf_last_num_before + 1: rf_start_num])
        # print(max_value)
        # print(min_value)
        # print(max_index)
        # print(min_index)

        if line_regression_slope >= 0:
            max_value_ad = max_value
            min_value_ad = min_value + line_regression_slope * (rf_start_num - 1 - min_index)
        else:
            max_value_ad = max_value - line_regression_slope * (rf_start_num - 1 - max_index)
            min_value_ad = min_value
        # print(max_value_ad)
        # print(min_value_ad)

        return (max_value_ad, min_value_ad, (max_value_ad - min_value_ad))

    def judge_renge_for_rf_detect(self, df_candlestick: pd.DataFrame, f_state_judge: list, fall_raise_value):
        '''
        急騰落の判定後に、その妥当性を判断し、レンジと判断した場合は修正する。
        '''
        # 急騰落の位置を特定       
        df_f_state_judge = pd.DataFrame({'state_judge': f_state_judge})
            
        rf_last_num, _ , _ , flug               =   self.find_raise_or_fall_backprocess(df_f_state_judge, "last", len(df_f_state_judge.index) - 1, 0) # 必ず最後尾1個手前になるはず
        rf_start_num, _ , double_judge, flug    =   self.find_raise_or_fall_backprocess(df_f_state_judge, "start", rf_last_num, flug)
        rf_last_num_before, _ , _ , flug        =   self.find_raise_or_fall_backprocess(df_f_state_judge, "last", rf_start_num, flug) # ない場合は0が代入される

        # # レンジ幅の計算ただし、rf_last_num_beforeとrf_start_numの間が1の場合はエラーが起きるので、更に一つ前で考える
        if rf_start_num - rf_last_num_before > 1 and double_judge == False: # 急騰落の間隔が1日以上あり、レンジの計算が出来る場合。注：一番始めの急騰落はlast_num_beforeが0となり、rengeの計算が厳密には出来ないが、重要度高くないのでやってしまう。
            
            self.renge["max"], self.renge["min"], self.renge["renge_width"] = self.culculate_renge(df_candlestick, rf_last_num_before, rf_start_num)
            f_state_judge = self.out_of_renge_judge(df_candlestick, rf_last_num, rf_start_num, self.renge["min"], self.renge["max"], self.renge["renge_width"], f_state_judge, 0, fall_raise_value)
        
        elif (rf_start_num - rf_last_num_before <= 1 or double_judge) and self.renge["renge_width"] != 0.0: # 急騰落の間隔が0 or 1の場合　、レンジの計算が出来ないので、前回のレンジ計算結果を使用する
            
            f_state_judge = self.out_of_renge_judge(df_candlestick, rf_last_num, rf_start_num, self.renge["min"], self.renge["max"], self.renge["renge_width"], f_state_judge, 1, fall_raise_value)
        
        elif (rf_start_num - rf_last_num_before <= 1 or double_judge) and self.renge["renge_width"] == 0.0:
            print("急騰落の妥当性検証を実施したいが、一番始めに十分なレンジがありません。多分急騰落の間隔が0 or 1であるデータが始めに来てしまっています")

        return f_state_judge

    def out_of_renge_judge(self, df_candlestick, rf_last_num, rf_start_num, min_value_just_before, max_value_just_before, width_value, f_state_judge, flug, fall_raise_value):
        # 特殊条件定義
        condition_A = fall_raise_value > width_value
        condition_B = df_candlestick["low"][rf_last_num] < min_value_just_before - width_value/3
        condition_C = df_candlestick["high"][rf_last_num] > max_value_just_before + width_value/3

        # フラグで処理を分けている理由は、真逆の急騰落が続いている場合は、レンジの位置と急騰落後の位置が定義できないから
        if flug == 0:
            if not condition_B or not condition_C:
                # 急騰落はレンジの中と判断して、f_state_judgeの該当箇所を0へ変更
                for n in numpy.arange(rf_start_num + 1, rf_last_num + 1, 1):
                    f_state_judge[n] = 0
        elif flug == 1:
            if not condition_A:
                # 急騰落はレンジの中と判断して、f_state_judgeの該当箇所を0へ変更
                for n in numpy.arange(rf_start_num + 1, rf_last_num + 1, 1):
                    f_state_judge[n] = 0

        return f_state_judge
    # ----------------------- 急騰落_妥当性ジャッジ　終わり-----------------------------------------------------------------------


    def channel_describe(self, start_num, last_num, df_candlestick_forfirst: pd.DataFrame, df_candlestick: pd.DataFrame, df_candlestick_marge: pd.DataFrame, f_side ,candle_intarval):
        '''
        ローソク足が更新される度に、チャネルを引き直す
        '''
        # ---------------ローカル極値を格納する--------------------------
        # 急変動終了時に、最高値もしくは、最安値を見つける # ★★df_candleは所望の場所も取り込めている？
        if self.local_ext_value["local_side"] == [] : # ★★初期化対象 distanceも
            if f_side == 2:
                self.local_ext_value["local_side"].append("high")
                self.local_ext_value["y_value"].append(max(df_candlestick_forfirst["high"]))
                self.local_ext_value["index"].append(0) # ★★ 確認
                self.local_ext_value["length"] = len(df_candlestick_forfirst)
                self.local_ext_value["first_index"] = df_candlestick_forfirst["high"].idxmax()
            else:
                self.local_ext_value["local_side"].append("low")
                self.local_ext_value["y_value"].append(min(df_candlestick_forfirst["low"]))
                self.local_ext_value["index"].append(0)
                self.local_ext_value["length"] = len(df_candlestick_forfirst)
                self.local_ext_value["first_index"] = df_candlestick_forfirst["low"].idxmax()
        else:
            # レンジ開始以降のローカル極値をジャッジ(retrun:値とside,index。ない場合は0,"None"が返却。ローソク足が更新されるたびに後ろから計算するので重複はない)
            local_value, local_side, x_index = self.find_local_ext_value(df_candlestick, candle_intarval)

            if x_index >= 0:
                self.local_ext_value["local_side"].append(local_side)
                self.local_ext_value["y_value"].append(local_value)
                self.local_ext_value["index"].append(x_index + self.local_ext_value["length"] - self.local_ext_value["first_index"] + 1) # このまま配列に代入して良い値
        # --------------------------------------------------------------
        print(self.local_ext_value)

        # -----------------------最小二乗法------------------------------
        # ローカル極値の数が○○個以上になったら最小二乗法で傾きと切片を計算。y=ax+b
        if self.local_ext_value["local_side"].count("high") >= self.start_channel and self.local_ext_value["local_side"].count("low") >= self.start_channel:
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
            
            for n in numpy.arange(self.dx, length_df, 1): # ★★ self.dxは初期化対象。 length.dfは最後尾を表している
                if self.local_ext_value["local_side"][n] == "high":
                    x0 = self.local_ext_value["index"][n]
                    # x0 = self.local_ext_value["index"][n] + (self.local_ext_value["length"] - self.local_ext_value["index"][0]) if n != 0 else 0 # 最初の極値まで含む計算式にしている。x0は配列に代入する値。0から数えて。。
                    y0 = self.local_ext_value["y_value"][n]
                    self.distance_high["value"] = numpy.append(self.distance_high["value"], abs(-self.line_regression.slope * x0 + 1 * y0 + (-self.line_regression.intercept)) / math.sqrt(self.line_regression.slope ** (2) + 1 ** (2))) # ★★self.local_ext_valueのnの位置がおかしい
                    self.distance_high["index"] = numpy.append(self.distance_high["index"], x0)

                if self.local_ext_value["local_side"][n] == "low":
                    x0 = self.local_ext_value["index"][n]
                    # x0 = self.local_ext_value["index"][n] + (self.local_ext_value["length"] - self.local_ext_value["index"][0]) if n != 0 else 0 # 最初の極値まで含む計算式にしている。x0は配列に代入する値。0から数えて。。
                    y0 = self.local_ext_value["y_value"][n]
                    self.distance_low["value"] = numpy.append(self.distance_low["value"], abs(-self.line_regression.slope * x0 + 1 * y0 + (-self.line_regression.intercept)) / math.sqrt(self.line_regression.slope ** (2) + 1 ** (2)))
                    self.distance_low["index"] = numpy.append(self.distance_low["index"], x0)
            self.dx = length_df

            # -------------------- 第１チャネルを計算する ------------------------------
            
            # max側
            self.max_channel.x0         =   self.distance_high["index"][numpy.argmax(self.distance_high["value"])]
            self.max_channel.y0         =   df_candlestick_marge["high"][self.max_channel.x0 + self.local_ext_value["first_index"]+1]
            self.max_channel.slope      =   self.line_regression.slope
            self.max_channel.intercept  =   self.max_channel.y0 - self.max_channel.x0 * self.max_channel.slope

            # min側
            self.min_channel.x0         =   self.distance_low["index"][numpy.argmax(self.distance_low["value"])]
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
    
    def channel_describe_forloop(self,df_f_state_judge, df_candlestick, candle_intarval):

        # 最後の急騰落を見つける
        data = False
        last_num = 0
        while not data:
            last_num += 1
            data = True if abs(df_f_state_judge['state_judge'][-1*last_num]) > 1 else False
        
        data = False
        start_num = last_num
        while not data:
            start_num += 1
            data = True if abs(df_f_state_judge['state_judge'][-1*start_num]) == 0 else False


    def find_raise_or_fall_forwardprocess(self, df_f_state_judge: pd.DataFrame, find_side, num_in_progress):
        '''
        チャネル引く時に使用。
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
    
    def find_raise_or_fall_backprocess(self, df_f_state_judge: pd.DataFrame, find_side, progress_last_number, flug):
        '''
        急騰落の妥当性確認の為に使用。
        '''
        rf_judge = False
        num = progress_last_number # len() - 1
        double_judge = False

        while not rf_judge:
            num -= 1
            
            if num <= 0:
                return (0, True, double_judge, 0)

            if flug == 0:
                if find_side == "last":
                    rf_judge = True if abs(df_f_state_judge['state_judge'][num]) > 1 else False
                    flug2 = df_f_state_judge['state_judge'][num]
                elif find_side == "start":
                    rf_judge = True if abs(df_f_state_judge['state_judge'][num]) == 0 else False
                    flug2 = df_f_state_judge['state_judge'][num]

            if flug != 0:
                if find_side == "last":
                    rf_judge        = True if abs(df_f_state_judge['state_judge'][num]) > 1 else False
                    double_judge    = True if abs(df_f_state_judge['state_judge'][num]) == flug * (-1) else False
                    flug2 = df_f_state_judge['state_judge'][num]
                    if double_judge:
                        return (num, False, double_judge, flug2)
                elif find_side == "start":
                    rf_judge = True if abs(df_f_state_judge['state_judge'][num]) == 0 else False
                    double_judge    = True if abs(df_f_state_judge['state_judge'][num]) == flug * (-1) else False
                    flug2 = df_f_state_judge['state_judge'][num]
                    if double_judge:
                        return (num, False, double_judge, flug2)
                
        return (num, False, double_judge, flug2)

    def ss(self, start, end, df_f_state_judge: pd.DataFrame, target):
        same_judge = True
        num = end - start
        while same_judge:
            num -= 1
            same_judge = False if df_f_state_judge['state_judge'][num] == target * (-1) else True
            if num <= 1:
                return start
        return num
    
    def find_local_ext_value(self, df_candlestick: pd.DataFrame, candle_intarval):
        '''
        ローカル極値を見つける
        '''
        # 複数の時間足に対応
        local_term_after    =   int(self.ch_val["local_term_after_"      +    CANDLE_INTARVAL[str(candle_intarval)]])
        local_term_before   =   int(self.ch_val["local_term_before_"     +    CANDLE_INTARVAL[str(candle_intarval)]])
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
    
    
    # def linear_regression(self, df_candlestick: pd.DataFrame):
    #     if (len(df_candlestick.index) >= 1):    
    #         # ステップ1：時間軸の平均
    #         df_length = len(df_candlestick["close"].index)
    #         time_average = df_length / 2
    #         distribution_xy = 0

    #         # ステップ2：終値の平均値
    #         close_price_average = df_candlestick["close"].mean()

    #         # ステップ3：分散,共分散を求める
    #         distribution_x = df_candlestick["close"].var()

    #         for i in range(df_length):
    #             distribution_xy += (i - time_average)*(df_candlestick["close"][i] - close_price_average)
    #         distribution_xy = distribution_xy/df_length

    #         #ステップ4：傾きを求める
    #         slope = distribution_xy/distribution_x
            
    #         # ステップ5 : 切片を導出
    #         intercept = close_price_average - slope * time_average

    #         # #ステップ5：規格化
    #         # slope = slope/close_price_average
    #         return (slope, intercept)
    #     return (1, 1)







    # def lpass_filter_1(self,dflist_candlestick):
    #     # 1次のローパスフィルタ

    #     df_candlestick

    #     pass

    # def lpass_filter_2(self,dflist_candlestick):
    #     # 2次のローパスフィルタ

    #     df_candlestick

    #     pass

    # def chart_diff(self,data):
    #     # グラフを微分して返す
    #     diff = [0 for i in range(len(data.index))]
    #     for i in range(len(data.index)):
    #         diff[i+1] = data[i+1] - data[i] # detaはリスト
    #     return diff

    # def state_judgement(self,df_candlestick,f_state_judge):
    #     # 急騰落の間のレンジをUP,DOWN,フラットのレンジ分けをする。日足で見やすいようにローパスをかける。よって傾きの転換点がトレンドの転換点と判断できる
    #     # 微分をして、目的の転換点を見つけられる加工がしたい
    #     # トレンドが途中で途切れないようにする
    #     # return 配列（上昇トレンドレンジ = 1、レンジ = 0、下降トレンドレンジ = -1）
    #     # filter
    #     data = self.lpass_filter_1(df_candlestick["close"])
    #     dflist_after_filter = self.lpass_filter_2(data)

    #     # 微分
    #     diff_close = self.chart_diff(data)
    #     return (dflist_after_filter,diff_close)
    
    # def uu():
    #     # チャネルから少し抜けた後に戻ってくる時の処理
    #     # チャネル情報は保存して置き、また適用する。ブレイクしたラインも追加する
    #     pass

    # def dd():
    #     # 平均2乗で渡されたデータの傾きを算出する。これ要らんかも。上の傾きデータと比較してみる
    #     pass

    # def ff():
    #     # high,lowからローカルhigh,lowを入れるリストを作成する
    #     pass

    # def ddff():
    #     # ローカルhigh,lowの傾きを算出
    #     # 同じレンジ内のデータの傾きと比較
    #     pass

    # def jj():
    #     # デバック用。上記をプロットしてうまく言っているか確認する
    #     pass

    # def additional_channel():
    #     # 反発する所が多い。意識されているチャネルか判断。ムリゲー
    #     pass

    # "↓ 以下、だめそうな気しかしない"
    # # def ll():
    # #     # わからんが、ボリンジャーバンド計算
    # #     pass

    # # def oo():
    # #     # ボリンジャーバンドの中＋チャネルの上下限の場合は逆張り
    # #     # ボリンジャーバンドの外＋チャネルの上下限の場合は順張り
    # #     pass

    # def rr():
    #     # 引数で渡されたチャネルの上限と下限の差が0.06%の手数料でも十分勝てる幅か判断する
    #     # return True or False
    #     pass
    
    # def aa():
    #     # チャネルを10分割。反発を検知した場合は全部売る。これは、トレンドの逆らうエントリの場合
    #     pass

    # def bb():
    #     # 
    #     pass

    '''
    def judgeForLoop(self, high, low, entryHighLine, entryLowLine, closeHighLine, closeLowLine):
        """
        最終的に、情報を組み合わせて、judgementを計算する。0=なにもしない。1=エントリー or クローズする
        """
        judgement = [0,0,0,0]
        #上抜けでエントリー
        if high > entryHighLine[-1]:# `entryHighLine[-1]` で直近のentryTerm期間の高値を取得できます。その値を直近約定30件の高値が超えていれば、買いエントリーを1にします。
            judgement[0] = 1
        #下抜けでエントリー
        if low < entryLowLine[-1]:
            judgement[1] = 1
        #下抜けでクローズ
        if low < closeLowLine[-1]:
            judgement[2] = 1
        #上抜けでクローズ
        if high > closeHighLine[-1]:
            judgement[3] = 1
        return judgement
    '''


    # def raise_fall_detection(self,df_candlestick, candle_intarval, f_state_judge):
    #     '''
    #     # 急騰落チェック（毎回）
    #     # 渡されたデータ（◇◇➀足）で全体チャートの内、現価格の〇〇➀％の急騰落と、それ以外に分類する
    #         # 上昇の場合：前日のlowを当日のlowが超えない(= 〇〇➁何日間のlowを下回る)。超えてもcloseが陽線ならまだ上昇と考える。当日のlowが前日のlowを超え、陰線の場合、上昇は終了と考える。
    #         # 下落の場合：前日のhighを当日のhighが超えない(= 〇〇➁何日間のhighを上回る)。超えてもcloseが陰線ならまだ下落と考える。当日のhighが前日のhighを超え、陽線の場合、下落は終了と考える。
    #     # return 配列f_state_judge（レンジ = 0、急騰 = 2、急落= -2）
    #     '''

    #     # 複数の時間足に対応
    #     candle_num  =   int(self.rf_val["candle_num_"   +    CANDLE_INTARVAL[str(candle_intarval)]])
    #     raise_rate  =   float(self.rf_val["raise_rate_" +    CANDLE_INTARVAL[str(candle_intarval)]])
    #     fall_rate   =   float(self.rf_val["fall_rate_"  +    CANDLE_INTARVAL[str(candle_intarval)]])
    #     raise_value =   int(self.rf_val["raise_value_"  +    CANDLE_INTARVAL[str(candle_intarval)]])
    #     fall_value  =   int(self.rf_val["fall_value_"   +    CANDLE_INTARVAL[str(candle_intarval)]])
    #     fluc_term   =   int(self.rf_val["fluc_term_"    +    CANDLE_INTARVAL[str(candle_intarval)]])

    #     # 急峻を判定。１，繋がっていて、２，一定以上に変動があること
    #     for i in range(len(df_candlestick.index)):
    #         if (i >= candle_num):
    #             change_val_high = max(df_candlestick["high"][i - candle_num + 1 : i + 1])
    #             change_val_low  = min(df_candlestick["low"][i - candle_num + 1 : i + 1])

    #             print(change_val_high - change_val_low)
    #             print(df_candlestick["close"][i - candle_num])

    #             if change_val_high - change_val_low > df_candlestick["close"][i - candle_num]*raise_rate + raise_value:
    #                 max_index = numpy.argmax(df_candlestick["high"][i - candle_num + 1 : i + 1])
    #                 min_index = numpy.argmin(df_candlestick["low"][i - candle_num + 1 : i + 1])

    #                 if   max_index > min_index:
    #                     # 急騰と判断。上書き禁止風  ★★ただし、上がって下がっての可能性も全然ありえるので、必ずどちらか一つであろう3毎に分けて判断。対応必要ないかも
                        
    #                     for j in range(max_index - min_index + 1):
    #                         f_state_judge[i - candle_num + min_index + j + 1] = 2 if f_state_judge[i - candle_num + min_index + j + 1] == 0 else f_state_judge[i - candle_num + min_index + j + 1]

    #                 elif max_index < min_index:
    #                     # 急落と判断。上書き禁止風 

    #                     for j in range(min_index - max_index + 1):
    #                         f_state_judge[i - candle_num + max_index + j + 1] = -2 if f_state_judge[i - candle_num + max_index + j + 1] == 0 else f_state_judge[i - candle_num + max_index + j + 1]

    #                 elif max_index == min_index:
    #                     # ハイボラティリティ、openとcloseから陽線か陰線かを特定
    #                     if f_state_judge[i - candle_num + max_index + 1] == 0:
    #                         f_state_judge[i - candle_num + max_index + 1] = -2 if df_candlestick["open"][i - candle_num + max_index + 1] > df_candlestick["close"][i - candle_num + max_index + 1] else 2
        

    #             # 上昇、下落の終了を判断する
    #             # 上昇の場合：前日のlowを当日のlowが超えない。超えてもcloseが陽線ならまだ上昇と考える。当日のlowが前日のlowを超え、陰線の場合、上昇は終了と考える。
    #             if f_state_judge[i-1] == 2 and f_state_judge[i] == 0:
                    
    #                 low         = min([price for price in df_candlestick["low"][i-fluc_term:i]])  # 一つ前までに結果
    #                 close_min   = min([price for price in df_candlestick["close"][i-fluc_term:i]])
                    
    #                 if df_candlestick["low"][i] < low and df_candlestick["close"][i] < close_min:
    #                     f_state_judge[i] = 0
    #                 elif  not (df_candlestick["low"][i] < low) or not (df_candlestick["close"][i] < close_min):
    #                     f_state_judge[i] = 2

    #             # 下落の場合：前日のhighを当日のhighが超えない。超えてもcloseが陰線ならまだ下落と考える。当日のhighが前日のhighを超え、陽線の場合、下落は終了と考える。
    #             elif f_state_judge[i-1] == -2 and f_state_judge[i] == 0:

    #                 high        = max([price for price in df_candlestick["high"][i-fluc_term:i]]) # 一つ前までに結果
    #                 close_max   = max([price for price in df_candlestick["close"][i-fluc_term:i]])
                    
    #                 if df_candlestick["high"][i] > high and df_candlestick["close"][i] > close_max:
    #                     f_state_judge[i] = 0
    #                 elif  (df_candlestick["high"][i] < high) or (df_candlestick["close"][i] < close_max):
    #                     f_state_judge[i] = -2

    #     print(f_state_judge)
    #     df_f_state_judge = pd.DataFrame({'state_judge':f_state_judge})  

    #     return df_f_state_judge