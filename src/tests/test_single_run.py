from single_run import single_run
from single_run import runTypes
from constants import blockNames

import unittest
import datetime

class TestSingleRun(unittest.TestCase):
    def test_compute_avg_pace(self):
        singleRun = single_run.SingleRun()
        singleRun.total_distance = 10
        singleRun.total_time = 40
        avg_pace = singleRun.compute_avg_pace()
        self.assertEqual(avg_pace, 240)

    def test_fill_info_with_dict(self):
        singleRun = single_run.SingleRun()

        input_dict = [
            {"type": "E", "distance" : 2.36},
            {"type":"T", "distance": 5.84, "pace":"3:56"},
            {"type":"E", "distance" : 2.2}
        ]

        singleRun.fill_basic_runtype_info_with_dict(input_dict)

        self.assertAlmostEqual(singleRun.basic_dist[runTypes.BASIC_RUN_TYPES_ENUM.E], 4.56, 2)
        self.assertEqual(singleRun.basic_dist[runTypes.BASIC_RUN_TYPES_ENUM.T], 5.84)

    def test_redistribute_distances_and_times(self):
        singleRun = single_run.SingleRun()

        input_dict = [
            {"type": "E", "distance" : 2.36},
            {"type":"T", "distance": 5.84, "pace":"3:56"},
            {"type":"E", "distance" : 2.2}
        ]

        singleRun.total_distance = 10.40

        singleRun.fill_basic_runtype_info_with_dict(input_dict)

        singleRun.redistribute_distances_and_times()

        self.assertAlmostEqual(singleRun.basic_dist[runTypes.BASIC_RUN_TYPES_ENUM.E], 4.56, 2)
        self.assertEqual(singleRun.basic_dist[runTypes.BASIC_RUN_TYPES_ENUM.T], 5.84)

    def test_load_json1(self):
        singleRun = single_run.SingleRun()

        parsed_json = {
                        "type": "T",
                        "date": "26-11-2018",
                        "time": "1h15min",
                        "distance": 13.8,
                        "climb": 110, 
                        "where":"Park",
                        "route":"Lap 1",
                        "notes": "Feeling good!",
                        "feeling": 5,
                        "structure":[
                            {"type":"E", "distance" : 2.36},
                            {"type":"T", "distance": 5.84, "pace":"3:56"},
                            {"type":"E", "distance" : 2.2}
                        ]
                      }

        singleRun.load_json(parsed_json)

        self.assertEqual(singleRun.total_time, 75)

        self.assertEqual(singleRun.climb, 110)

        self.assertAlmostEqual(singleRun.vspeed, 88.0, 2)

        self.assertEqual(singleRun.where, "Park")

        self.assertEqual(singleRun.route, "Lap 1")

        self.assertEqual(singleRun.notes, "Feeling good!")

        self.assertEqual(singleRun.feeling, 5)

        dateObj = datetime.datetime.strptime("26/11/2018", "%d/%m/%Y").date()
        self.assertEqual(singleRun.date, dateObj)

        self.assertAlmostEqual(singleRun.basic_dist[runTypes.BASIC_RUN_TYPES_ENUM.E], 7.96, 2)
        self.assertEqual(singleRun.basic_dist[runTypes.BASIC_RUN_TYPES_ENUM.T], 5.84)
        self.assertEqual(singleRun.basic_dist[runTypes.BASIC_RUN_TYPES_ENUM.M], 0)
        self.assertEqual(singleRun.basic_dist[runTypes.BASIC_RUN_TYPES_ENUM.I], 0)
        self.assertEqual(singleRun.basic_dist[runTypes.BASIC_RUN_TYPES_ENUM.R], 0)

        self.assertEqual(singleRun.basic_time[runTypes.BASIC_RUN_TYPES_ENUM.E], 3121.76)
        self.assertEqual(singleRun.basic_time[runTypes.BASIC_RUN_TYPES_ENUM.M], 0)
        self.assertEqual(singleRun.basic_time[runTypes.BASIC_RUN_TYPES_ENUM.T], 1378.24)
        self.assertEqual(singleRun.basic_time[runTypes.BASIC_RUN_TYPES_ENUM.I], 0)
        self.assertEqual(singleRun.basic_time[runTypes.BASIC_RUN_TYPES_ENUM.R], 0)

        self.assertAlmostEqual(singleRun.basic_pace[runTypes.BASIC_RUN_TYPES_ENUM.E], 392.1809,2)
        self.assertEqual(singleRun.basic_pace[runTypes.BASIC_RUN_TYPES_ENUM.M], None)
        self.assertEqual(singleRun.basic_pace[runTypes.BASIC_RUN_TYPES_ENUM.T], 236)
        self.assertEqual(singleRun.basic_pace[runTypes.BASIC_RUN_TYPES_ENUM.I], None)
        self.assertEqual(singleRun.basic_pace[runTypes.BASIC_RUN_TYPES_ENUM.R], None)


    def test_load_json2(self):
        singleRun = single_run.SingleRun()

        parsed_json = {
                        "type": "E",
                        "trail": True,
                        "date": "26-11-2018",
                        "time": "1h15min",
                        "distance": 15,
                      }

        singleRun.load_json(parsed_json)

        self.assertEqual(singleRun.total_time, 75)

        self.assertEqual(singleRun.climb, 0)

        self.assertEqual(singleRun.where, "")

        self.assertEqual(singleRun.route, "")

        self.assertEqual(singleRun.feeling, None)

        self.assertEqual(singleRun.trail_running, True)

        dateObj = datetime.datetime.strptime("26/11/2018", "%d/%m/%Y").date()
        self.assertEqual(singleRun.date, dateObj)

        self.assertEqual(singleRun.basic_dist[runTypes.BASIC_RUN_TYPES_ENUM.E], 15.0)
        self.assertEqual(singleRun.basic_dist[runTypes.BASIC_RUN_TYPES_ENUM.M], 0)
        self.assertEqual(singleRun.basic_dist[runTypes.BASIC_RUN_TYPES_ENUM.T], 0)
        self.assertEqual(singleRun.basic_dist[runTypes.BASIC_RUN_TYPES_ENUM.I], 0)
        self.assertEqual(singleRun.basic_dist[runTypes.BASIC_RUN_TYPES_ENUM.R], 0)

        self.assertEqual(singleRun.basic_pace[runTypes.BASIC_RUN_TYPES_ENUM.E], 300.0)
        self.assertEqual(singleRun.basic_pace[runTypes.BASIC_RUN_TYPES_ENUM.M], None)
        self.assertEqual(singleRun.basic_pace[runTypes.BASIC_RUN_TYPES_ENUM.T], None)
        self.assertEqual(singleRun.basic_pace[runTypes.BASIC_RUN_TYPES_ENUM.I], None)
        self.assertEqual(singleRun.basic_pace[runTypes.BASIC_RUN_TYPES_ENUM.R], None)

    def test_load_json3(self):
        singleRun = single_run.SingleRun()

        parsed_json = {
                        "type": "X",
                        "date": "26-11-2018",
                        "time": "1h15min",
                        "distance": 15,
                      }

        singleRun.load_json(parsed_json)

        self.assertEqual(singleRun.total_time, 75)

        self.assertEqual(singleRun.climb, 0)

        self.assertEqual(singleRun.where, "")

        self.assertEqual(singleRun.route, "")

        self.assertEqual(singleRun.feeling, None)

        dateObj = datetime.datetime.strptime("26/11/2018", "%d/%m/%Y").date()
        self.assertEqual(singleRun.date, dateObj)

        self.assertEqual(singleRun.basic_dist[runTypes.BASIC_RUN_TYPES_ENUM.E], 0)
        self.assertEqual(singleRun.basic_dist[runTypes.BASIC_RUN_TYPES_ENUM.M], 0)
        self.assertEqual(singleRun.basic_dist[runTypes.BASIC_RUN_TYPES_ENUM.T], 0)
        self.assertEqual(singleRun.basic_dist[runTypes.BASIC_RUN_TYPES_ENUM.I], 0)
        self.assertEqual(singleRun.basic_dist[runTypes.BASIC_RUN_TYPES_ENUM.R], 0)
        self.assertEqual(singleRun.basic_dist[runTypes.BASIC_RUN_TYPES_ENUM.X], 15.0)
        self.assertEqual(singleRun.basic_dist[runTypes.BASIC_RUN_TYPES_ENUM.XB], 0)

        self.assertEqual(singleRun.basic_pace[runTypes.BASIC_RUN_TYPES_ENUM.E], None)
        self.assertEqual(singleRun.basic_pace[runTypes.BASIC_RUN_TYPES_ENUM.M], None)
        self.assertEqual(singleRun.basic_pace[runTypes.BASIC_RUN_TYPES_ENUM.T], None)
        self.assertEqual(singleRun.basic_pace[runTypes.BASIC_RUN_TYPES_ENUM.I], None)
        self.assertEqual(singleRun.basic_pace[runTypes.BASIC_RUN_TYPES_ENUM.R], None)
        self.assertEqual(singleRun.basic_pace[runTypes.BASIC_RUN_TYPES_ENUM.X], 300.0)
        self.assertEqual(singleRun.basic_pace[runTypes.BASIC_RUN_TYPES_ENUM.XB], None)

    def test_load_json4(self):
        singleRun = single_run.SingleRun()

        parsed_json = {
                        "type": "X",
                        "date": "26-11-2018",
                        "time": "1h 15m",
                        "distance": 15,
                        "structure": [
                            {"type":"M", "distance":15}
                        ]
                      }

        singleRun.load_json(parsed_json)

        self.assertEqual(singleRun.total_time, 75)

        self.assertEqual(singleRun.climb, 0)

        self.assertEqual(singleRun.where, "")

        self.assertEqual(singleRun.route, "")

        self.assertEqual(singleRun.feeling, None)

        dateObj = datetime.datetime.strptime("26/11/2018", "%d/%m/%Y").date()
        self.assertEqual(singleRun.date, dateObj)

        self.assertEqual(singleRun.basic_dist[runTypes.BASIC_RUN_TYPES_ENUM.E], 0)
        self.assertEqual(singleRun.basic_dist[runTypes.BASIC_RUN_TYPES_ENUM.M], 15.0)
        self.assertEqual(singleRun.basic_dist[runTypes.BASIC_RUN_TYPES_ENUM.T], 0)
        self.assertEqual(singleRun.basic_dist[runTypes.BASIC_RUN_TYPES_ENUM.I], 0)
        self.assertEqual(singleRun.basic_dist[runTypes.BASIC_RUN_TYPES_ENUM.R], 0)

        self.assertEqual(singleRun.basic_pace[runTypes.BASIC_RUN_TYPES_ENUM.E], None)
        self.assertEqual(singleRun.basic_pace[runTypes.BASIC_RUN_TYPES_ENUM.M], None)
        self.assertEqual(singleRun.basic_pace[runTypes.BASIC_RUN_TYPES_ENUM.T], None)
        self.assertEqual(singleRun.basic_pace[runTypes.BASIC_RUN_TYPES_ENUM.I], None)
        self.assertEqual(singleRun.basic_pace[runTypes.BASIC_RUN_TYPES_ENUM.R], None)

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

        self.assertEqual(singleRun.total_time, 60)

        self.assertEqual(singleRun.climb, 0)

        self.assertEqual(singleRun.where, "")

        self.assertEqual(singleRun.route, "")

        self.assertEqual(singleRun.feeling, None)

        dateObj = datetime.datetime.strptime("01/01/2020", "%d/%m/%Y").date()
        self.assertEqual(singleRun.date, dateObj)

        self.assertEqual(singleRun.basic_dist[runTypes.BASIC_RUN_TYPES_ENUM.E], 4)
        self.assertEqual(singleRun.basic_dist[runTypes.BASIC_RUN_TYPES_ENUM.M], 0)
        self.assertEqual(singleRun.basic_dist[runTypes.BASIC_RUN_TYPES_ENUM.T], 10)
        self.assertEqual(singleRun.basic_dist[runTypes.BASIC_RUN_TYPES_ENUM.I], 0)
        self.assertEqual(singleRun.basic_dist[runTypes.BASIC_RUN_TYPES_ENUM.R], 0)

        self.assertEqual(singleRun.basic_pace[runTypes.BASIC_RUN_TYPES_ENUM.E], 300)
        self.assertEqual(singleRun.basic_pace[runTypes.BASIC_RUN_TYPES_ENUM.M], None)
        self.assertEqual(singleRun.basic_pace[runTypes.BASIC_RUN_TYPES_ENUM.T], 240)
        self.assertEqual(singleRun.basic_pace[runTypes.BASIC_RUN_TYPES_ENUM.I], None)
        self.assertEqual(singleRun.basic_pace[runTypes.BASIC_RUN_TYPES_ENUM.R], None)

        self.assertEqual(singleRun.basic_time[runTypes.BASIC_RUN_TYPES_ENUM.E], 20*60)
        self.assertEqual(singleRun.basic_time[runTypes.BASIC_RUN_TYPES_ENUM.M], 0)
        self.assertEqual(singleRun.basic_time[runTypes.BASIC_RUN_TYPES_ENUM.T], 40*60)
        self.assertEqual(singleRun.basic_time[runTypes.BASIC_RUN_TYPES_ENUM.I], 0)
        self.assertEqual(singleRun.basic_time[runTypes.BASIC_RUN_TYPES_ENUM.R], 0)

    def test_as_dict(self):
        singleRun = single_run.SingleRun()
        singleRun.type=runTypes.BASIC_RUN_TYPES_ENUM.E
        singleRun.total_time=75
        singleRun.total_distance=12
        singleRun.climb=110
        singleRun.vspeed=88
        singleRun.avg_pace=375
        singleRun.date = datetime.datetime.strptime("01/01/19", "%d/%m/%y").date()
        singleRun.where = "Park"
        singleRun.route  = "Lap 1"
        singleRun.notes = "Good!"
        singleRun.feeling = 5
        singleRun.basic_dist[runTypes.BASIC_RUN_TYPES_ENUM.E]=12
        singleRun.basic_time[runTypes.BASIC_RUN_TYPES_ENUM.E]=4500
        singleRun.basic_pace[runTypes.BASIC_RUN_TYPES_ENUM.E]=375

        golden_dict = {
            blockNames.Colnames.type : runTypes.RUN_TYPES_DICTIONARY[runTypes.BASIC_RUN_TYPES_ENUM.E],
            blockNames.Colnames.time : 75, 
            blockNames.Colnames.distance : 12, 
            blockNames.Colnames.climb : 110,
            blockNames.Colnames.vspeed : 88,
            blockNames.Colnames.avg_pace : 375,
            blockNames.Colnames.date : datetime.datetime.strptime("01/01/19", "%d/%m/%y").date(),
            blockNames.Colnames.trail : False,
            blockNames.Colnames.where : "Park",
            blockNames.Colnames.route : "Lap 1",
            blockNames.Colnames.notes : "Good!",
            blockNames.Colnames.feeling : 5,
            blockNames.Colnames.distE : 12,
            blockNames.Colnames.distM : 0, 
            blockNames.Colnames.distT : 0,
            blockNames.Colnames.distI : 0,
            blockNames.Colnames.distR : 0,
            blockNames.Colnames.distX : 0,
            blockNames.Colnames.distXB : 0,
            blockNames.Colnames.timeE : 4500,
            blockNames.Colnames.timeM : 0, 
            blockNames.Colnames.timeT : 0,
            blockNames.Colnames.timeI : 0,
            blockNames.Colnames.timeR : 0,
            blockNames.Colnames.timeX : 0,
            blockNames.Colnames.timeXB : 0,
            blockNames.Colnames.paceE : 375,
            blockNames.Colnames.paceM : None,
            blockNames.Colnames.paceT : None,
            blockNames.Colnames.paceI : None,
            blockNames.Colnames.paceR : None,
            blockNames.Colnames.paceX : None,
            blockNames.Colnames.paceXB : None
        }

        self.assertEqual(singleRun.as_dict(), golden_dict)


def main():
    return unittest.main(exit=False)

if __name__ == "__main__":
    main()
