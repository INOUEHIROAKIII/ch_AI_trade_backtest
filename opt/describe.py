import matplotlib.pyplot as plt
import pandas as pd
import backtest
import fromcsvtodf
import algrithm_to_back
import trade_algorithm
import sys

class describe:
    
    def __init__(self,limit_gap,market_trigger_gap,rate_of_failure_limit_order):
        self.csvread = fromcsvtodf.csv_to_df()
        self.algorithm = trade_algorithm.trade_algorithm()
        self.judge1 = algrithm_to_back.back_judge(limit_gap,market_trigger_gap,rate_of_failure_limit_order)
        self.backtest1 = backtest.backtest(market_trigger_gap)
    
    def describeResult(self, entryTerm, closeTerm, fileName=None, candleTerm=None, rangeTh=5000, rangeTerm=15, originalWaitTerm=10, waitTh=10000, showFigure=True, cost=0.0001):
        """
        signalsは買い，売り，中立が入った配列
        """

        if fileName == None:# 引数で渡されたfileNameがNoneの場合の処理。
           print("読み込む対象データのファイル名を指定して下さい")
           sys.exit()
            # s_hour = 0
            # s_min = 0
            # e_hour = 23
            # e_min = 59
            # number = int((e_hour - s_hour)*60 + e_min - s_min)# numberは一日の「分」の個数。1分ローソク足の個数計算。start_timestampは2018/3/24 00:00、end_timestampは2018/3/24 23:59のdatetimegが入る。ここの日付を変更することで任意の日のテストができる。
            # start_timestamp = datetime.datetime(2020, 8, 24, s_hour, s_min, 0, 0).timestamp()
            # end_timestamp = datetime.datetime(2020, 10, 24, e_hour, e_min, 0, 0).timestamp()
            # candleStick = self.getSpecifiedCandlestick(number, "60", start_timestamp, end_timestamp)# candleStickにnumberで指定した長さのローソク足が入る。
        else:
            # ファイル名が渡されている場合はそのファイルからローソク足を取得。
            candleStick = self.csvread.readDataFromFile(fileName)
 
        if candleTerm != None:
            print("無効なcandleTermが代入されています")
            sys.exit()
            # df_candleStick = self.processCandleStick(candleStick, candleTerm)
        else:
            # 取得したローソク足データをデータフレームへ変換
            print("DFに変換します")
            df_candleStick = self.csvread.fromListToDF(candleStick)
            print("DF変換完了しました")
 
        entryLowLine, entryHighLine = self.algorithm.calculateLines(df_candleStick, entryTerm)
        closeLowLine, closeHighLine = self.algorithm.calculateLines(df_candleStick, closeTerm)
        print("calculateLinesが完了しました")
        judgement,apo_market_order,exe_market_order = self.judge1.judge(df_candleStick, entryHighLine, entryLowLine, closeHighLine, closeLowLine, entryTerm)
        print("ジャッジが完了しました")
        pl, buyEntrySignals, sellEntrySignals, buyCloseSignals, sellCloseSignals, nOfTrade, plPerTrade, buy_entry,buy_close,sell_entry,sell_close = self.backtest1.backtest(judgement, df_candleStick, 0.1, rangeTh, rangeTerm, originalWaitTerm=originalWaitTerm, waitTh=waitTh, cost=cost,apo_market_order=apo_market_order,exe_market_order=exe_market_order)
        '''
        plはトレードの損益履歴、
        buyEntrySignalsはロングエントリー時のローソク足の時間情報、
        sellEntrySignalsはショートエントリー時のローソク足の時間情報、
        buyCloseSignalsはロングクローズ時のローソク足の時間情報、
        sellCloseSignalsはショートクローズ時のローソク足の時間情報、
        nOfTradeは取引回数、
        plPerTradeは取引ごとの損益、
        '''
        #1か月所要時間3秒
        # https://bicycle1885.hatenablog.com/entry/2014/02/14/023734 matplotlib入門
        plt.figure(figsize=(20,18))
        plt.subplot(311)
        plt.plot(df_candleStick.index, df_candleStick["high"])# x軸をローソク足の番号、y軸を高値もしくは安値としたグラフを描画します。
        plt.plot(df_candleStick.index, df_candleStick["low"])
        plt.ylabel("Price(USD)")# y軸の名前を設定します。
        ymin = min(df_candleStick["low"]) - 20
        ymax = max(df_candleStick["high"]) + 20#グラフの分かりやすさのために、minを20減算し、maxを20加算します。
        plt.plot(buyEntrySignals, buy_entry, "ro")
        plt.plot(buyCloseSignals, buy_close, "mo")
        #plt.vlines(buyEntrySignals, ymin , ymax, "blue", linestyles='dashed', linewidth=1)# エントリークローズした時間に縦線を引きます。先ほどのグラフと合わせるとどういう価格でエントリーしてどういう価格でクローズしたかがわかりやすくなります。
        #plt.vlines(sellEntrySignals, ymin , ymax, "red", linestyles='dashed', linewidth=1)
        #plt.vlines(buyCloseSignals, ymin , ymax, "black", linestyles='dashed', linewidth=1)
        #plt.vlines(sellCloseSignals, ymin , ymax, "green", linestyles='dashed', linewidth=1)

        plt.figure(figsize=(20,18))
        plt.subplot(312)
        plt.plot(df_candleStick.index, df_candleStick["high"])# x軸をローソク足の番号、y軸を高値もしくは安値としたグラフを描画します。
        plt.plot(df_candleStick.index, df_candleStick["low"])
        plt.ylabel("Price(USD)")# y軸の名前を設定します。
        ymin = min(df_candleStick["low"]) - 20
        ymax = max(df_candleStick["high"]) + 20#グラフの分かりやすさのために、minを200減算し、maxを200加算します。
        plt.plot(sellEntrySignals, sell_entry, "yo")
        plt.plot(sellCloseSignals, sell_close, "co") 

        plt.figure(figsize=(20,18))
        plt.subplot(313)
        plt.plot(df_candleStick.index, pl)
        plt.hlines(y=0, xmin=df_candleStick.index[0], xmax=df_candleStick.index[-1], colors='k', linestyles='dashed')
        plt.ylabel("PL(USD)")# 二つ目のグラフとして、損益履歴をプロットします。
 
        #各統計量の計算および表示．
        winTrade = sum([1 for i in plPerTrade if i > 0])
        loseTrade = sum([1 for i in plPerTrade if i < 0])
        winPer = round(winTrade/(winTrade+loseTrade) * 100,2)# 勝ちトレードの利益と負けトレードの損失を計算し、プロフィットファクターを算出します。
 
        winTotal = sum([i for i in plPerTrade if i > 0])
        loseTotal = sum([i for i in plPerTrade if i < 0])
        profitFactor = round(winTotal/-loseTotal, 3)
 
        maxProfit = max(plPerTrade)
        maxLoss = min(plPerTrade)
 
        print("Total pl: {}USD".format(int(pl[-1])))
        print("The number of Trades: {}".format(nOfTrade))
        print("The Winning percentage: {}%".format(winPer))
        print("The profitFactor: {}".format(profitFactor))
        print("The maximum Profit and Loss: {}JPY, {}JPY".format(maxProfit, maxLoss))
        if showFigure:# showFigureが指定されている場合はグラフを描画します。
            plt.show()
        else:
            plt.clf()
        return pl[-1], profitFactor# 最終損益とプロフィットファクターを返します。