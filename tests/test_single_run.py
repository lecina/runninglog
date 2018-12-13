from single_run import single_run
from single_run import runTypes
from constants import blockNames

import unittest
import datetime

class TestSingleRun(unittest.TestCase):
    def test_parse_totaldistance1(self):
        singleRun = single_run.SingleRun()
        parsed_dist = singleRun.parse_distance("9.8km")
        self.assertEqual(parsed_dist, 9.8)

    def test_parse_totaldistance2(self):
        singleRun = single_run.SingleRun()
        parsed_dist = singleRun.parse_distance(9.8)
        self.assertEqual(parsed_dist, 9.8)

    def test_parse_totaldistance3(self):
        singleRun = single_run.SingleRun()
        parsed_dist = singleRun.parse_distance("9.8KM")
        self.assertEqual(parsed_dist, 9.8)

    def test_parse_totaldistance4(self):
        singleRun = single_run.SingleRun()
        parsed_dist = singleRun.parse_distance("9km")
        self.assertEqual(parsed_dist, 9)

    def test_parse_totaldistance5(self):
        singleRun = single_run.SingleRun()
        parsed_dist = singleRun.parse_distance("9")
        self.assertEqual(parsed_dist, 9)

    def test_parse_totaldistance6(self):
        singleRun = single_run.SingleRun()
        parsed_dist = singleRun.parse_distance("9.03")
        self.assertEqual(parsed_dist, 9.03)

    def test_parse_totaltime1(self):
        singleRun = single_run.SingleRun()
        parsed_time = singleRun.parse_total_time("1h")
        self.assertEqual(parsed_time, 60)

    def test_parse_totaltime2(self):
        singleRun = single_run.SingleRun()
        parsed_time = singleRun.parse_total_time("1m")
        self.assertEqual(parsed_time, 1)

    def test_parse_totaltime3(self):
        singleRun = single_run.SingleRun()
        parsed_time = singleRun.parse_total_time("30s")
        self.assertEqual(parsed_time, 0.5)

    def test_parse_totaltime4(self):
        singleRun = single_run.SingleRun()
        parsed_time = singleRun.parse_total_time("1h 30 min 30s")
        self.assertEqual(parsed_time, 90.5)

    def test_parse_totaltime5(self):
        singleRun = single_run.SingleRun()
        parsed_time = singleRun.parse_total_time("1h30min30s")
        self.assertEqual(parsed_time, 90.5)

    def test_parse_totaltime6(self):
        singleRun = single_run.SingleRun()
        parsed_time = singleRun.parse_total_time("1h30m30seg")
        self.assertEqual(parsed_time, 90.5)

    def test_parse_totaltime7(self):
        singleRun = single_run.SingleRun()
        parsed_time = singleRun.parse_total_time("1h30mi30seg")
        self.assertEqual(parsed_time, 90.5)

    def test_parse_totaltime8(self):
        singleRun = single_run.SingleRun()
        parsed_time = singleRun.parse_total_time("1h30mn30seg")
        self.assertEqual(parsed_time, 90.5)

    def test_parse_totaltime9(self):
        singleRun = single_run.SingleRun()
        parsed_time = singleRun.parse_total_time("1hr30mn30seg")
        self.assertEqual(parsed_time, 90.5)

    def test_parse_pace(self):
        singleRun = single_run.SingleRun()
        parsed_time = singleRun.parse_pace("3:56")
        self.assertEqual(parsed_time, 236)

    def test_parse_pace2(self):
        singleRun = single_run.SingleRun()
        parsed_time = singleRun.parse_pace(240)
        self.assertEqual(parsed_time, 240)

    def test_compute_avg_pace(self):
        singleRun = single_run.SingleRun()
        singleRun.total_distance = 10
        singleRun.total_time = 40
        avg_pace = singleRun.compute_avg_pace()
        self.assertEqual(avg_pace, 240)

    def test_fill_info_with_dict(self):
        singleRun = single_run.SingleRun()

        input_dict = {
            "WU" : {"distance" : 2.36},
            "T" : {"distance": 5.84, "pace":"3:56"},
            "CD" : {"distance" : 2.2}
        }

        singleRun.fill_basic_runtype_info_with_dict(input_dict)

        self.assertEqual(singleRun.basic_dist[runTypes.BASIC_RUN_TYPES.WU], 2.36)
        self.assertEqual(singleRun.basic_dist[runTypes.BASIC_RUN_TYPES.T], 5.84)
        self.assertEqual(singleRun.basic_dist[runTypes.BASIC_RUN_TYPES.CD], 2.2)
        self.assertEqual(singleRun.basic_pace[runTypes.BASIC_RUN_TYPES.WU], None)
        self.assertEqual(singleRun.basic_pace[runTypes.BASIC_RUN_TYPES.T], 236)
        self.assertEqual(singleRun.basic_pace[runTypes.BASIC_RUN_TYPES.CD], None)

    def test_redistribute_distances(self):
        singleRun = single_run.SingleRun()

        input_dict = {
            "WU" : {"distance" : 2.36},
            "T" : {"distance": 5.84, "pace":"3:56"},
            "CD" : {"distance" : 2.2}
        }

        singleRun.total_distance = 10.40

        singleRun.fill_basic_runtype_info_with_dict(input_dict)

        singleRun.redistribute_distances()


        self.assertAlmostEqual(singleRun.basic_dist[runTypes.BASIC_RUN_TYPES.E], 4.56, 2)
        self.assertEqual(singleRun.basic_dist[runTypes.BASIC_RUN_TYPES.T], 5.84)
        self.assertEqual(singleRun.basic_dist[runTypes.BASIC_RUN_TYPES.WU], 0)
        self.assertEqual(singleRun.basic_dist[runTypes.BASIC_RUN_TYPES.CD], 0)
        self.assertEqual(singleRun.basic_pace[runTypes.BASIC_RUN_TYPES.WU], None)
        self.assertEqual(singleRun.basic_pace[runTypes.BASIC_RUN_TYPES.T], 236)
        self.assertEqual(singleRun.basic_pace[runTypes.BASIC_RUN_TYPES.CD], None)

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
                        "structure":{
                            "E" : {"distance" : 2.36},
                            "T" : {"distance": 5.84, "pace":"3:56"},
                            "E" : {"distance" : 2.2}
                        }
                      }

        singleRun.load_json(parsed_json)

        self.assertEqual(singleRun.total_time, 75)

        self.assertEqual(singleRun.climb, 110)

        self.assertEqual(singleRun.where, "Park")

        self.assertEqual(singleRun.notes, "Feeling good!")

        dateObj = datetime.datetime.strptime("26/11/2018", "%d/%m/%Y")
        self.assertEqual(singleRun.date, dateObj)

        self.assertAlmostEqual(singleRun.basic_dist[runTypes.BASIC_RUN_TYPES.E], 7.96, 2)
        self.assertEqual(singleRun.basic_dist[runTypes.BASIC_RUN_TYPES.T], 5.84)
        self.assertEqual(singleRun.basic_dist[runTypes.BASIC_RUN_TYPES.M], 0)
        self.assertEqual(singleRun.basic_dist[runTypes.BASIC_RUN_TYPES.I], 0)
        self.assertEqual(singleRun.basic_dist[runTypes.BASIC_RUN_TYPES.R], 0)
        self.assertEqual(singleRun.basic_dist[runTypes.BASIC_RUN_TYPES.WU], 0)
        self.assertEqual(singleRun.basic_dist[runTypes.BASIC_RUN_TYPES.CD], 0)

        self.assertEqual(singleRun.basic_pace[runTypes.BASIC_RUN_TYPES.E], None)
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
                        "date": "26-11-2018",
                        "time": "1h15min",
                        "distance": 15,
                      }

        singleRun.load_json(parsed_json)

        self.assertEqual(singleRun.total_time, 75)

        self.assertEqual(singleRun.climb, 0)

        self.assertEqual(singleRun.where, "")

        dateObj = datetime.datetime.strptime("26/11/2018", "%d/%m/%Y")
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

        dateObj = datetime.datetime.strptime("26/11/2018", "%d/%m/%Y")
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

    def test_load_json4(self):
        singleRun = single_run.SingleRun()

        parsed_json = {
                        "type": "X",
                        "date": "26-11-2018",
                        "time": "1h 15m",
                        "distance": 15,
                        "structure": {
                            "M":{"distance":15}
                        }
                      }

        singleRun.load_json(parsed_json)

        self.assertEqual(singleRun.total_time, 75)

        self.assertEqual(singleRun.climb, 0)

        self.assertEqual(singleRun.where, "")

        dateObj = datetime.datetime.strptime("26/11/2018", "%d/%m/%Y")
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

    def test_as_dict(self):
        singleRun = single_run.SingleRun()
        singleRun.type="E"
        singleRun.total_time=75
        singleRun.total_distance=12
        singleRun.climb=110
        singleRun.avg_pace=375
        singleRun.date = datetime.datetime.strptime("01/01/19", "%d/%m/%y")
        singleRun.where = "Park"
        singleRun.notes = "Good!"
        singleRun.basic_dist[runTypes.BASIC_RUN_TYPES.E]=12
        singleRun.basic_pace[runTypes.BASIC_RUN_TYPES.E]=375

        golden_dict = {
            blockNames.Colnames.type : "E",
            blockNames.Colnames.time : 75, 
            blockNames.Colnames.distance : 12, 
            blockNames.Colnames.climb : 110,
            blockNames.Colnames.avg_pace : 375,
            blockNames.Colnames.date : datetime.datetime.strptime("01/01/19", "%d/%m/%y"),
            blockNames.Colnames.where : "Park",
            blockNames.Colnames.notes : "Good!",
            blockNames.Colnames.distE : 12,
            blockNames.Colnames.distM : 0, 
            blockNames.Colnames.distT : 0,
            blockNames.Colnames.distI : 0,
            blockNames.Colnames.distR : 0,
            blockNames.Colnames.paceE : 375,
            blockNames.Colnames.paceM : None,
            blockNames.Colnames.paceT : None,
            blockNames.Colnames.paceI : None,
            blockNames.Colnames.paceR : None
        }

        self.assertEqual(singleRun.as_dict(), golden_dict)


def main():
    return unittest.main(exit=False)

if __name__ == "__main__":
    main()
