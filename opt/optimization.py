import describe

class optimization:
    
    def __init__(self,filename):
        self.backtest = describe.describe()
        self.filename = filename

    def optimization(self):
        entryAndCloseTerm = [(5,3),(5,5),(10,10),(20,10)]
        rangeThAndrangeTerm = [(5000,5),(5000,15),(10000,15),(None,15),(None,20),(None,15)]
        waitTermAndwaitTh = [(10,10000),(10,20000),(5,10000)]
    
        paramList = []
        for i in entryAndCloseTerm:
            for j in rangeThAndrangeTerm:
                for k in waitTermAndwaitTh:
                    self.backtest.entryTerm = i[0]
                    self.backtest.closeTerm = i[1]
                    self.backtest.rangeTh = j[0]
                    self.backtest.rangeTerm = j[1]
                    self.backtest.waitTerm = k[0]
                    self.backtest.waitTh = k[1]
                    self.backtest.candleTerm = "1T"
                    #テスト
                    pl, profitFactor =  self.backtest.describeResult(entryTerm=self.backtest.entryTerm, closeTerm=self.backtest.closeTerm, fileName=self.filename, rangeTh=self.backtest.rangeTh, rangeTerm=self.backtest.rangeTerm,  originalWaitTerm=self.backtest.waitTerm, waitTh=self.backtest.waitTh, candleTerm=self.backtest.candleTerm, showFigure=False)
                    paramList.append([pl,profitFactor, i,j,k])
        pF = [i[1] for i in paramList]
        pL = [i[0] for i in paramList]
        print("ProfitFactor max:")
        print(paramList[pF.index(max(pF))])
        print("PL max:")
        print(paramList[pL.index(max(pL))])