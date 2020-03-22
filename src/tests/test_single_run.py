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
            {"type": "WU", "distance" : 2.36},
            {"type":"T", "distance": 5.84, "pace":"3:56"},
            {"type":"CD", "distance" : 2.2}
        ]

        singleRun.fill_basic_runtype_info_with_dict(input_dict)

        self.assertEqual(singleRun.basic_dist[runTypes.BASIC_RUN_TYPES.WU], 2.36)
        self.assertEqual(singleRun.basic_dist[runTypes.BASIC_RUN_TYPES.T], 5.84)
        self.assertEqual(singleRun.basic_dist[runTypes.BASIC_RUN_TYPES.CD], 2.2)

    def test_redistribute_distances_and_times(self):
        singleRun = single_run.SingleRun()

        input_dict = [
            {"type": "WU", "distance" : 2.36},
            {"type":"T", "distance": 5.84, "pace":"3:56"},
            {"type":"CD", "distance" : 2.2}
        ]
        #input_dict = {
        #    "WU" : {"distance" : 2.36},
        #    "T" : {"distance": 5.84, "pace":"3:56"},
        #    "CD" : {"distance" : 2.2}
        #}

        singleRun.total_distance = 10.40

        singleRun.fill_basic_runtype_info_with_dict(input_dict)

        singleRun.redistribute_distances_and_times()


        self.assertAlmostEqual(singleRun.basic_dist[runTypes.BASIC_RUN_TYPES.E], 4.56, 2)
        self.assertEqual(singleRun.basic_dist[runTypes.BASIC_RUN_TYPES.T], 5.84)
        self.assertEqual(singleRun.basic_dist[runTypes.BASIC_RUN_TYPES.WU], 0)
        self.assertEqual(singleRun.basic_dist[runTypes.BASIC_RUN_TYPES.CD], 0)

    def test_load_json1(self):
        singleRun = single_run.SingleRun()

        parsed_json = {
                        "type": "T",
                        "date": "26-11-2018",
                        "time": "1h15min",
                        "distance": 13.8,
                        "climb": 110, 
                        "where":"Park",
                        "notes": "Feeling good!",
                        "structure":[
                            {"type":"E", "distance" : 2.36},
                            {"type":"T", "distance": 5.84, "pace":"3:56"},
                            {"type":"E", "distance" : 2.2}
                        ]
                      }

        singleRun.load_json(parsed_json)

        self.assertEqual(singleRun.total_time, 75)

        self.assertEqual(singleRun.climb, 110)

        self.assertEqual(singleRun.where, "Park")

        self.assertEqual(singleRun.notes, "Feeling good!")

        dateObj = datetime.datetime.strptime("26/11/2018", "%d/%m/%Y").date()
        self.assertEqual(singleRun.date, dateObj)

        self.assertAlmostEqual(singleRun.basic_dist[runTypes.BASIC_RUN_TYPES.E], 7.96, 2)
        self.assertEqual(singleRun.basic_dist[runTypes.BASIC_RUN_TYPES.T], 5.84)
        self.assertEqual(singleRun.basic_dist[runTypes.BASIC_RUN_TYPES.M], 0)
        self.assertEqual(singleRun.basic_dist[runTypes.BASIC_RUN_TYPES.I], 0)
        self.assertEqual(singleRun.basic_dist[runTypes.BASIC_RUN_TYPES.R], 0)
        self.assertEqual(singleRun.basic_dist[runTypes.BASIC_RUN_TYPES.WU], 0)
        self.assertEqual(singleRun.basic_dist[runTypes.BASIC_RUN_TYPES.CD], 0)

        self.assertEqual(singleRun.basic_time[runTypes.BASIC_RUN_TYPES.E], 3121.76)
        self.assertEqual(singleRun.basic_time[runTypes.BASIC_RUN_TYPES.M], 0)
        self.assertEqual(singleRun.basic_time[runTypes.BASIC_RUN_TYPES.T], 1378.24)
        self.assertEqual(singleRun.basic_time[runTypes.BASIC_RUN_TYPES.I], 0)
        self.assertEqual(singleRun.basic_time[runTypes.BASIC_RUN_TYPES.R], 0)
        self.assertEqual(singleRun.basic_time[runTypes.BASIC_RUN_TYPES.WU], 0)
        self.assertEqual(singleRun.basic_time[runTypes.BASIC_RUN_TYPES.CD], 0)

        self.assertAlmostEqual(singleRun.basic_pace[runTypes.BASIC_RUN_TYPES.E], 392.1809,2)
        self.assertEqual(singleRun.basic_pace[runTypes.BASIC_RUN_TYPES.M], None)
        self.assertEqual(singleRun.basic_pace[runTypes.BASIC_RUN_TYPES.T], 236)
        self.assertEqual(singleRun.basic_pace[runTypes.BASIC_RUN_TYPES.I], None)
        self.assertEqual(singleRun.basic_pace[runTypes.BASIC_RUN_TYPES.R], None)
        self.assertEqual(singleRun.basic_pace[runTypes.BASIC_RUN_TYPES.WU], None)
        self.assertEqual(singleRun.basic_pace[runTypes.BASIC_RUN_TYPES.CD], None)


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

        self.assertEqual(singleRun.trail_running, True)

        dateObj = datetime.datetime.strptime("26/11/2018", "%d/%m/%Y").date()
        self.assertEqual(singleRun.date, dateObj)

        self.assertEqual(singleRun.basic_dist[runTypes.BASIC_RUN_TYPES.E], 15.0)
        self.assertEqual(singleRun.basic_dist[runTypes.BASIC_RUN_TYPES.M], 0)
        self.assertEqual(singleRun.basic_dist[runTypes.BASIC_RUN_TYPES.T], 0)
        self.assertEqual(singleRun.basic_dist[runTypes.BASIC_RUN_TYPES.I], 0)
        self.assertEqual(singleRun.basic_dist[runTypes.BASIC_RUN_TYPES.R], 0)
        self.assertEqual(singleRun.basic_dist[runTypes.BASIC_RUN_TYPES.WU], 0)
        self.assertEqual(singleRun.basic_dist[runTypes.BASIC_RUN_TYPES.CD], 0)

        self.assertEqual(singleRun.basic_pace[runTypes.BASIC_RUN_TYPES.E], 300.0)
        self.assertEqual(singleRun.basic_pace[runTypes.BASIC_RUN_TYPES.M], None)
        self.assertEqual(singleRun.basic_pace[runTypes.BASIC_RUN_TYPES.T], None)
        self.assertEqual(singleRun.basic_pace[runTypes.BASIC_RUN_TYPES.I], None)
        self.assertEqual(singleRun.basic_pace[runTypes.BASIC_RUN_TYPES.R], None)
        self.assertEqual(singleRun.basic_pace[runTypes.BASIC_RUN_TYPES.WU], None)
        self.assertEqual(singleRun.basic_pace[runTypes.BASIC_RUN_TYPES.CD], None)

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

        dateObj = datetime.datetime.strptime("26/11/2018", "%d/%m/%Y").date()
        self.assertEqual(singleRun.date, dateObj)

        self.assertEqual(singleRun.basic_dist[runTypes.BASIC_RUN_TYPES.E], 0)
        self.assertEqual(singleRun.basic_dist[runTypes.BASIC_RUN_TYPES.M], 0)
        self.assertEqual(singleRun.basic_dist[runTypes.BASIC_RUN_TYPES.T], 0)
        self.assertEqual(singleRun.basic_dist[runTypes.BASIC_RUN_TYPES.I], 0)
        self.assertEqual(singleRun.basic_dist[runTypes.BASIC_RUN_TYPES.R], 0)
        self.assertEqual(singleRun.basic_dist[runTypes.BASIC_RUN_TYPES.WU], 0)
        self.assertEqual(singleRun.basic_dist[runTypes.BASIC_RUN_TYPES.CD], 0)
        self.assertEqual(singleRun.basic_dist[runTypes.BASIC_RUN_TYPES.X], 15.0)
        self.assertEqual(singleRun.basic_dist[runTypes.BASIC_RUN_TYPES.XB], 0)

        self.assertEqual(singleRun.basic_pace[runTypes.BASIC_RUN_TYPES.E], None)
        self.assertEqual(singleRun.basic_pace[runTypes.BASIC_RUN_TYPES.M], None)
        self.assertEqual(singleRun.basic_pace[runTypes.BASIC_RUN_TYPES.T], None)
        self.assertEqual(singleRun.basic_pace[runTypes.BASIC_RUN_TYPES.I], None)
        self.assertEqual(singleRun.basic_pace[runTypes.BASIC_RUN_TYPES.R], None)
        self.assertEqual(singleRun.basic_pace[runTypes.BASIC_RUN_TYPES.WU], None)
        self.assertEqual(singleRun.basic_pace[runTypes.BASIC_RUN_TYPES.CD], None)
        self.assertEqual(singleRun.basic_pace[runTypes.BASIC_RUN_TYPES.X], 300.0)
        self.assertEqual(singleRun.basic_pace[runTypes.BASIC_RUN_TYPES.XB], None)

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

        dateObj = datetime.datetime.strptime("26/11/2018", "%d/%m/%Y").date()
        self.assertEqual(singleRun.date, dateObj)

        self.assertEqual(singleRun.basic_dist[runTypes.BASIC_RUN_TYPES.E], 0)
        self.assertEqual(singleRun.basic_dist[runTypes.BASIC_RUN_TYPES.M], 15.0)
        self.assertEqual(singleRun.basic_dist[runTypes.BASIC_RUN_TYPES.T], 0)
        self.assertEqual(singleRun.basic_dist[runTypes.BASIC_RUN_TYPES.I], 0)
        self.assertEqual(singleRun.basic_dist[runTypes.BASIC_RUN_TYPES.R], 0)
        self.assertEqual(singleRun.basic_dist[runTypes.BASIC_RUN_TYPES.WU], 0)
        self.assertEqual(singleRun.basic_dist[runTypes.BASIC_RUN_TYPES.CD], 0)

        self.assertEqual(singleRun.basic_pace[runTypes.BASIC_RUN_TYPES.E], None)
        self.assertEqual(singleRun.basic_pace[runTypes.BASIC_RUN_TYPES.M], None)
        self.assertEqual(singleRun.basic_pace[runTypes.BASIC_RUN_TYPES.T], None)
        self.assertEqual(singleRun.basic_pace[runTypes.BASIC_RUN_TYPES.I], None)
        self.assertEqual(singleRun.basic_pace[runTypes.BASIC_RUN_TYPES.R], None)
        self.assertEqual(singleRun.basic_pace[runTypes.BASIC_RUN_TYPES.WU], None)
        self.assertEqual(singleRun.basic_pace[runTypes.BASIC_RUN_TYPES.CD], None)

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

        dateObj = datetime.datetime.strptime("01/01/2020", "%d/%m/%Y").date()
        self.assertEqual(singleRun.date, dateObj)

        self.assertEqual(singleRun.basic_dist[runTypes.BASIC_RUN_TYPES.E], 4)
        self.assertEqual(singleRun.basic_dist[runTypes.BASIC_RUN_TYPES.M], 0)
        self.assertEqual(singleRun.basic_dist[runTypes.BASIC_RUN_TYPES.T], 10)
        self.assertEqual(singleRun.basic_dist[runTypes.BASIC_RUN_TYPES.I], 0)
        self.assertEqual(singleRun.basic_dist[runTypes.BASIC_RUN_TYPES.R], 0)
        self.assertEqual(singleRun.basic_dist[runTypes.BASIC_RUN_TYPES.WU], 0)
        self.assertEqual(singleRun.basic_dist[runTypes.BASIC_RUN_TYPES.CD], 0)

        self.assertEqual(singleRun.basic_pace[runTypes.BASIC_RUN_TYPES.E], 300)
        self.assertEqual(singleRun.basic_pace[runTypes.BASIC_RUN_TYPES.M], None)
        self.assertEqual(singleRun.basic_pace[runTypes.BASIC_RUN_TYPES.T], 240)
        self.assertEqual(singleRun.basic_pace[runTypes.BASIC_RUN_TYPES.I], None)
        self.assertEqual(singleRun.basic_pace[runTypes.BASIC_RUN_TYPES.R], None)
        self.assertEqual(singleRun.basic_pace[runTypes.BASIC_RUN_TYPES.WU], None)
        self.assertEqual(singleRun.basic_pace[runTypes.BASIC_RUN_TYPES.CD], None)

        self.assertEqual(singleRun.basic_time[runTypes.BASIC_RUN_TYPES.E], 20*60)
        self.assertEqual(singleRun.basic_time[runTypes.BASIC_RUN_TYPES.M], 0)
        self.assertEqual(singleRun.basic_time[runTypes.BASIC_RUN_TYPES.T], 40*60)
        self.assertEqual(singleRun.basic_time[runTypes.BASIC_RUN_TYPES.I], 0)
        self.assertEqual(singleRun.basic_time[runTypes.BASIC_RUN_TYPES.R], 0)
        self.assertEqual(singleRun.basic_time[runTypes.BASIC_RUN_TYPES.WU], 0)
        self.assertEqual(singleRun.basic_time[runTypes.BASIC_RUN_TYPES.CD], 0)

    def test_as_dict(self):
        singleRun = single_run.SingleRun()
        singleRun.type=runTypes.RUN_TYPES.E
        singleRun.total_time=75
        singleRun.total_distance=12
        singleRun.climb=110
        singleRun.avg_pace=375
        singleRun.date = datetime.datetime.strptime("01/01/19", "%d/%m/%y").date()
        singleRun.where = "Park"
        singleRun.notes = "Good!"
        singleRun.basic_dist[runTypes.BASIC_RUN_TYPES.E]=12
        singleRun.basic_time[runTypes.BASIC_RUN_TYPES.E]=4500
        singleRun.basic_pace[runTypes.BASIC_RUN_TYPES.E]=375

        golden_dict = {
            blockNames.Colnames.type : runTypes.RUN_TYPES_DICTIONARY[runTypes.RUN_TYPES.E],
            blockNames.Colnames.time : 75, 
            blockNames.Colnames.distance : 12, 
            blockNames.Colnames.climb : 110,
            blockNames.Colnames.avg_pace : 375,
            blockNames.Colnames.date : datetime.datetime.strptime("01/01/19", "%d/%m/%y").date(),
            blockNames.Colnames.trail : False,
            blockNames.Colnames.where : "Park",
            blockNames.Colnames.notes : "Good!",
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
