import datetime
import pandas as pd
import csv

class csv_to_df:
    
    def __init__(self):
        pass

    def fromListToDF(self, candleStick):
        """
        Listのローソク足をpandasデータフレームへ.
        """
        date = [price[0] for price in candleStick]# 少し複雑ですが、candleStick配列をfor文で回して取得した要素の0番目をdate配列に入れていきます。
        priceOpen = [int(price[1]) for price in candleStick]
        priceHigh = [int(price[2]) for price in candleStick]
        priceLow = [int(price[3]) for price in candleStick]
        priceClose = [int(price[4]) for price in candleStick]
        date_datetime = map(datetime.datetime.fromtimestamp, date)# mapは高階関数.`map` でdate配列の値に順次 `datetime.datetime.fromtimestamp` メソッドを適用.`datetime.datetime.fromtimestamp` メソッドは、unixtimestampをdatetime型に変換します。例えば `1534466705` をfromtimestampすると `datetime.datetime(2018, 8, 17, 9, 45, 5)` になります。括弧内は前から順番に、年・月・日・時間・分・秒です。
        dti = pd.DatetimeIndex(date_datetime)# date_datetime配列を、pandasで利用しやすいDatetimeIndexに変換します。
        df_candleStick = pd.DataFrame({"open" : priceOpen, "high" : priceHigh, "low": priceLow, "close" : priceClose}, index=dti)# 価格データと日時データを、日時データをindexとしてpandas dataframeに変換します。参考: https://deepage.net/features/pandas-dataframe.html
        return df_candleStick
 
    #csvファイル（ヘッダなし）からohlcデータを作成．
    def readDataFromFile(self,filename):
        print("読み込み開始")
        with open(filename, 'r', encoding="utf-8") as f:
            reader = csv.reader(f)
            for row in reader:
                candleStick = [row for row in reader if row[4] != "0"]  # row[4]が0でない場合に、csvの各行をrowに格納し、そのrowをcandleStickとする。

        dtDate = [datetime.datetime.strptime(data[0], '%Y/%m/%d %H:%M') for data in candleStick]  # strptime関数で文字列を'%Y-%m-%d %H:%M:%S'形式の時刻に変換
        dtTimeStamp = [dt.timestamp() for dt in dtDate]  # timestamp関数で変換

        for i in range(len(candleStick)):
            candleStick[i][0] = dtTimeStamp[i]

        print("読み込み完了")
        candleStick = [[float(i) for i in data] for data in candleStick]
        return candleStick