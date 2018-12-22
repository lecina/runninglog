from all_runs import all_runs
from single_run import single_run, runTypes

import unittest
import datetime

class TestAllRuns(unittest.TestCase):
    def test_read_single_run1(self):
        allRuns = all_runs.AllRuns()
        singleRun = allRuns.read_single_run("tests/data/test_2.json")

        goldenSingleRun = single_run.SingleRun()
        goldenSingleRun.type = runTypes.RUN_TYPES.T
        goldenSingleRun.total_time = 75
        goldenSingleRun.total_distance = 13.80
        goldenSingleRun.climb = 110
        goldenSingleRun.avg_pace = 326.087
        goldenSingleRun.where = "Park"
        goldenSingleRun.date = datetime.datetime.strptime("26/11/2018", "%d/%m/%Y")
        goldenSingleRun.basic_dist[runTypes.BASIC_RUN_TYPES.E] = 7.96
        goldenSingleRun.basic_dist[runTypes.BASIC_RUN_TYPES.M] = 0
        goldenSingleRun.basic_dist[runTypes.BASIC_RUN_TYPES.T] = 5.84
        goldenSingleRun.basic_dist[runTypes.BASIC_RUN_TYPES.I] = 0
        goldenSingleRun.basic_dist[runTypes.BASIC_RUN_TYPES.R] = 0
        goldenSingleRun.basic_pace[runTypes.BASIC_RUN_TYPES.E] = None
        goldenSingleRun.basic_pace[runTypes.BASIC_RUN_TYPES.M] = None
        goldenSingleRun.basic_pace[runTypes.BASIC_RUN_TYPES.T] = 236
        goldenSingleRun.basic_pace[runTypes.BASIC_RUN_TYPES.I] = None
        goldenSingleRun.basic_pace[runTypes.BASIC_RUN_TYPES.R] = None

        self.assertEqual(singleRun, goldenSingleRun)

    def test_read_single_run2(self):
        allRuns = all_runs.AllRuns()
        singleRun = allRuns.read_single_run("tests/data/test_3.json")

        goldenSingleRun = single_run.SingleRun()
        goldenSingleRun.type = runTypes.RUN_TYPES.E
        goldenSingleRun.total_time = 60
        goldenSingleRun.total_distance = 12.2
        goldenSingleRun.climb = 100
        goldenSingleRun.avg_pace = 295.082
        goldenSingleRun.where = "Park2"
        goldenSingleRun.date = datetime.datetime.strptime("27/11/2018", "%d/%m/%Y")
        goldenSingleRun.basic_dist[runTypes.BASIC_RUN_TYPES.E] = 60
        goldenSingleRun.basic_dist[runTypes.BASIC_RUN_TYPES.M] = 0
        goldenSingleRun.basic_dist[runTypes.BASIC_RUN_TYPES.T] = 0
        goldenSingleRun.basic_dist[runTypes.BASIC_RUN_TYPES.I] = 0
        goldenSingleRun.basic_dist[runTypes.BASIC_RUN_TYPES.R] = 0
        goldenSingleRun.basic_pace[runTypes.BASIC_RUN_TYPES.E] = None
        goldenSingleRun.basic_pace[runTypes.BASIC_RUN_TYPES.M] = None
        goldenSingleRun.basic_pace[runTypes.BASIC_RUN_TYPES.T] = None
        goldenSingleRun.basic_pace[runTypes.BASIC_RUN_TYPES.I] = None
        goldenSingleRun.basic_pace[runTypes.BASIC_RUN_TYPES.R] = None

        self.assertEqual(singleRun, goldenSingleRun)

    def test_read_single_run3(self):
        allRuns = all_runs.AllRuns()
        singleRuns = allRuns.read_single_run("tests/data/test_1.json")

        goldenSingleRun = single_run.SingleRun()
        goldenSingleRun.type = runTypes.RUN_TYPES.T
        goldenSingleRun.total_time = 75
        goldenSingleRun.total_distance = 13.80
        goldenSingleRun.climb = 110
        goldenSingleRun.avg_pace = 326.087
        goldenSingleRun.where = "Park"
        goldenSingleRun.date = datetime.datetime.strptime("26/12/2018", "%d/%m/%Y")
        goldenSingleRun.basic_dist[runTypes.BASIC_RUN_TYPES.E] = 7.96
        goldenSingleRun.basic_dist[runTypes.BASIC_RUN_TYPES.M] = 0
        goldenSingleRun.basic_dist[runTypes.BASIC_RUN_TYPES.T] = 5.84
        goldenSingleRun.basic_dist[runTypes.BASIC_RUN_TYPES.I] = 0
        goldenSingleRun.basic_dist[runTypes.BASIC_RUN_TYPES.R] = 0
        goldenSingleRun.basic_pace[runTypes.BASIC_RUN_TYPES.E] = None
        goldenSingleRun.basic_pace[runTypes.BASIC_RUN_TYPES.M] = None
        goldenSingleRun.basic_pace[runTypes.BASIC_RUN_TYPES.T] = 236
        goldenSingleRun.basic_pace[runTypes.BASIC_RUN_TYPES.I] = None
        goldenSingleRun.basic_pace[runTypes.BASIC_RUN_TYPES.R] = None

        goldenSingleRun2 = single_run.SingleRun()
        goldenSingleRun2.type = runTypes.RUN_TYPES.E
        goldenSingleRun2.total_time = 60
        goldenSingleRun2.total_distance = 12.2
        goldenSingleRun2.climb = 100
        goldenSingleRun2.avg_pace = 295.082
        goldenSingleRun2.where = "Park2"
        goldenSingleRun2.date = datetime.datetime.strptime("27/12/2018", "%d/%m/%Y")
        goldenSingleRun2.basic_dist[runTypes.BASIC_RUN_TYPES.E] = 60
        goldenSingleRun2.basic_dist[runTypes.BASIC_RUN_TYPES.M] = 0
        goldenSingleRun2.basic_dist[runTypes.BASIC_RUN_TYPES.T] = 0
        goldenSingleRun2.basic_dist[runTypes.BASIC_RUN_TYPES.I] = 0
        goldenSingleRun2.basic_dist[runTypes.BASIC_RUN_TYPES.R] = 0
        goldenSingleRun2.basic_pace[runTypes.BASIC_RUN_TYPES.E] = None
        goldenSingleRun2.basic_pace[runTypes.BASIC_RUN_TYPES.M] = None
        goldenSingleRun2.basic_pace[runTypes.BASIC_RUN_TYPES.T] = None
        goldenSingleRun2.basic_pace[runTypes.BASIC_RUN_TYPES.I] = None
        goldenSingleRun2.basic_pace[runTypes.BASIC_RUN_TYPES.R] = None

        self.assertEqual(singleRuns[0], goldenSingleRun)
        self.assertEqual(singleRuns[1], goldenSingleRun2)

def main():
    return unittest.main(exit=False)

if __name__ == "__main__":
    main()
