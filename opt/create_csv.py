import csv

class csv:
    def get_candlestick_and_create_csv(self,df_candleStick,filename):
                df_candleStick.to_csv(str(filename)+'.csv')