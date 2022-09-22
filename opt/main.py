import describe
import optimization
import signal

signal.signal(signal.SIGINT, signal.SIG_DFL)


if __name__ == '__main__':# if __name__=='__main__': はこのPythonファイルが「python ファイル名.py というふうに実行されているかどうか」を判定するif文
    # とりあえず5分足，5期間安値・高値でエントリー，クローズする設定
    limit_gap = 0
    market_trigger_gap = 60
    rate_of_failure_limit_order = 30
    backtest = describe.describe(limit_gap,market_trigger_gap,rate_of_failure_limit_order)
    backtest.entryTerm = 5
    backtest.closeTerm = 5
    backtest.rangeTh = 35
    backtest.rangeTerm = 15
    backtest.waitTerm = 10
    backtest.waitTh = 10000
    backtest.candleTerm = None#5分足にしたければ、"5T"
    backtest.cost = 0.0001
    API_KEY    ='uYvNx2Vr1QFmGXgSPE'
    API_SECRET ='Snla6UdZAJbAcwyE6XmdhASnKAswRvn6Vis1'
    symbol = "BTCUSDT"
    size = 0.001

    
    # バックテスト

    fileName = "BTCUSDT_1か月_2022_8_9_23.csv"
    # fileName = "to_csv_out.csv"
    backtest.describeResult(entryTerm=backtest.entryTerm, closeTerm=backtest.closeTerm, fileName=fileName , rangeTh=backtest.rangeTh, rangeTerm=backtest.rangeTerm,  originalWaitTerm=backtest.waitTerm, waitTh=backtest.waitTh, candleTerm=backtest.candleTerm,showFigure=True, cost=backtest.cost)



    # バックテスト＆最適化

    # fileName = "BTCUSDT_2年_2022_8_10_15.csv"
    # backtest = optimization.optimization(fileName)
    # backtest.optimization()