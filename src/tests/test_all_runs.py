from src.all_runs import all_runs
from src.single_run import single_run, runTypes
from src.reader import reader

import unittest
import datetime
import pandas as pd

class TestAllRuns(unittest.TestCase):
    def test_read_single_run1(self):
        allRuns = all_runs.AllRuns()
        singleRun = allRuns.read_single_run("src/tests/data/test_2.json", verbose=False)

        goldenSingleRun = single_run.SingleRun()
        goldenSingleRun.type = runTypes.RUN_TYPES_ENUM.T
        goldenSingleRun.total_time = 75
        goldenSingleRun.total_distance = 13.80
        goldenSingleRun.climb = 110
        goldenSingleRun.vspeed = 88
        goldenSingleRun.avg_pace = 326.087
        goldenSingleRun.where = "Park"
        goldenSingleRun.route = "Lap 1"
        goldenSingleRun.trail_running = True
        goldenSingleRun.date = datetime.datetime.strptime("26/11/2018", "%d/%m/%Y").date()
        goldenSingleRun.basic_dist[runTypes.BASIC_RUN_TYPES_ENUM.E] = 7.96
        goldenSingleRun.basic_dist[runTypes.BASIC_RUN_TYPES_ENUM.M] = 0
        goldenSingleRun.basic_dist[runTypes.BASIC_RUN_TYPES_ENUM.T] = 5.84
        goldenSingleRun.basic_dist[runTypes.BASIC_RUN_TYPES_ENUM.I] = 0
        goldenSingleRun.basic_dist[runTypes.BASIC_RUN_TYPES_ENUM.R] = 0
        goldenSingleRun.basic_time[runTypes.BASIC_RUN_TYPES_ENUM.E] = 3121.76
        goldenSingleRun.basic_time[runTypes.BASIC_RUN_TYPES_ENUM.M] = 0
        goldenSingleRun.basic_time[runTypes.BASIC_RUN_TYPES_ENUM.T] = 1378.24
        goldenSingleRun.basic_time[runTypes.BASIC_RUN_TYPES_ENUM.I] = 0
        goldenSingleRun.basic_time[runTypes.BASIC_RUN_TYPES_ENUM.R] = 0
        goldenSingleRun.basic_pace[runTypes.BASIC_RUN_TYPES_ENUM.E] = 392.1809
        goldenSingleRun.basic_pace[runTypes.BASIC_RUN_TYPES_ENUM.M] = None
        goldenSingleRun.basic_pace[runTypes.BASIC_RUN_TYPES_ENUM.T] = 236
        goldenSingleRun.basic_pace[runTypes.BASIC_RUN_TYPES_ENUM.I] = None
        goldenSingleRun.basic_pace[runTypes.BASIC_RUN_TYPES_ENUM.R] = None

        self.assertEqual(singleRun, goldenSingleRun)

    def test_read_single_run2(self):
        allRuns = all_runs.AllRuns()
        singleRun = allRuns.read_single_run("src/tests/data/test_3.json", verbose=False)

        goldenSingleRun = single_run.SingleRun()
        goldenSingleRun.type = runTypes.RUN_TYPES_ENUM.E
        goldenSingleRun.total_time = 60
        goldenSingleRun.total_distance = 12.2
        goldenSingleRun.climb = 100
        goldenSingleRun.vspeed = 100
        goldenSingleRun.avg_pace = 295.081967213 
        goldenSingleRun.trail_running = False
        goldenSingleRun.where = "Park2"
        goldenSingleRun.route = ""
        goldenSingleRun.date = datetime.datetime.strptime("27/11/2018", "%d/%m/%Y").date()
        goldenSingleRun.basic_dist[runTypes.BASIC_RUN_TYPES_ENUM.E] = 12.2
        goldenSingleRun.basic_dist[runTypes.BASIC_RUN_TYPES_ENUM.M] = 0
        goldenSingleRun.basic_dist[runTypes.BASIC_RUN_TYPES_ENUM.T] = 0
        goldenSingleRun.basic_dist[runTypes.BASIC_RUN_TYPES_ENUM.I] = 0
        goldenSingleRun.basic_dist[runTypes.BASIC_RUN_TYPES_ENUM.R] = 0
        goldenSingleRun.basic_time[runTypes.BASIC_RUN_TYPES_ENUM.E] = 3600
        goldenSingleRun.basic_time[runTypes.BASIC_RUN_TYPES_ENUM.M] = 0
        goldenSingleRun.basic_time[runTypes.BASIC_RUN_TYPES_ENUM.T] = 0
        goldenSingleRun.basic_time[runTypes.BASIC_RUN_TYPES_ENUM.I] = 0
        goldenSingleRun.basic_time[runTypes.BASIC_RUN_TYPES_ENUM.R] = 0
        goldenSingleRun.basic_pace[runTypes.BASIC_RUN_TYPES_ENUM.E] = 295.081967213
        goldenSingleRun.basic_pace[runTypes.BASIC_RUN_TYPES_ENUM.M] = None
        goldenSingleRun.basic_pace[runTypes.BASIC_RUN_TYPES_ENUM.T] = None
        goldenSingleRun.basic_pace[runTypes.BASIC_RUN_TYPES_ENUM.I] = None
        goldenSingleRun.basic_pace[runTypes.BASIC_RUN_TYPES_ENUM.R] = None

        self.assertEqual(singleRun, goldenSingleRun)

    def test_read_single_run3(self):
        allRuns = all_runs.AllRuns()
        singleRuns = allRuns.read_single_run("src/tests/data/test_1.json", verbose=False)

        goldenSingleRun = single_run.SingleRun()
        goldenSingleRun.type = runTypes.RUN_TYPES_ENUM.T
        goldenSingleRun.total_time = 75
        goldenSingleRun.total_distance = 13.80
        goldenSingleRun.climb = 110
        goldenSingleRun.vspeed = 88
        goldenSingleRun.avg_pace = 326.087
        goldenSingleRun.where = "Park"
        goldenSingleRun.route = ""
        goldenSingleRun.date = datetime.datetime.strptime("26/12/2018", "%d/%m/%Y").date()
        goldenSingleRun.basic_dist[runTypes.BASIC_RUN_TYPES_ENUM.E] = 7.96
        goldenSingleRun.basic_dist[runTypes.BASIC_RUN_TYPES_ENUM.M] = 0
        goldenSingleRun.basic_dist[runTypes.BASIC_RUN_TYPES_ENUM.T] = 5.84
        goldenSingleRun.basic_dist[runTypes.BASIC_RUN_TYPES_ENUM.I] = 0
        goldenSingleRun.basic_dist[runTypes.BASIC_RUN_TYPES_ENUM.R] = 0
        goldenSingleRun.basic_time[runTypes.BASIC_RUN_TYPES_ENUM.E] = 3121.76
        goldenSingleRun.basic_time[runTypes.BASIC_RUN_TYPES_ENUM.M] = 0
        goldenSingleRun.basic_time[runTypes.BASIC_RUN_TYPES_ENUM.T] = 1378.24
        goldenSingleRun.basic_time[runTypes.BASIC_RUN_TYPES_ENUM.I] = 0
        goldenSingleRun.basic_time[runTypes.BASIC_RUN_TYPES_ENUM.R] = 0
        goldenSingleRun.basic_pace[runTypes.BASIC_RUN_TYPES_ENUM.E] = 392.1809
        goldenSingleRun.basic_pace[runTypes.BASIC_RUN_TYPES_ENUM.M] = None
        goldenSingleRun.basic_pace[runTypes.BASIC_RUN_TYPES_ENUM.T] = 236
        goldenSingleRun.basic_pace[runTypes.BASIC_RUN_TYPES_ENUM.I] = None
        goldenSingleRun.basic_pace[runTypes.BASIC_RUN_TYPES_ENUM.R] = None

        goldenSingleRun2 = single_run.SingleRun()
        goldenSingleRun2.type = runTypes.RUN_TYPES_ENUM.E
        goldenSingleRun2.total_time = 60
        goldenSingleRun2.total_distance = 12.2
        goldenSingleRun2.climb = 100
        goldenSingleRun2.vspeed = 100
        goldenSingleRun2.avg_pace = 295.082
        goldenSingleRun2.where = "Park2"
        goldenSingleRun2.route = ""
        goldenSingleRun2.date = datetime.datetime.strptime("27/12/2018", "%d/%m/%Y").date()
        goldenSingleRun2.basic_dist[runTypes.BASIC_RUN_TYPES_ENUM.E] = 12.2
        goldenSingleRun2.basic_dist[runTypes.BASIC_RUN_TYPES_ENUM.M] = 0
        goldenSingleRun2.basic_dist[runTypes.BASIC_RUN_TYPES_ENUM.T] = 0
        goldenSingleRun2.basic_dist[runTypes.BASIC_RUN_TYPES_ENUM.I] = 0
        goldenSingleRun2.basic_dist[runTypes.BASIC_RUN_TYPES_ENUM.R] = 0
        goldenSingleRun2.basic_time[runTypes.BASIC_RUN_TYPES_ENUM.E] = 3600
        goldenSingleRun2.basic_time[runTypes.BASIC_RUN_TYPES_ENUM.M] = 0
        goldenSingleRun2.basic_time[runTypes.BASIC_RUN_TYPES_ENUM.T] = 0
        goldenSingleRun2.basic_time[runTypes.BASIC_RUN_TYPES_ENUM.I] = 0
        goldenSingleRun2.basic_time[runTypes.BASIC_RUN_TYPES_ENUM.R] = 0
        goldenSingleRun2.basic_pace[runTypes.BASIC_RUN_TYPES_ENUM.E] = 295.081967213
        goldenSingleRun2.basic_pace[runTypes.BASIC_RUN_TYPES_ENUM.M] = None
        goldenSingleRun2.basic_pace[runTypes.BASIC_RUN_TYPES_ENUM.T] = None
        goldenSingleRun2.basic_pace[runTypes.BASIC_RUN_TYPES_ENUM.I] = None
        goldenSingleRun2.basic_pace[runTypes.BASIC_RUN_TYPES_ENUM.R] = None

        self.assertEqual(singleRuns[0], goldenSingleRun)
        self.assertEqual(singleRuns[1], goldenSingleRun2)

    def test_get_json_files_in_subdirs(self):
        allRuns = all_runs.AllRuns()
        files = allRuns.get_json_files_in_subdirs("src/tests/data/test_get_json_files")
        files.sort()

        goldenData = ['src/tests/data/test_get_json_files/1/2/a2.json', 'src/tests/data/test_get_json_files/1/2/b2.json', 'src/tests/data/test_get_json_files/1/a1.json', 'src/tests/data/test_get_json_files/a.json', 'src/tests/data/test_get_json_files/b.json']

        self.assertEqual(files, goldenData)

    def test_not_adding_duplicated_single_run(self):
        allRuns = all_runs.AllRuns()

        singleRun = single_run.SingleRun()
        parsed_json = reader.read_file('src/tests/data/test_2.json')
        singleRun.load_json(parsed_json)

        added1 = allRuns.append_single_run_if_not_present(singleRun)
        df1 = allRuns.df.copy()
        added2 = allRuns.append_single_run_if_not_present(singleRun)
        df2 = allRuns.df.copy()

        goldenAdded1 = True
        goldenAdded2 = False

        self.assertEqual(added1, goldenAdded1)
        self.assertEqual(added2, goldenAdded2)
        pd.testing.assert_frame_equal(df1, df2, check_less_precise=True)

    def test_adding_two_different_single_runs(self):
        allRuns = all_runs.AllRuns()

        singleRun = single_run.SingleRun()
        parsed_json = reader.read_file('src/tests/data/test_2.json')
        singleRun.load_json(parsed_json)
        added1 = allRuns.append_single_run_if_not_present(singleRun)
        df1 = allRuns.df.copy()

        singleRun = single_run.SingleRun()
        parsed_json = reader.read_file('src/tests/data/test_3.json')
        singleRun.load_json(parsed_json)
        added2 = allRuns.append_single_run_if_not_present(singleRun)
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

        singleRun = single_run.SingleRun()
        parsed_json = reader.read_file('src/tests/data/test_3.json')
        singleRun.load_json(parsed_json)
        added1 = allRuns.append_single_run_if_not_present(singleRun)
        df1 = allRuns.df.copy()

        singleRun = single_run.SingleRun()
        parsed_json = reader.read_file('src/tests/data/test_4.json')
        singleRun.load_json(parsed_json)
        added2 = allRuns.append_single_run_if_not_present(singleRun)
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
        added_single_runs = allRuns.load_files_in_dir("src/tests/data/test_load_files_in_dir", verbose=False)

        goldenSingleRun = single_run.SingleRun()
        goldenSingleRun.type = runTypes.RUN_TYPES_ENUM.T
        goldenSingleRun.total_time = 75
        goldenSingleRun.total_distance = 13.80
        goldenSingleRun.climb = 110
        goldenSingleRun.vspeed = 88
        goldenSingleRun.avg_pace = 326.09
        goldenSingleRun.where = "Park"
        goldenSingleRun.route = ""
        goldenSingleRun.date = datetime.datetime.strptime("26/11/2018", "%d/%m/%Y").date()
        goldenSingleRun.basic_dist[runTypes.BASIC_RUN_TYPES_ENUM.E] = 7.96
        goldenSingleRun.basic_dist[runTypes.BASIC_RUN_TYPES_ENUM.M] = 0
        goldenSingleRun.basic_dist[runTypes.BASIC_RUN_TYPES_ENUM.T] = 5.84
        goldenSingleRun.basic_dist[runTypes.BASIC_RUN_TYPES_ENUM.I] = 0
        goldenSingleRun.basic_dist[runTypes.BASIC_RUN_TYPES_ENUM.R] = 0
        goldenSingleRun.basic_time[runTypes.BASIC_RUN_TYPES_ENUM.E] = 3121.76
        goldenSingleRun.basic_time[runTypes.BASIC_RUN_TYPES_ENUM.M] = 0
        goldenSingleRun.basic_time[runTypes.BASIC_RUN_TYPES_ENUM.T] = 1378.24
        goldenSingleRun.basic_time[runTypes.BASIC_RUN_TYPES_ENUM.I] = 0
        goldenSingleRun.basic_time[runTypes.BASIC_RUN_TYPES_ENUM.R] = 0
        goldenSingleRun.basic_pace[runTypes.BASIC_RUN_TYPES_ENUM.E] = 392.18
        goldenSingleRun.basic_pace[runTypes.BASIC_RUN_TYPES_ENUM.M] = None
        goldenSingleRun.basic_pace[runTypes.BASIC_RUN_TYPES_ENUM.T] = 236
        goldenSingleRun.basic_pace[runTypes.BASIC_RUN_TYPES_ENUM.I] = None
        goldenSingleRun.basic_pace[runTypes.BASIC_RUN_TYPES_ENUM.R] = None

        goldenSingleRun2 = single_run.SingleRun()
        goldenSingleRun2.type = runTypes.RUN_TYPES_ENUM.E
        goldenSingleRun2.total_time = 60
        goldenSingleRun2.total_distance = 12.2
        goldenSingleRun2.climb = 100
        goldenSingleRun2.vspeed = 100
        goldenSingleRun2.avg_pace = 295.08
        goldenSingleRun2.where = "Park2"
        goldenSingleRun2.route = ""
        goldenSingleRun2.date = datetime.datetime.strptime("27/11/2018", "%d/%m/%Y").date()
        goldenSingleRun2.basic_dist[runTypes.BASIC_RUN_TYPES_ENUM.E] = 12.2
        goldenSingleRun2.basic_dist[runTypes.BASIC_RUN_TYPES_ENUM.M] = 0
        goldenSingleRun2.basic_dist[runTypes.BASIC_RUN_TYPES_ENUM.T] = 0
        goldenSingleRun2.basic_dist[runTypes.BASIC_RUN_TYPES_ENUM.I] = 0
        goldenSingleRun2.basic_dist[runTypes.BASIC_RUN_TYPES_ENUM.R] = 0
        goldenSingleRun2.basic_time[runTypes.BASIC_RUN_TYPES_ENUM.E] = 3600
        goldenSingleRun2.basic_time[runTypes.BASIC_RUN_TYPES_ENUM.M] = 0
        goldenSingleRun2.basic_time[runTypes.BASIC_RUN_TYPES_ENUM.T] = 0
        goldenSingleRun2.basic_time[runTypes.BASIC_RUN_TYPES_ENUM.I] = 0
        goldenSingleRun2.basic_time[runTypes.BASIC_RUN_TYPES_ENUM.R] = 0
        goldenSingleRun2.basic_pace[runTypes.BASIC_RUN_TYPES_ENUM.E] = 295.08
        goldenSingleRun2.basic_pace[runTypes.BASIC_RUN_TYPES_ENUM.M] = None
        goldenSingleRun2.basic_pace[runTypes.BASIC_RUN_TYPES_ENUM.T] = None
        goldenSingleRun2.basic_pace[runTypes.BASIC_RUN_TYPES_ENUM.I] = None
        goldenSingleRun2.basic_pace[runTypes.BASIC_RUN_TYPES_ENUM.R] = None

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
