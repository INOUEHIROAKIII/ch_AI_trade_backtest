# _*_ coding: utf-8 _*_

import configparser
from dataclasses import dataclass
import numpy as numpy

class setting:
    CANDLE_INTARVAL = {
        "1440" : "days",
        "240" : "four_hour",
        "60" : "one_hour",
        "15" : "fifteen_minutes",
        "1" : "one_minutes"
    } 
    INITIAL_DF_SIZE = 200

    # [raise_fall_detection]
    # 急落の基準値を現在価格から算出する為の係数
    raise_rate = {
        0: {
            "days":         0.00000000000000000001538461539,
            "four_hour":    0.10,
            "one_hour":     0.10,
            "fifteen_minutes": 0.10,
            "one_minutes":  0.10
            },
        1: {
            "days":         -0.00000000000000475524475572719,
            "four_hour":    0.10,
            "one_hour":     0.10,
            "fifteen_minutes": 0.10,
            "one_minutes":  0.10
            },
        2: {
            "days":         0.000000000557342657391638,
            "four_hour":    0.10,
            "one_hour":     0.10,
            "fifteen_minutes": 0.10,
            "one_minutes":  0.10
            },
        3: {
            "days":         -0.0000306293706316018,
            "four_hour":    0.10,
            "one_hour":     0.10,
            "fifteen_minutes": 0.10,
            "one_minutes":  0.10
            },
        4: {
            "days":         0.878517482563806,
            "four_hour":    0.10,
            "one_hour":     0.10,
            "fifteen_minutes": 0.10,
            "one_minutes":  0.10
            }
    }

    # 10000台で2000、20000台で5000、30000台で6000、40000台で7000目指す
    raise_value = {
        "days":         -4200,
        "four_hour":    3000,
        "one_hour":     3000,
        "fifteen_minutes": 3000,
        "one_minutes":  3000
    }

    # ; 急騰落の判断するローソク足の数
    candle_num = {
        "days":         7,
        "four_hour":    7,
        "one_hour":     7,
        "fifteen_minutes": 7,
        "one_minutes":  30
    }

    # ; 変動終了判断の足数
    fluc_term = {
        "days":         1,
        "four_hour":    1,
        "one_hour":     1,
        "fifteen_minutes": 1,
        "one_minutes":  1
    }

    # [channel_describe]
    # ; ローカル極値日にち計算。大きすぎるとエラーとなる。
    local_term = {
        "after": {
            "days":         2,
            "four_hour":    2,
            "one_hour":     2,
            "fifteen_minutes": 2,
            "one_minutes":  2
            },
        "before": {
            "days":         2,
            "four_hour":    2,
            "one_hour":     2,
            "fifteen_minutes": 2,
            "one_minutes":  2
            }
    }

    # ; 第二max,minチャネルの検索窓の幅
    second_channel_search_rate = 0.6

    # ; チャネルを引き始めるローカル極値の数閾値★★デフォルトは4
    ch_start_point = 1


@dataclass
class trend_channel:
    y0:         float
    x0:         float
    slope:      float
    intercept:  float


@dataclass
class local_value:
    side:           list
    y_value:        list
    index:          list
    length:         float
    first_index:    int


class channel_info_set:
    rf_start_date = None
    rf_last_date = None
    ch_big_break_date = None
    ch_small_break_date = None
    tmp_ch_break_date = []
    previous_start_num = len(rf_start_date)
    local_value , temp_ch = local_value(
        side = [],
        y_value = [],
        index = [],
        length = 0,
        first_index = 0
        )
    max_channel = min_channel = max_channel2 = min_channel2 = line_regression = trend_channel(
        y0 = 0,
        x0 = 0,
        slope = 0,
        intercept = 0
        )
    distance_high = distance_low = {
        "index": numpy.empty(0),
        "value": numpy.empty(0)
        }
    renge = {
        "just_max": 0.0,
        "just_min": 0.0,
        "renge_width": 0.0,
        "rf_value": 0.0 # ★★急落時にデータを格納し、"renge_wedth"と比較する
        }
    f_4_comp = False
    f_channel_out = False
    f_re_ch = True

class channel_ctrl:
    # df_start_dateは、キャンドルデータの最初
    save_df_start_date = None
    save_df_start_point = 0
    loop_count = 0
    # process_dateは、処理の終了した最新日付
    save_process_date = None
    save_process_point = 0
    

class inifile:

    def __init__(self):
        self.set = configparser.ConfigParser()
        self.set.read('set.ini',encoding="utf-8")