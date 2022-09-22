#_*_ coding: utf-8 _*_
import pandas as pd

class trade_algorithm:
    
    def __init__(self):
        pass
    
    def judgeForLoop(self, high, low, entryHighLine, entryLowLine, closeHighLine, closeLowLine):
            """
            売り買い判断．入力した価格が期間高値より高ければ買いエントリー，期間安値を下抜けたら売りエントリー．judgementリストは[買いエントリー，売りエントリー，買いクローズ（売り），売りクローズ（買い）]のリストになっている．（値は0or1）
            ローソク足は1分ごとに取得するのでインデックスが-1のもの（現在より1本前）をつかう．
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


    def calculateLines(self, df_candleStick, term):
            """
            期間高値・安値を計算する．
            candleStickはcryptowatchのローソク足．termは安値，高値を計算する期間．（5ならローソク足5本文の安値，高値．)
            """
            lowLine = []
            highLine = []
            for i in range(len(df_candleStick.index)):# 行数分 = ローソク足の本数分
                if i < term:
                    lowLine.append(df_candleStick["high"][i])# iがtermより小さければ、lowLineにはローソク足の高値を、highLineにはローソク足の安値を入れています。
                    highLine.append(df_candleStick["low"][i])# 逆？？
                else:
                    low = min([price for price in df_candleStick["low"][i-term:i]])# ローソク足の安値の `i-term` から `i` 未満の配列番号のpriceが入った配列を生成しています。これを `min()` で囲っているので、この範囲の安値の中で一番小さい値がlowに入ります。逆にこの範囲の高値の中で一番大きい値がhighに入ります。low, highそれぞれlowLine, highLineにappendされます。
                    high = max([price for price in df_candleStick["high"][i-term:i]])
                    lowLine.append(low)
                    highLine.append(high)
            return (lowLine, highLine)


    def calculatePriceRange(self, df_candleStick, term):
            """
            termの期間の値幅を計算．
            """
            low = [min([df_candleStick["close"][i-term+1:i].min(),df_candleStick["open"][i-term+1:i].min()]) for i in range(len(df_candleStick.index))]
            high = [max([df_candleStick["close"][i-term+1:i].max(), df_candleStick["open"][i-term+1:i].max()]) for i in range(len(df_candleStick.index))]
            low = pd.Series(low)
            high = pd.Series(high)
            priceRange = [high.iloc[i]-low.iloc[i] for i in range(len(df_candleStick.index))]
            return priceRange
   
    
    def isRange(self,df_candleStick ,term, th):
            """
            レンジ相場かどうかをTrue,Falseの配列で返す．termは期間高値・安値の計算期間．thはレンジ判定閾値．
            """
            #値幅での判定．
            if th != None:
                priceRange = self.calculatePriceRange(df_candleStick, term)
                isRange = [th > i for i in priceRange]# >>> priceRange = [1,2,3,4,5,6,7,8,9,0]>>> th = 4>>> isRange = [th > i for i in priceRange]>>> print(isRange)[True, True, True, False, False, False, False, False, False, True]
            #終値の標準偏差の差分が正か負かでの判定．
            elif th == None and term != None:
                df_candleStick["std"] = [df_candleStick["close"][i-term+1:i].std() for i in range(len(df_candleStick.index))]# for以下は以前と同じでローソク足の要素数分iを加算して繰り返します。`std()` することで対象期間内の終値の標準偏差を取得しています。df_candleStick["std"]には、対象期間内の終値の標準偏差が入ります。
                df_candleStick["std_slope"] = [df_candleStick["std"][i]-df_candleStick["std"][i-1] for i in range(len(df_candleStick.index))]
                isRange = [i > 0 for i in df_candleStick["std_slope"]]
            else:
                isRange = [False for i in df_candleStick.index]# その他のケース（thもtermも指定されていない場合）は、Falseが詰められます。
            return isRange