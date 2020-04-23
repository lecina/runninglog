from src.single_run import single_run
from src.single_run import runTypes
from src.constants import blockNames

import unittest
import datetime

class TestSingleTest(unittest.TestCase):
    def test_load_json5(self):
        singleRun = single_run.SingleRun()

        parsed_json = {
                        "type": "T",
                        "date": "01-01-2020",
                        "time": "1h",
                        "distance": 14,
                        "structure": [
                            {"type":"T", "distance":5, "time":"18min"},
                            {"type":"T", "distance":5, "time":"22min"}
                        ]
                      }

        singleRun.load_json(parsed_json)

        print singleRun

        self.assertEqual(singleRun.total_time, 60)

        self.assertEqual(singleRun.climb, 0)

        self.assertEqual(singleRun.where, "")

        dateObj = datetime.datetime.strptime("01/01/2020", "%d/%m/%Y").date()
        self.assertEqual(singleRun.date, dateObj)

        self.assertEqual(singleRun.basic_dist[runTypes.BASIC_RUN_TYPES_ENUM.E], 4)
        self.assertEqual(singleRun.basic_dist[runTypes.BASIC_RUN_TYPES_ENUM.M], 0)
        self.assertEqual(singleRun.basic_dist[runTypes.BASIC_RUN_TYPES_ENUM.T], 10)
        self.assertEqual(singleRun.basic_dist[runTypes.BASIC_RUN_TYPES_ENUM.I], 0)
        self.assertEqual(singleRun.basic_dist[runTypes.BASIC_RUN_TYPES_ENUM.R], 0)
        self.assertEqual(singleRun.basic_dist[runTypes.BASIC_RUN_TYPES_ENUM.WU], 0)
        self.assertEqual(singleRun.basic_dist[runTypes.BASIC_RUN_TYPES_ENUM.CD], 0)

        self.assertEqual(singleRun.basic_pace[runTypes.BASIC_RUN_TYPES_ENUM.E], 300)
        self.assertEqual(singleRun.basic_pace[runTypes.BASIC_RUN_TYPES_ENUM.M], None)
        self.assertEqual(singleRun.basic_pace[runTypes.BASIC_RUN_TYPES_ENUM.T], 240)
        self.assertEqual(singleRun.basic_pace[runTypes.BASIC_RUN_TYPES_ENUM.I], None)
        self.assertEqual(singleRun.basic_pace[runTypes.BASIC_RUN_TYPES_ENUM.R], None)
        self.assertEqual(singleRun.basic_pace[runTypes.BASIC_RUN_TYPES_ENUM.WU], None)
        self.assertEqual(singleRun.basic_pace[runTypes.BASIC_RUN_TYPES_ENUM.CD], None)

        self.assertEqual(singleRun.basic_time[runTypes.BASIC_RUN_TYPES_ENUM.E], 20*60)
        self.assertEqual(singleRun.basic_time[runTypes.BASIC_RUN_TYPES_ENUM.M], 0)
        self.assertEqual(singleRun.basic_time[runTypes.BASIC_RUN_TYPES_ENUM.T], 40*60)
        self.assertEqual(singleRun.basic_time[runTypes.BASIC_RUN_TYPES_ENUM.I], 0)
        self.assertEqual(singleRun.basic_time[runTypes.BASIC_RUN_TYPES_ENUM.R], 0)
        self.assertEqual(singleRun.basic_time[runTypes.BASIC_RUN_TYPES_ENUM.WU], 0)
        self.assertEqual(singleRun.basic_time[runTypes.BASIC_RUN_TYPES_ENUM.CD], 0)
