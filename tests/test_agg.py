import unittest
import logging
import math
from datetime import datetime

import pandas as pd

import context
from runninglog.run import aggregator, all_runs, types

logger = logging.getLogger()
logger.setLevel(logging.CRITICAL)


def get_activity_trail_agg_data():
        return pd.DataFrame({
            'trail': [0,0,0,0,1],
            'date': [
            pd.to_datetime(datetime.strptime("16/08/2020", "%d/%m/%Y").date()),
            pd.to_datetime(datetime.strptime("16/08/2020", "%d/%m/%Y").date()),
            pd.to_datetime(datetime.strptime("16/08/2020", "%d/%m/%Y").date()),
            pd.to_datetime(datetime.strptime("23/08/2020", "%d/%m/%Y").date()),
            pd.to_datetime(datetime.strptime("23/08/2020", "%d/%m/%Y").date())
            ],
            'activity': [
                types.ACTIVITIES.RUNNING,
                types.ACTIVITIES.BIKING,
                types.ACTIVITIES.MOUNTAINEERING,
                types.ACTIVITIES.RUNNING,
                types.ACTIVITIES.RUNNING,
            ],
            'distance': [10, 11, 12, 13, 29],
            'time': [38, 20, 120, 50, 125],
            'climb': [50, 100, 600, 50, 1200],
            'distE': [0, 0, 0, 0, 15],
            'distM': [0, 0, 0, 0, 0],
            'distT': [10, 0, 0, 13, 14],
            'distI': [0, 0, 0, 0, 0],
            'distR': [0, 0, 0, 0, 0],
            'distX': [0, 0, 12, 0, 0],
            'distXB': [0, 11, 0, 0, 0],
            'timeE': [0, 20, 120, 0, 65],
            'timeM': [0, 0, 0, 0, 0],
            'timeT': [38, 0, 0, 50, 60],
            'timeI': [0, 0, 0, 0, 0],
            'timeR': [0, 0, 0, 0, 0],
            'timeX': [0, 0, 120, 0, 0],
            'timeXB': [0, 20, 0, 0, 0],
            'feeling': [3, None, 5, 4, 5],
            'N': [1, 1, 1, 1, 2]
        })

