import trade_algorithm

class backtest:    
    
    def __init__(self,market_trigger_gap):
        self.algorithm = trade_algorithm.trade_algorithm()
        self.market_trigger_gap = market_trigger_gap
    
    def backtest(self, judgement, df_candleStick, lot, rangeTh, rangeTerm, originalWaitTerm, waitTh, cost, apo_market_order, exe_market_order):
        #エントリーポイント，クローズポイントを入れるリスト
        buyEntrySignals = []
        sellEntrySignals = []
        buyCloseSignals = []
        sellCloseSignals = []
        nOfTrade = 0
        pos = 0
        pl = []
        pl.append(0)
        #トレードごとの損益
        plPerTrade = []
        #取引時の価格を入れる配列．この価格でバックテストのplを計算する．（ので，どの価格で約定するかはテストのパフォーマンスに大きく影響を与える．）
        buy_entry = []
        buy_close = []
        sell_entry = []
        sell_close = []
        #各ローソク足について，レンジ相場かどうかの判定が入っている配列
        isRange =  self.algorithm.isRange(df_candleStick, rangeTerm, rangeTh)
        #基本ロット．勝ちトレードの直後はロットを落とす．
        originalLot = lot
        #勝ちトレード後，何回のトレードでロットを落とすか．
        waitTerm = 0
        entry_cost = cost
        close_cost = cost


        for i in range(len(judgement)):
            if i > 0:
                lastPL = pl[-1]# lastPL=pl[-1], pl.append(lastPL)の処理はおそらくここの処理が行われなかった場合のデフォルト値を入れているのでしょう。エントリーした際はplの末尾要素は（値的には）変化せず、closeした場合に変化するということです。
                pl.append(lastPL)
            
            #エントリーロジック
            if pos == 0 and not isRange[i]:
                #ロングエントリー
                if judgement[i][0] != 0 and apo_market_order[i][0] == 0:
                    pos += 1
                    buy_entry.append(judgement[i][0])#約定価格が入る
                    buyEntrySignals.append(df_candleStick.index[i])
                    entry_cost = cost

                #ロングエントリー。マーケット
                elif apo_market_order[i][0] != 0 and exe_market_order[i][0] == 1:
                    pos += 1
                    buy_entry.append(apo_market_order[i][0] + self.market_trigger_gap)#約定価格が入る
                    buyEntrySignals.append(df_candleStick.index[i])
                    entry_cost = cost*6
                
                #ショートエントリー
                elif judgement[i][1] != 0 and apo_market_order[i][1] == 0:
                    pos -= 1
                    sell_entry.append(judgement[i][1])
                    sellEntrySignals.append(df_candleStick.index[i])
                    entry_cost = cost

                #ショートエントリー。マーケット
                elif apo_market_order[i][1] != 0 and exe_market_order[i][1] == 1:
                    pos -= 1
                    sell_entry.append(apo_market_order[i][1] - self.market_trigger_gap)
                    sellEntrySignals.append(df_candleStick.index[i])
                    entry_cost = cost*6

            #ロングクローズロジック
            elif pos == 1:
                #ロングクローズ
                if judgement[i][2] != 0 and apo_market_order[i][2] == 0:
                    nOfTrade += 1
                    pos -= 1
                    buy_close.append(judgement[i][2])
                    close_cost = cost
                    #値幅
                    plRange = buy_close[-1] - buy_entry[-1]
                    pl[-1] = pl[-2] + (plRange) * lot - (buy_close[-1]*close_cost + buy_entry[-1]*entry_cost) * lot# self._cost = 0.0001に変更
                    buyCloseSignals.append(df_candleStick.index[i])
                    plPerTrade.append((plRange) * lot - (buy_close[-1]*close_cost + buy_entry[-1]*entry_cost) * lot)

                    waitTerm,lot = self.calc_next_order_lot(plRange,waitTh,originalWaitTerm,originalLot,waitTerm)

                #ロングクローズ。マーケット
                elif apo_market_order[i][2] != 0 and exe_market_order[i][2] == 1:
                    nOfTrade += 1
                    pos -= 1
                    buy_close.append(apo_market_order[i][2] - self.market_trigger_gap)
                    close_cost = cost*6
                    #値幅
                    plRange = buy_close[-1] - buy_entry[-1]
                    pl[-1] = pl[-2] + (plRange) * lot - (buy_close[-1]*close_cost + buy_entry[-1]*entry_cost) * lot# self._cost = 0.0001に変更
                    buyCloseSignals.append(df_candleStick.index[i])
                    plPerTrade.append((plRange) * lot - (buy_close[-1]*close_cost + buy_entry[-1]*entry_cost) * lot)

                    waitTerm,lot = self.calc_next_order_lot(plRange,waitTh,originalWaitTerm,originalLot,waitTerm)

            #ショートクローズロジック
            elif pos == -1:
                #ショートクローズ
                if judgement[i][3] != 0 and apo_market_order[i][3] == 0:
                    nOfTrade += 1
                    pos += 1
                    sell_close.append(judgement[i][3])
                    close_cost = cost
                    plRange = sell_entry[-1] - sell_close[-1]
                    pl[-1] = pl[-2] + (plRange) * lot - (sell_close[-1]*close_cost + sell_entry[-1]*entry_cost) * lot
                    sellCloseSignals.append(df_candleStick.index[i])
                    plPerTrade.append((plRange) * lot - (sell_close[-1]*close_cost + sell_entry[-1]*entry_cost) * lot)

                    waitTerm,lot = self.calc_next_order_lot(plRange,waitTh,originalWaitTerm,originalLot,waitTerm)

                #ショートクローズ。マーケット
                elif apo_market_order[i][3] != 0 and exe_market_order[i][3] == 1:
                    nOfTrade += 1
                    pos += 1
                    sell_close.append(apo_market_order[i][3] + self.market_trigger_gap)
                    close_cost = cost*6
                    plRange = sell_entry[-1] - sell_close[-1]
                    pl[-1] = pl[-2] + (plRange) * lot - (sell_close[-1]*close_cost + sell_entry[-1]*entry_cost) * lot
                    sellCloseSignals.append(df_candleStick.index[i])
                    plPerTrade.append((plRange) * lot - (sell_close[-1]*close_cost + sell_entry[-1]*entry_cost) * lot)

                    waitTerm,lot = self.calc_next_order_lot(plRange,waitTh,originalWaitTerm,originalLot,waitTerm)
 
            #さらに，クローズしたと同時にエントリーシグナルが出ていた場合のロジック．
            if pos == 0 and not isRange[i]:
                #ロングエントリー
                if judgement[i][0] != 0 and apo_market_order[i][0] == 0:
                    pos += 1
                    buy_entry.append(judgement[i][0])
                    buyEntrySignals.append(df_candleStick.index[i])# Signals配列にローソク足の時間情報を入れます。
                    entry_cost = cost

                #ロングエントリー。マーケット
                elif apo_market_order[i][0] != 0 and exe_market_order[i][0] == 1:
                    pos += 1
                    buy_entry.append(apo_market_order[i][0] + self.market_trigger_gap)#約定価格が入る
                    buyEntrySignals.append(df_candleStick.index[i])
                    entry_cost = cost*6

                #ショートエントリー
                elif judgement[i][1] != 0 and apo_market_order[i][1] == 0:
                    pos -= 1
                    sell_entry.append(judgement[i][1])
                    sellEntrySignals.append(df_candleStick.index[i])
                    entry_cost = cost
                
                #ショートエントリー。マーケット
                elif apo_market_order[i][1] != 0 and exe_market_order[i][1] == 1:
                    pos -= 1
                    sell_entry.append(apo_market_order[i][1] - self.market_trigger_gap)
                    sellEntrySignals.append(df_candleStick.index[i])
                    entry_cost = cost*6

        #最後にポジションを持っていたら，期間最後のローソク足の終値で反対売買．
        if pos == 1:
            buy_close.append(df_candleStick["close"][-1])
            plRange = buy_close[-1] - buy_entry[-1]
            pl[-1] = pl[-2] + plRange * lot
            pos -= 1
            buyCloseSignals.append(df_candleStick.index[-1])
            nOfTrade += 1
            plPerTrade.append(plRange*lot)
        elif pos ==-1:
            sell_close.append(df_candleStick["close"][-1])
            plRange = sell_entry[-1] - sell_close[-1]
            pl[-1] = pl[-2] + plRange * lot
            pos +=1
            sellCloseSignals.append(df_candleStick.index[-1])
            nOfTrade += 1
            plPerTrade.append(plRange*lot)
        return (pl, buyEntrySignals, sellEntrySignals, buyCloseSignals, sellCloseSignals, nOfTrade, plPerTrade,buy_entry,buy_close,sell_entry,sell_close)

    def calc_next_order_lot(self,plRange,waitTh,originalWaitTerm,originalLot,waitTerm):
        #waitTh円以上の値幅を取った場合，次の10トレードはロットを1/10に落とす．
        if plRange > waitTh:
            waitTerm = originalWaitTerm
            lot = originalLot/10
        elif waitTerm > 0:
            waitTerm -= 1
            lot = originalLot/10
        if waitTerm == 0:
            lot = originalLot
        
        return (waitTerm,lot)