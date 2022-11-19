import trade_algorithm
import random
import pandas as pd
import math
import datetime
import matplotlib.dates as dates

class back_judge:
    
    def __init__(self,limit_gap,market_trigger_gap,rate_of_failure_limit_order):
        self.algrithm = trade_algorithm.trade_algorithm()
        self.limit_gap = limit_gap
        self.market_trigger_gap = market_trigger_gap
        self.rate_of_failure_limit_order = rate_of_failure_limit_order
    
    def judge(self, df_candleStick, entryHighLine, entryLowLine, closeHighLine, closeLowLine, entryTerm):
        """
        売り買い判断．ローソク足の高値が期間高値を上抜けたら買いエントリー．（2）ローソク足の安値が期間安値を下抜けたら売りエントリー．judgementリストは[買いエントリー，売りエントリー，買いクローズ（売り），売りクローズ（買い）]のリストになっている．（二次元リスト）リスト内リストはの要素は，0（シグナルなし）,価格（シグナル点灯）を取る．
        """
        judgement = [[0,0,0,0] for i in range(len(df_candleStick.index))]

        apo_market_order = [[0,0,0,0] for i in range(len(df_candleStick.index))]
        exe_market_order = [[0,0,0,0] for i in range(len(df_candleStick.index))]

        for i in range(len(df_candleStick.index)):
            
            if (i >= entryTerm):
                # 実働アルゴリズムをバックテストに使用
                judgement[i] = self.algrithm.judgeForLoop(df_candleStick["high"][i], df_candleStick["low"][i], entryHighLine[i-5:i], entryLowLine[i-5:i], closeHighLine[i-5:i], closeLowLine[i-5:i])
                # バックテスト用にjudgementを加工
                judgement[i],apo_market_order[i],exe_market_order[i] = self.convert_judge_for_backtest(judgement[i],entryHighLine[i],entryLowLine[i],closeLowLine[i],closeHighLine[i],apo_market_order[i-2:i],exe_market_order[i-2:i],df_candleStick["high"][i], df_candleStick["low"][i])

            else:
                pass

        return (judgement,apo_market_order,exe_market_order)

    def convert_judge_for_backtest(self,judgement,entryHighLine,entryLowLine,closeLowLine,closeHighLine,apo_market_order,exe_market_order,high,low):
        
        # 実際のorderでの様々なパターンを想定し、かかるコストをよりリアルに算出する
        # 1. limit 0.0001、market 0.0006
        # 2. limit発注が約定するまでの最大ずれ gap_limit(USDT) ← 実際には、乱数でいつ約定するかはランダムと仮定する
        # 3. 引っかからなかった場合は諦める ← 諦める確率はどれくらいだか難しいが、例えば3割とする
        # 4. 価格がmarket_trigger_gap(USDT)となった場合はmarketで約定させに行く
        
        # 仮(30%)の確率でlimitが約定しないと仮定する
        catch = self.return_probability(self.rate_of_failure_limit_order)


        # 上抜けでエントリー
        if judgement[0] == 1:
                judgement[0] = entryHighLine + self.limit_gap*random.randint(1,10)/10 

        # 下抜けでエントリー
        if judgement[1] == 1:
                judgement[1] = entryLowLine - self.limit_gap*random.randint(1,10)/10

        # 下抜けでクローズ
        if judgement[2] == 1:
                judgement[2] = closeLowLine - self.limit_gap*random.randint(1,10)/10

        # 上抜けでクローズ
        if judgement[3] == 1:
                judgement[3] = closeHighLine + self.limit_gap*random.randint(1,10)/10

        # # 上抜けでエントリー
        # if judgement[0] == 1:
        #     if catch:
        #         judgement[0] = entryHighLine + self.limit_gap*random.randint(1,10)/10 
        #     else:
        #         judgement[0] = 0
        # # 下抜けでエントリー
        # if judgement[1] == 1:
        #     if catch:
        #         judgement[1] = entryLowLine - self.limit_gap*random.randint(1,10)/10
        #     else:
        #         judgement[1] = 0
        # # 下抜けでクローズ
        # if judgement[2] == 1:
        #     if catch:
        #         judgement[2] = closeLowLine - self.limit_gap*random.randint(1,10)/10
        #     else:
        #         judgement[2] = 0
        # # 上抜けでクローズ
        # if judgement[3] == 1:
        #     if catch:
        #         judgement[3] = closeHighLine + self.limit_gap*random.randint(1,10)/10
        #     else:
        #         judgement[3] = 0
        
        # limitが約定しなかった場合に、marketでの注文を行うべきか判断する
        apo_market_order_ret,exe_market_order_ret = self.miss_limit_deal(catch,apo_market_order,exe_market_order,judgement,entryHighLine,entryLowLine,closeLowLine,closeHighLine,high,low)
        
        return (judgement,apo_market_order_ret,exe_market_order_ret)


    def return_probability(self,rate):
        # target(%)でFalseを返す
        prob = True if rate/10 <= random.randint(1,10) else False
        return prob

    def miss_limit_deal(self,catch,apo_market_order,exe_market_order,judgement,entryHighLine,entryLowLine,closeLowLine,closeHighLine,high,low):
        
        # apo_market_orderが点灯するタイミング
        #     Limitの約定に失敗した(catch == False)となったタイミング
        # apo_market_orderを消灯するタイミング
        #     反対決済に1が点灯した場合
        #     価格(high or low)がapo_market_orderよりも低くなったタイミング
        #     exe_market_orderが1になった次の足のタイミング
        # exe_market_orderが、1になる条件：
        #     highもしくはlowが目標値(= apo_market_order)±market_gapより大きくなった場合。Judgementのiで±を判
        # Judgementに1が点灯していても、apo_market_orderに値が入っている場合は、entryはしない。
        # 一番下が1となった場合のみマーケットでエントリー or close

        
        # 前回の情報の引継ぎ確認
        if (apo_market_order[0][0] != 0 and apo_market_order[0][0] < low and exe_market_order[0][0] != 1):
            apo_market_order[1][0] = apo_market_order[0][0]
        if (apo_market_order[0][1] != 0 and apo_market_order[0][1] > high and exe_market_order[0][1] != 1):
            apo_market_order[1][1] = apo_market_order[0][1]
        if (apo_market_order[0][2] != 0 and apo_market_order[0][2] > high and exe_market_order[0][2] != 1):
            apo_market_order[1][2] = apo_market_order[0][2]
        if (apo_market_order[0][3] != 0 and apo_market_order[0][3] < low and exe_market_order[0][3] != 1):
            apo_market_order[1][3] = apo_market_order[0][3]
        
        
        # 新規登録と初期化
        # 上抜けでエントリー
        if catch == False and judgement[0] != 0 and apo_market_order[0][0] == 0:
            # 代入
            apo_market_order[1][0] = entryHighLine
        if judgement[0] != 0:
            # 初期化(1.反対決済に1が点灯した場合)
            apo_market_order[1][1] = 0
            apo_market_order[1][2] = 0

        # 下抜けでエントリー
        if  catch == False and judgement[1] != 0 and apo_market_order[0][1] == 0:
            # 代入
            apo_market_order[1][1] = entryLowLine
        if judgement[1] != 0:
            # 初期化(1.反対決済に1が点灯した場合)
            apo_market_order[1][0] = 0
            apo_market_order[1][3] = 0

        # 下抜けでクローズ
        if  catch == False and judgement[2] != 0 and apo_market_order[0][2] == 0:
            # 代入
            apo_market_order[1][2] = closeLowLine
        if judgement[2] != 0:
            # 初期化(1.反対決済に1が点灯した場合)
            apo_market_order[1][0] = 0
            apo_market_order[1][3] = 0

        # 上抜けでクローズ
        if  catch == False and judgement[3] != 0 and apo_market_order[0][3] == 0:
            # 代入
            apo_market_order[1][3] = closeHighLine
        if judgement[3] != 0:
            # 初期化(1.反対決済に1が点灯した場合)
            apo_market_order[1][1] = 0
            apo_market_order[1][2] = 0


        # market決済の決心
        if (apo_market_order[1][0] != 0 and apo_market_order[1][0] + self.market_trigger_gap <= high):
            exe_market_order[1][0] = 1
        if (apo_market_order[1][1] != 0 and apo_market_order[1][1] - self.market_trigger_gap >= low):
            exe_market_order[1][1] = 1
        if (apo_market_order[1][2] != 0 and apo_market_order[1][2] - self.market_trigger_gap >= low):
            exe_market_order[1][2] = 1
        if (apo_market_order[1][3] != 0 and apo_market_order[1][3] + self.market_trigger_gap <= high):
            exe_market_order[1][3] = 1
        
        return (apo_market_order[1],exe_market_order[1])


        # 実際のorderでの様々なパターンを想定し、かかるコストをよりリアルに算出する
        # 1. limit 0.0001、market 0.0006
        # 2. limit発注が約定するまでの最大ずれ gap_limit(USDT) ← 実際には、乱数でいつ約定するかはランダムと仮定する
        # 3. 引っかからなかった場合は諦める ← 諦める確率はどれくらいだか難しいが、例えば3割とする
        # 4. 価格がmarket_trigger_gap(USDT)となった場合はmarketとする

        # 2に関連してclose_priceとentry_priceを加工してreturnする


        # 4に関連して、limit諦めた場合に価格とjudgement及びjudgementのiを覚えておき、high及びlowが同じ方向にmarket_trigger_gap以上離れた場合にmarketで約定しに行く。marketが約定したことを示す配列が別途いる

    # def judge(self, df_candleStick, entryHighLine, entryLowLine, closeHighLine, closeLowLine, entryTerm):
    #         """
    #         売り買い判断．ローソク足の高値が期間高値を上抜けたら買いエントリー．（2）ローソク足の安値が期間安値を下抜けたら売りエントリー．judgementリストは[買いエントリー，売りエントリー，買いクローズ（売り），売りクローズ（買い）]のリストになっている．（二次元リスト）リスト内リストはの要素は，0（シグナルなし）,価格（シグナル点灯）を取る．
    #         """
    #         judgement = [[0,0,0,0] for i in range(len(df_candleStick.index))]
    #         for i in range(len(df_candleStick.index)):
    #             #上抜けでエントリー
    #             if df_candleStick["high"][i] > entryHighLine[i] and i >= entryTerm:
    #                 judgement[i][0] = entryHighLine[i]
    #             #下抜けでエントリー
    #             if df_candleStick["low"][i] < entryLowLine[i] and i >= entryTerm:
    #                 judgement[i][1] = entryLowLine[i]
    #             #下抜けでクローズ
    #             if df_candleStick["low"][i] < closeLowLine[i] and i >= entryTerm:
    #                 judgement[i][2] = closeLowLine[i]
    #             #上抜けでクローズ
    #             if df_candleStick["high"][i] > closeHighLine[i] and i >= entryTerm:
    #                 judgement[i][3] = closeHighLine[i]
                
    #             else:
    #                 pass
    #         return judgement