class TestAgg(unittest.TestCase):
    def test_agg_df(self):
        # Test aggregation

        df = pd.DataFrame({
            'date': [
            pd.to_datetime(datetime.strptime("14/08/2020", "%d/%m/%Y").date()),
            pd.to_datetime(datetime.strptime("15/08/2020", "%d/%m/%Y").date()),
            pd.to_datetime(datetime.strptime("16/08/2020", "%d/%m/%Y").date()),
            pd.to_datetime(datetime.strptime("21/08/2020", "%d/%m/%Y").date()),
            pd.to_datetime(datetime.strptime("22/08/2020", "%d/%m/%Y").date()),
            pd.to_datetime(datetime.strptime("23/08/2020", "%d/%m/%Y").date())
            ],
            'activity': [
                types.ACTIVITIES.RUNNING,
                types.ACTIVITIES.BIKING,
                types.ACTIVITIES.MOUNTAINEERING,
                types.ACTIVITIES.RUNNING,
                types.ACTIVITIES.RUNNING,
                types.ACTIVITIES.RUNNING,
            ],
            'trail': [0, 0, 0, 0, 1, 1],
            'distance': [10, 11, 12, 13, 14, 15],
            'time': [38, 20, 120, 50, 60, 65],
            'climb': [50, 100, 600, 50, 500, 700],
            'feeling': [3, None, 5, 4, None, 5],
            'distE': [0, 0, 0, 0, 0, 15],
            'distT': [10, 0, 0, 13, 14, 0],
            'timeE': [0, 20, 120, 0, 0, 65],
            'timeT': [38, 0, 0, 50, 60, 0],
            'distM': [0, 0, 0, 0, 0, 0],
            'distI': [0, 0, 0, 0, 0, 0],
            'distR': [0, 0, 0, 0, 0, 0],
            'distX': [0, 0, 12, 0, 0, 0],
            'distXB': [0, 11, 0, 0, 0, 0],
            'timeM': [0, 0, 0, 0, 0, 0],
            'timeI': [0, 0, 0, 0, 0, 0],
            'timeR': [0, 0, 0, 0, 0, 0],
            'timeX': [0, 0, 120, 0, 0, 0],
            'timeXB': [0, 20, 0, 0, 0, 0]
        })

        df_agg = aggregator.agg_df(df, 'week')
        df_agg.reset_index(inplace=True)

        df_agg_golden = get_activity_trail_agg_data()

        df_agg.sort_values(by=['date', 'activity', 'trail'], inplace=True)
        df_agg_golden.sort_values(by=['date', 'activity', 'trail'], inplace=True)

        df_agg_golden.reset_index(drop=True, inplace=True)
        df_agg.reset_index(drop=True, inplace=True)

        pd.testing.assert_frame_equal(df_agg, df_agg_golden)

    def test_agg_df_monthly(self):
        # Test aggregation; monthly

        df = pd.DataFrame({
            'date': [
            pd.to_datetime(datetime.strptime("14/08/2020", "%d/%m/%Y").date()),
            pd.to_datetime(datetime.strptime("15/08/2020", "%d/%m/%Y").date()),
            pd.to_datetime(datetime.strptime("16/08/2020", "%d/%m/%Y").date()),
            pd.to_datetime(datetime.strptime("21/08/2020", "%d/%m/%Y").date()),
            pd.to_datetime(datetime.strptime("22/08/2020", "%d/%m/%Y").date()),
            pd.to_datetime(datetime.strptime("23/08/2020", "%d/%m/%Y").date())
            ],
            'activity': [
                types.ACTIVITIES.RUNNING,
                types.ACTIVITIES.BIKING,
                types.ACTIVITIES.MOUNTAINEERING,
                types.ACTIVITIES.RUNNING,
                types.ACTIVITIES.RUNNING,
                types.ACTIVITIES.RUNNING,
            ],
            'trail': [0, 0, 0, 0, 1, 1],
            'distance': [10, 11, 12, 13, 14, 15],
            'time': [38, 20, 120, 50, 60, 65],
            'climb': [50, 100, 600, 50, 500, 700],
            'feeling': [3, None, 5, 4, None, 5],
            'distE': [0, 0, 0, 0, 0, 15],
            'distT': [10, 0, 0, 13, 14, 0],
            'timeE': [0, 20, 120, 0, 0, 65],
            'timeT': [38, 0, 0, 50, 60, 0],
            'distM': [0, 0, 0, 0, 0, 0],
            'distI': [0, 0, 0, 0, 0, 0],
            'distR': [0, 0, 0, 0, 0, 0],
            'distX': [0, 0, 12, 0, 0, 0],
            'distXB': [0, 11, 0, 0, 0, 0],
            'timeM': [0, 0, 0, 0, 0, 0],
            'timeI': [0, 0, 0, 0, 0, 0],
            'timeR': [0, 0, 0, 0, 0, 0],
            'timeX': [0, 0, 120, 0, 0, 0],
            'timeXB': [0, 20, 0, 0, 0, 0]
        })

        df_agg = aggregator.agg_df(df, 'month')
        df_agg.reset_index(inplace=True)

        df_agg_golden = pd.DataFrame({
            'trail': [0,0,0,1],
            'date': [
            pd.to_datetime(datetime.strptime("01/08/2020", "%d/%m/%Y").date()),
            pd.to_datetime(datetime.strptime("01/08/2020", "%d/%m/%Y").date()),
            pd.to_datetime(datetime.strptime("01/08/2020", "%d/%m/%Y").date()),
            pd.to_datetime(datetime.strptime("01/08/2020", "%d/%m/%Y").date())
            ],
            'activity': [
                types.ACTIVITIES.BIKING,
                types.ACTIVITIES.MOUNTAINEERING,
                types.ACTIVITIES.RUNNING,
                types.ACTIVITIES.RUNNING,
            ],
            'distance': [11, 12, 23, 29],
            'time': [20, 120, 88, 125],
            'climb': [100, 600, 100, 1200],
            'distE': [0, 0, 0, 15],
            'distM': [0, 0, 0, 0],
            'distT': [0, 0, 23, 14],
            'distI': [0, 0, 0, 0],
            'distR': [0, 0, 0, 0],
            'distX': [0, 12, 0, 0],
            'distXB': [11, 0, 0, 0],
            'timeE': [20, 120, 0, 65],
            'timeM': [0, 0, 0, 0],
            'timeT': [0, 0, 88, 60],
            'timeI': [0, 0, 0, 0],
            'timeR': [0, 0, 0, 0],
            'timeX': [0, 120, 0, 0],
            'timeXB': [20, 0, 0, 0],
            'feeling': [None, 5, 3.5, 5],
            'N': [1, 1, 2, 2]
        })

        df_agg.sort_values(by=['date', 'activity', 'trail'], inplace=True)
        df_agg_golden.sort_values(by=['date', 'activity', 'trail'], inplace=True)

        df_agg_golden.reset_index(drop=True, inplace=True)
        df_agg.reset_index(drop=True, inplace=True)

        pd.testing.assert_frame_equal(df_agg, df_agg_golden)

    def test_agg_by_date(self):
        # Test agg by date: running activities; both trail and road

        df = get_activity_trail_agg_data()

        df_agg = aggregator.agg_by_date(df,
                                        chosen_activities = ['running'],
                                        trail_road_selector = [0,1],
                                        time_option = 'week')

        df_agg_golden = pd.DataFrame({
            'date': ['2020-08-16', '2020-08-23'],
            'distance': [10, 42],
            'time': [38, 175],
            'climb': [50, 1250],
            'distE': [0, 15],
            'distM': [0, 0],
            'distT': [10, 27],
            'distI': [0, 0],
            'distR': [0, 0],
            'distX': [0, 0],
            'distXB': [0, 0],
            'timeE': [0, 65],
            'timeM': [0, 0],
            'timeT': [38, 110],
            'timeI': [0, 0],
            'timeR': [0, 0],
            'timeX': [0, 0],
            'timeXB': [0, 0],
            'feeling': [3, round((5*2+4)/3.,1)],
            'N': [1, 3],
            'n_trail': [0, 2],
            'n_road': [1, 1],
            'distance_trail': [0, 29],
            'distance_road': [10, 13],
            'Nall_Nroad_Ntrail': ['1/1/0', '3/1/2'],
            '%E': [0,35.7],
            '%M': [0.0,0],
            '%T': [100.0,64.3],
            '%I': [0.0,0],
            '%R': [0.0,0],
            '%X': [0,0],
            '%XB': [0,0],
            '%types': ['0(0)%/100%/0%/0%', '36(0)%/64%/0%/0%']
        })

        df_agg.sort_values(by=['date'], inplace=True)
        df_agg_golden.sort_values(by=['date'], inplace=True)

        df_agg_golden.reset_index(drop=True, inplace=True)
        df_agg.reset_index(drop=True, inplace=True)

        pd.testing.assert_frame_equal(df_agg, df_agg_golden, check_like=True)

    def test_agg_by_date_2(self):
        # Test agg by date: running activities; only trail

        df = get_activity_trail_agg_data()

        df_agg = aggregator.agg_by_date(df,
                                        chosen_activities = ['running'],
                                        trail_road_selector = [1],
                                        time_option = 'week')

        df_agg_golden = pd.DataFrame({
            'date': ['2020-08-23'],
            'distance': [29],
            'time': [125],
            'climb': [1200],
            'distE': [15],
            'distM': [0],
            'distT': [14],
            'distI': [0],
            'distR': [0],
            'distX': [0],
            'distXB': [0],
            'timeE': [65],
            'timeM': [0],
            'timeT': [60],
            'timeI': [0],
            'timeR': [0],
            'timeX': [0],
            'timeXB': [0],
            'feeling': [5.0],
            'N': [2],
            'n_trail': [2],
            'n_road': [0],
            'distance_trail': [ 29],
            'distance_road': [ 0],
            'Nall_Nroad_Ntrail': ['2/0/2'],
            '%E': [51.7],
            '%M': [0.0],
            '%T': [48.3],
            '%I': [0.0],
            '%R': [0.0],
            '%X': [0],
            '%XB': [0],
            '%types': ['52(0)%/48%/0%/0%']
        })

        df_agg.sort_values(by=['date'], inplace=True)
        df_agg_golden.sort_values(by=['date'], inplace=True)

        df_agg_golden.reset_index(drop=True, inplace=True)
        df_agg.reset_index(drop=True, inplace=True)

        pd.testing.assert_frame_equal(df_agg, df_agg_golden, check_like=True)

    def test_agg_by_date_3(self):
        # Test agg by date: no activities

        df = get_activity_trail_agg_data()

        df_agg = aggregator.agg_by_date(df,
                                        chosen_activities = [],
                                        trail_road_selector = [],
                                        time_option = 'week')

        cols = [
            'date',
            'distance',
            'time',
            'climb',
            'distE', 'distM', 'distT', 'distI', 'distR', 'distX', 'distXB',
            'timeE', 'timeM', 'timeT', 'timeI', 'timeR', 'timeX', 'timeXB',
            'feeling',
            'N', 'n_trail', 'n_road',
            'distance_trail', 'distance_road',
            'Nall_Nroad_Ntrail',
            '%E', '%M', '%T', '%I', '%R', '%X', '%XB',
            '%types'
        ]
        df_agg_golden = pd.DataFrame(columns = cols, data=[[0]*len(cols)])

        df_agg.sort_values(by=['date'], inplace=True)
        df_agg_golden.sort_values(by=['date'], inplace=True)

        df_agg_golden.reset_index(drop=True, inplace=True)
        df_agg.reset_index(drop=True, inplace=True)

        pd.testing.assert_frame_equal(df_agg, df_agg_golden, check_like=True, check_dtype = False)

    def test_agg_by_date_monthly(self):
        # Test agg by date: running activities; both trail and road. Group by
        # month

        df = pd.DataFrame({
            'trail': [0,0,0,1],
            'date': [
            pd.to_datetime(datetime.strptime("01/08/2020", "%d/%m/%Y").date()),
            pd.to_datetime(datetime.strptime("01/08/2020", "%d/%m/%Y").date()),
            pd.to_datetime(datetime.strptime("01/08/2020", "%d/%m/%Y").date()),
            pd.to_datetime(datetime.strptime("01/08/2020", "%d/%m/%Y").date())
            ],
            'activity': [
                types.ACTIVITIES.BIKING,
                types.ACTIVITIES.MOUNTAINEERING,
                types.ACTIVITIES.RUNNING,
                types.ACTIVITIES.RUNNING,
            ],
            'distance': [11, 12, 23, 29],
            'time': [20, 120, 88, 125],
            'climb': [100, 600, 100, 1200],
            'distE': [0, 0, 0, 15],
            'distM': [0, 0, 0, 0],
            'distT': [0, 0, 23, 14],
            'distI': [0, 0, 0, 0],
            'distR': [0, 0, 0, 0],
            'distX': [0, 12, 0, 0],
            'distXB': [11, 0, 0, 0],
            'timeE': [20, 120, 0, 65],
            'timeM': [0, 0, 0, 0],
            'timeT': [0, 0, 88, 60],
            'timeI': [0, 0, 0, 0],
            'timeR': [0, 0, 0, 0],
            'timeX': [0, 120, 0, 0],
            'timeXB': [20, 0, 0, 0],
            'feeling': [None, 5, 3.5, 5],
            'N': [1, 1, 2, 2]
        })

        df_agg = aggregator.agg_by_date(df,
                                        chosen_activities = [
                                                                'running',
                                                                'mountaineering'
                                                            ],
                                        trail_road_selector = [0,1],
                                        time_option = 'month')

        df_agg_golden = pd.DataFrame({
            'date': ['2020-08-01'],
            'distance': [64],
            'time': [333],
            'climb': [1900],
            'distE': [15],
            'distM': [0],
            'distT': [37],
            'distI': [0],
            'distR': [0],
            'distX': [12],
            'distXB': [0],
            'timeE': [185],
            'timeM': [0],
            'timeT': [148],
            'timeI': [0],
            'timeR': [0],
            'timeX': [120],
            'timeXB': [0],
            'feeling': [4.4],
            'N': [5],
            'n_trail': [2],
            'n_road': [3],
            'distance_trail': [29],
            'distance_road': [35],
            'Nall_Nroad_Ntrail': ['5/3/2'],
            '%E': [28.8],
            '%M': [0.0],
            '%T': [71.2],
            '%I': [0.0],
            '%R': [0.0],
            '%X': [0],
            '%XB': [0],
            '%types': ['29(0)%/71%/0%/0%']
        })

        df_agg.sort_values(by=['date'], inplace=True)
        df_agg_golden.sort_values(by=['date'], inplace=True)

        df_agg_golden.reset_index(drop=True, inplace=True)
        df_agg.reset_index(drop=True, inplace=True)

        pd.testing.assert_frame_equal(df_agg, df_agg_golden, check_like=True)

    def test_agg_by_date_feeling_avg(self):

        df = pd.DataFrame({
            'trail': [0,1],
            'date': [
            pd.to_datetime(datetime.strptime("01/08/2020", "%d/%m/%Y").date()),
            pd.to_datetime(datetime.strptime("01/08/2020", "%d/%m/%Y").date())
            ],
            'activity': [
                types.ACTIVITIES.RUNNING,
                types.ACTIVITIES.RUNNING,
            ],
            'distance': [23, 29],
            'time': [88, 125],
            'climb': [100, 1200],
            'distE': [0, 15],
            'distM': [0, 0],
            'distT': [23, 14],
            'distI': [0, 0],
            'distR': [0, 0],
            'distX': [0, 0],
            'distXB': [0, 0],
            'timeE': [0, 65],
            'timeM': [0, 0],
            'timeT': [88, 60],
            'timeI': [0, 0],
            'timeR': [0, 0],
            'timeX': [0, 0],
            'timeXB': [ 0, 0],
            'feeling': [None, 5],
            'N': [2,2]
        })

        df_agg = aggregator.agg_by_date(df, chosen_activities = ['running'],
                                        trail_road_selector = [0,1],
                                        time_option = 'month')

        self.assertEqual(df_agg.feeling[0], 5)

def main():
    return unittest.main(exit=False)

if __name__ == "__main__":
    main()
