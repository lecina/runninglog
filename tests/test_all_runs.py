import unittest
import datetime
import os
import pandas as pd

import context
from runninglog.run import all_runs
from runninglog.run import single, types
from runninglog.reader import reader


class TestAllRuns(unittest.TestCase):
    def test_read_single_run1(self):
        allRuns = all_runs.AllRuns()
        datafile = os.path.join(os.path.split(__file__)[0], 'data', 'test_2.json')
        singleRun = allRuns.read_file(datafile, verbose=False)

        self.assertEqual(len(singleRun),1)
        singleRun = singleRun[0]

        goldenSingleRun = single.SingleRun()
        goldenSingleRun.type = types.RUN_TYPES_ENUM.T
        goldenSingleRun.time = 75
        goldenSingleRun.distance = 13.80
        goldenSingleRun.climb = 110
        goldenSingleRun.vspeed = 88
        goldenSingleRun.pace = 326.087
        goldenSingleRun.where = "Park"
        goldenSingleRun.route = "Lap 1"
        goldenSingleRun.is_trail_running = True
        goldenSingleRun.date = datetime.datetime.strptime("26/11/2018", "%d/%m/%Y").date()
        goldenSingleRun.basic_dist[types.BASIC_RUN_TYPES_ENUM.E] = 7.96
        goldenSingleRun.basic_dist[types.BASIC_RUN_TYPES_ENUM.M] = 0
        goldenSingleRun.basic_dist[types.BASIC_RUN_TYPES_ENUM.T] = 5.84
        goldenSingleRun.basic_dist[types.BASIC_RUN_TYPES_ENUM.I] = 0
        goldenSingleRun.basic_dist[types.BASIC_RUN_TYPES_ENUM.R] = 0
        goldenSingleRun.basic_time[types.BASIC_RUN_TYPES_ENUM.E] = 3121.76
        goldenSingleRun.basic_time[types.BASIC_RUN_TYPES_ENUM.M] = 0
        goldenSingleRun.basic_time[types.BASIC_RUN_TYPES_ENUM.T] = 1378.24
        goldenSingleRun.basic_time[types.BASIC_RUN_TYPES_ENUM.I] = 0
        goldenSingleRun.basic_time[types.BASIC_RUN_TYPES_ENUM.R] = 0
        goldenSingleRun.basic_pace[types.BASIC_RUN_TYPES_ENUM.E] = 392.1809
        goldenSingleRun.basic_pace[types.BASIC_RUN_TYPES_ENUM.M] = None
        goldenSingleRun.basic_pace[types.BASIC_RUN_TYPES_ENUM.T] = 236
        goldenSingleRun.basic_pace[types.BASIC_RUN_TYPES_ENUM.I] = None
        goldenSingleRun.basic_pace[types.BASIC_RUN_TYPES_ENUM.R] = None

        self.assertEqual(singleRun, goldenSingleRun)

    def test_read_single_run2(self):
        allRuns = all_runs.AllRuns()
        datafile = os.path.join(os.path.split(__file__)[0], 'data', 'test_3.json')
        singleRun = allRuns.read_file(datafile, verbose=False)

        self.assertEqual(len(singleRun),1)
        singleRun = singleRun[0]

        goldenSingleRun = single.SingleRun()
        goldenSingleRun.type = types.RUN_TYPES_ENUM.E
        goldenSingleRun.time = 60
        goldenSingleRun.distance = 12.2
        goldenSingleRun.climb = 100
        goldenSingleRun.vspeed = 100
        goldenSingleRun.pace = 295.081967213 
        goldenSingleRun.trail_running = False
        goldenSingleRun.where = "Park2"
        goldenSingleRun.route = ""
        goldenSingleRun.date = datetime.datetime.strptime("27/11/2018", "%d/%m/%Y").date()
        goldenSingleRun.basic_dist[types.BASIC_RUN_TYPES_ENUM.E] = 12.2
        goldenSingleRun.basic_dist[types.BASIC_RUN_TYPES_ENUM.M] = 0
        goldenSingleRun.basic_dist[types.BASIC_RUN_TYPES_ENUM.T] = 0
        goldenSingleRun.basic_dist[types.BASIC_RUN_TYPES_ENUM.I] = 0
        goldenSingleRun.basic_dist[types.BASIC_RUN_TYPES_ENUM.R] = 0
        goldenSingleRun.basic_time[types.BASIC_RUN_TYPES_ENUM.E] = 3600
        goldenSingleRun.basic_time[types.BASIC_RUN_TYPES_ENUM.M] = 0
        goldenSingleRun.basic_time[types.BASIC_RUN_TYPES_ENUM.T] = 0
        goldenSingleRun.basic_time[types.BASIC_RUN_TYPES_ENUM.I] = 0
        goldenSingleRun.basic_time[types.BASIC_RUN_TYPES_ENUM.R] = 0
        goldenSingleRun.basic_pace[types.BASIC_RUN_TYPES_ENUM.E] = 295.081967213
        goldenSingleRun.basic_pace[types.BASIC_RUN_TYPES_ENUM.M] = None
        goldenSingleRun.basic_pace[types.BASIC_RUN_TYPES_ENUM.T] = None
        goldenSingleRun.basic_pace[types.BASIC_RUN_TYPES_ENUM.I] = None
        goldenSingleRun.basic_pace[types.BASIC_RUN_TYPES_ENUM.R] = None

        self.assertEqual(singleRun, goldenSingleRun)

    def test_read_single_run3(self):
        allRuns = all_runs.AllRuns()
        datafile = os.path.join(os.path.split(__file__)[0], 'data', 'test_1.json')
        singleRuns = allRuns.read_file(datafile, verbose=False)

        goldenSingleRun = single.SingleRun()
        goldenSingleRun.type = types.RUN_TYPES_ENUM.T
        goldenSingleRun.time = 75
        goldenSingleRun.distance = 13.80
        goldenSingleRun.climb = 110
        goldenSingleRun.vspeed = 88
        goldenSingleRun.pace = 326.087
        goldenSingleRun.where = "Park"
        goldenSingleRun.route = ""
        goldenSingleRun.date = datetime.datetime.strptime("26/12/2018", "%d/%m/%Y").date()
        goldenSingleRun.basic_dist[types.BASIC_RUN_TYPES_ENUM.E] = 7.96
        goldenSingleRun.basic_dist[types.BASIC_RUN_TYPES_ENUM.M] = 0
        goldenSingleRun.basic_dist[types.BASIC_RUN_TYPES_ENUM.T] = 5.84
        goldenSingleRun.basic_dist[types.BASIC_RUN_TYPES_ENUM.I] = 0
        goldenSingleRun.basic_dist[types.BASIC_RUN_TYPES_ENUM.R] = 0
        goldenSingleRun.basic_time[types.BASIC_RUN_TYPES_ENUM.E] = 3121.76
        goldenSingleRun.basic_time[types.BASIC_RUN_TYPES_ENUM.M] = 0
        goldenSingleRun.basic_time[types.BASIC_RUN_TYPES_ENUM.T] = 1378.24
        goldenSingleRun.basic_time[types.BASIC_RUN_TYPES_ENUM.I] = 0
        goldenSingleRun.basic_time[types.BASIC_RUN_TYPES_ENUM.R] = 0
        goldenSingleRun.basic_pace[types.BASIC_RUN_TYPES_ENUM.E] = 392.1809
        goldenSingleRun.basic_pace[types.BASIC_RUN_TYPES_ENUM.M] = None
        goldenSingleRun.basic_pace[types.BASIC_RUN_TYPES_ENUM.T] = 236
        goldenSingleRun.basic_pace[types.BASIC_RUN_TYPES_ENUM.I] = None
        goldenSingleRun.basic_pace[types.BASIC_RUN_TYPES_ENUM.R] = None

        goldenSingleRun2 = single.SingleRun()
        goldenSingleRun2.type = types.RUN_TYPES_ENUM.E
        goldenSingleRun2.time = 60
        goldenSingleRun2.distance = 12.2
        goldenSingleRun2.climb = 100
        goldenSingleRun2.vspeed = 100
        goldenSingleRun2.pace = 295.082
        goldenSingleRun2.where = "Park2"
        goldenSingleRun2.route = ""
        goldenSingleRun2.date = datetime.datetime.strptime("27/12/2018", "%d/%m/%Y").date()
        goldenSingleRun2.basic_dist[types.BASIC_RUN_TYPES_ENUM.E] = 12.2
        goldenSingleRun2.basic_dist[types.BASIC_RUN_TYPES_ENUM.M] = 0
        goldenSingleRun2.basic_dist[types.BASIC_RUN_TYPES_ENUM.T] = 0
        goldenSingleRun2.basic_dist[types.BASIC_RUN_TYPES_ENUM.I] = 0
        goldenSingleRun2.basic_dist[types.BASIC_RUN_TYPES_ENUM.R] = 0
        goldenSingleRun2.basic_time[types.BASIC_RUN_TYPES_ENUM.E] = 3600
        goldenSingleRun2.basic_time[types.BASIC_RUN_TYPES_ENUM.M] = 0
        goldenSingleRun2.basic_time[types.BASIC_RUN_TYPES_ENUM.T] = 0
        goldenSingleRun2.basic_time[types.BASIC_RUN_TYPES_ENUM.I] = 0
        goldenSingleRun2.basic_time[types.BASIC_RUN_TYPES_ENUM.R] = 0
        goldenSingleRun2.basic_pace[types.BASIC_RUN_TYPES_ENUM.E] = 295.081967213
        goldenSingleRun2.basic_pace[types.BASIC_RUN_TYPES_ENUM.M] = None
        goldenSingleRun2.basic_pace[types.BASIC_RUN_TYPES_ENUM.T] = None
        goldenSingleRun2.basic_pace[types.BASIC_RUN_TYPES_ENUM.I] = None
        goldenSingleRun2.basic_pace[types.BASIC_RUN_TYPES_ENUM.R] = None

        self.assertEqual(singleRuns[0], goldenSingleRun)
        self.assertEqual(singleRuns[1], goldenSingleRun2)

    def test_get_json_files_in_subdirs(self):
        allRuns = all_runs.AllRuns()
        datafolder = os.path.join(os.path.split(__file__)[0], 'data', 'test_get_json_files')
        files = allRuns.get_json_files_in_subdirs(datafolder)
        files.sort()

        goldenData = [
                        os.path.join('1','2','a2.json'), 
                        os.path.join('1','2','b2.json'), 
                        os.path.join('1','a1.json'), 
                        'a.json', 
                        'b.json',
                    ]
        goldenData = [os.path.join(datafolder, f) for f in goldenData]

        self.assertEqual(files, goldenData)

    def test_not_adding_duplicated_single_run(self):
        allRuns = all_runs.AllRuns()

        singleRun = single.SingleRun()
        datafile = os.path.join(os.path.split(__file__)[0], 'data', 'test_2.json')
        parsed_json = reader.read_file(datafile)
        singleRun.load(parsed_json)

        added1 = allRuns.add_run(singleRun)
        df1 = allRuns.df.copy()
        added2 = allRuns.add_run(singleRun)
        df2 = allRuns.df.copy()

        goldenAdded1 = True
        goldenAdded2 = False

        self.assertEqual(added1, goldenAdded1)
        self.assertEqual(added2, goldenAdded2)
        pd.testing.assert_frame_equal(df1, df2, check_less_precise=True)

    def test_adding_two_different_single_runs(self):
        allRuns = all_runs.AllRuns()

        singleRun = single.SingleRun()
        datafile = os.path.join(os.path.split(__file__)[0], 'data', 'test_2.json')
        parsed_json = reader.read_file(datafile)
        singleRun.load(parsed_json)
        added1 = allRuns.add_run(singleRun)
        df1 = allRuns.df.copy()

        singleRun = single.SingleRun()
        datafile = os.path.join(os.path.split(__file__)[0], 'data', 'test_3.json')
        parsed_json = reader.read_file(datafile)
        singleRun.load(parsed_json)
        added2 = allRuns.add_run(singleRun)
        df2 = allRuns.df.copy()

        goldenAdded1 = True
        goldenAdded2 = True

        self.assertEqual(added1, goldenAdded1)
        self.assertEqual(added2, goldenAdded2)
        self.assertEqual(df1.equals(df2), False)
        self.assertEqual(df1.shape[0], 1)
        self.assertEqual(df2.shape[0], 2)

    def test_adding_two_different_single_runs_same_day(self):
        allRuns = all_runs.AllRuns()

        singleRun = single.SingleRun()
        datafile = os.path.join(os.path.split(__file__)[0], 'data', 'test_3.json')
        parsed_json = reader.read_file(datafile)
        singleRun.load(parsed_json)
        added1 = allRuns.add_run(singleRun)
        df1 = allRuns.df.copy()

        singleRun = single.SingleRun()
        datafile = os.path.join(os.path.split(__file__)[0], 'data', 'test_4.json')
        parsed_json = reader.read_file(datafile)
        singleRun.load(parsed_json)
        added2 = allRuns.add_run(singleRun)
        df2 = allRuns.df.copy()

        goldenAdded1 = True
        goldenAdded2 = True

        self.assertEqual(added1, goldenAdded1)
        self.assertEqual(added2, goldenAdded2)
        self.assertEqual(df1.equals(df2), False)
        self.assertEqual(df1.shape[0], 1)
        self.assertEqual(df2.shape[0], 2)

    def test_load_files_in_dir(self):
        allRuns = all_runs.AllRuns()
        datafolder = os.path.join(os.path.split(__file__)[0], 'data', 'test_load_files_in_dir')
        added_single_runs = allRuns.load_files_in_dir(datafolder, verbose=False)

        goldenSingleRun = single.SingleRun()
        goldenSingleRun.type = types.RUN_TYPES_ENUM.T
        goldenSingleRun.time = 75
        goldenSingleRun.distance = 13.80
        goldenSingleRun.climb = 110
        goldenSingleRun.vspeed = 88
        goldenSingleRun.pace = 326.09
        goldenSingleRun.where = "Park"
        goldenSingleRun.route = ""
        goldenSingleRun.date = datetime.datetime.strptime("26/11/2018", "%d/%m/%Y").date()
        goldenSingleRun.basic_dist[types.BASIC_RUN_TYPES_ENUM.E] = 7.96
        goldenSingleRun.basic_dist[types.BASIC_RUN_TYPES_ENUM.M] = 0
        goldenSingleRun.basic_dist[types.BASIC_RUN_TYPES_ENUM.T] = 5.84
        goldenSingleRun.basic_dist[types.BASIC_RUN_TYPES_ENUM.I] = 0
        goldenSingleRun.basic_dist[types.BASIC_RUN_TYPES_ENUM.R] = 0
        goldenSingleRun.basic_time[types.BASIC_RUN_TYPES_ENUM.E] = 3121.76
        goldenSingleRun.basic_time[types.BASIC_RUN_TYPES_ENUM.M] = 0
        goldenSingleRun.basic_time[types.BASIC_RUN_TYPES_ENUM.T] = 1378.24
        goldenSingleRun.basic_time[types.BASIC_RUN_TYPES_ENUM.I] = 0
        goldenSingleRun.basic_time[types.BASIC_RUN_TYPES_ENUM.R] = 0
        goldenSingleRun.basic_pace[types.BASIC_RUN_TYPES_ENUM.E] = 392.18
        goldenSingleRun.basic_pace[types.BASIC_RUN_TYPES_ENUM.M] = None
        goldenSingleRun.basic_pace[types.BASIC_RUN_TYPES_ENUM.T] = 236
        goldenSingleRun.basic_pace[types.BASIC_RUN_TYPES_ENUM.I] = None
        goldenSingleRun.basic_pace[types.BASIC_RUN_TYPES_ENUM.R] = None

        goldenSingleRun2 = single.SingleRun()
        goldenSingleRun2.type = types.RUN_TYPES_ENUM.E
        goldenSingleRun2.time = 60
        goldenSingleRun2.distance = 12.2
        goldenSingleRun2.climb = 100
        goldenSingleRun2.vspeed = 100
        goldenSingleRun2.pace = 295.08
        goldenSingleRun2.where = "Park2"
        goldenSingleRun2.route = ""
        goldenSingleRun2.date = datetime.datetime.strptime("27/11/2018", "%d/%m/%Y").date()
        goldenSingleRun2.basic_dist[types.BASIC_RUN_TYPES_ENUM.E] = 12.2
        goldenSingleRun2.basic_dist[types.BASIC_RUN_TYPES_ENUM.M] = 0
        goldenSingleRun2.basic_dist[types.BASIC_RUN_TYPES_ENUM.T] = 0
        goldenSingleRun2.basic_dist[types.BASIC_RUN_TYPES_ENUM.I] = 0
        goldenSingleRun2.basic_dist[types.BASIC_RUN_TYPES_ENUM.R] = 0
        goldenSingleRun2.basic_time[types.BASIC_RUN_TYPES_ENUM.E] = 3600
        goldenSingleRun2.basic_time[types.BASIC_RUN_TYPES_ENUM.M] = 0
        goldenSingleRun2.basic_time[types.BASIC_RUN_TYPES_ENUM.T] = 0
        goldenSingleRun2.basic_time[types.BASIC_RUN_TYPES_ENUM.I] = 0
        goldenSingleRun2.basic_time[types.BASIC_RUN_TYPES_ENUM.R] = 0
        goldenSingleRun2.basic_pace[types.BASIC_RUN_TYPES_ENUM.E] = 295.08
        goldenSingleRun2.basic_pace[types.BASIC_RUN_TYPES_ENUM.M] = None
        goldenSingleRun2.basic_pace[types.BASIC_RUN_TYPES_ENUM.T] = None
        goldenSingleRun2.basic_pace[types.BASIC_RUN_TYPES_ENUM.I] = None
        goldenSingleRun2.basic_pace[types.BASIC_RUN_TYPES_ENUM.R] = None

        golden_df = pd.DataFrame()
        sr_ds = pd.Series(goldenSingleRun.as_dict())
        sr_ds2 = pd.Series(goldenSingleRun2.as_dict())
        golden_df = golden_df.append(sr_ds, ignore_index=True)
        golden_df = golden_df.append(sr_ds2, ignore_index=True)

        pd.testing.assert_frame_equal(allRuns.df, golden_df, check_less_precise=True)

def main():
    return unittest.main(exit=False)

if __name__ == "__main__":
    main()
