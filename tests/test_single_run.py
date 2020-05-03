import unittest
import datetime

import context
from runninglog.run import single
from runninglog.run import segment
from runninglog.run import types
from runninglog.constants import blockNames


class TestSingleRun(unittest.TestCase):
    def test_compute_avg_pace(self):
        singleRun = single.SingleRun()
        singleRun.distance = 10
        singleRun.time = 40
        avg_pace = singleRun.compute_avg_pace()
        self.assertEqual(avg_pace, 240)

    def test_fill_segments(self):
        singleRun = single.SingleRun()

        input_dict = [
            {"type":"E", "distance" : 2.36},
            {"type":"T", "distance": 5.84, "pace":"3:56"},
            {"type":"E", "distance" : 2.2}
        ]

        singleRun.fill_segments(input_dict)

        self.assertEqual(len(singleRun.run_structure), 3)

        for i, sgmnt in enumerate(singleRun.run_structure):
            if i == 0:
                self.assertAlmostEqual(sgmnt.distance, 2.36, 2)
            elif i == 1:
                self.assertAlmostEqual(sgmnt.distance, 5.84, 2)
                self.assertAlmostEqual(sgmnt.pace, 236, 2)
            elif i == 2:
                self.assertAlmostEqual(sgmnt.distance, 2.2, 2)

    def test_fill_segments_empty_segment(self):
        # Goal: assert that empty segments are not added
        singleRun = single.SingleRun()

        # First segment does not match a known type
        input_dict = [
            {},
            {"type":"T", "distance": 5.84, "pace":"3:56"},
            {"type":"E", "distance" : 2.2}
        ]

        singleRun.fill_segments(input_dict)

        self.assertEqual(len(singleRun.run_structure), 2)

        for i, sgmnt in enumerate(singleRun.run_structure):
            if i == 0:
                self.assertAlmostEqual(sgmnt.distance, 5.84, 2)
                self.assertAlmostEqual(sgmnt.pace, 236, 2)
            elif i == 1:
                self.assertAlmostEqual(sgmnt.distance, 2.2, 2)

    def test_fill_segments_invalid_segment(self):
        # Goal: assert that an exception is raised when an
        # invalid segment type is passed. This is already
        # tested in the segment's tests, but explicitly added
        # here as a remark

        singleRun = single.SingleRun()

        # First segment has an invalid type
        input_dict = [
            {"type":"AAA", "distance" : 2.2},
            {"type":"T", "distance": 5.84, "pace":"3:56"},
            {"type":"E", "distance" : 2.2}
        ]

        with self.assertRaises(Exception):
            singleRun.fill_segments(input_dict)

    def test_fill_dist_and_time_dictionaries(self):
        #Single run type is not passed to the structure

        singleRun = single.SingleRun()

        input_dict = [
            {"type":"E", "distance":2.36},
            {"type":"T", "distance":5.84, "pace":"3:56"},
            {"type":"E", "distance":2.2}
        ]

        #Segments are needed to be set in singleRun
        singleRun.fill_segments(input_dict)
        singleRun.fill_basic_volume_dict_with_structure_volume()

        golden_basic_dist = {}
        golden_basic_time = {}
        golden_basic_pace = {}
        for i in types.BASIC_RUN_TYPES_DICTIONARY.keys():
            golden_basic_dist[i] = 0
            golden_basic_time[i] = 0
            golden_basic_pace[i] = None

        golden_basic_dist[types.BASIC_RUN_TYPES_ENUM.E] = 4.56
        golden_basic_dist[types.BASIC_RUN_TYPES_ENUM.T] = 5.84
        golden_basic_time[types.BASIC_RUN_TYPES_ENUM.T] = 1378.24

        for i in types.BASIC_RUN_TYPES_DICTIONARY.keys():
            self.assertAlmostEqual(
                            singleRun.basic_dist[i],
                            golden_basic_dist[i],
                            2)
            self.assertAlmostEqual(
                            singleRun.basic_pace[i],
                            golden_basic_pace[i],
                            2)
            self.assertAlmostEqual(
                            singleRun.basic_time[i],
                            golden_basic_time[i],
                            2)

    def test_fill_basic_volume_dict_with_unassigned_volume(self):
        singleRun = single.SingleRun()

        #Equivalent distance and time distributions to structure:
        #[
        #    {"type":"M", "distance":10.0, "time":"40min"},
        #    {"type":"T", "distance":5.0, "time":"17min"}
        #]
        singleRun.basic_dist[types.BASIC_RUN_TYPES_ENUM.M] = 10
        singleRun.basic_dist[types.BASIC_RUN_TYPES_ENUM.T] = 5
        singleRun.basic_time[types.BASIC_RUN_TYPES_ENUM.M] = 40*60
        singleRun.basic_time[types.BASIC_RUN_TYPES_ENUM.T] = 17*60
        singleRun.type = types.RUN_TYPES_ENUM.E
        singleRun.distance = 20
        singleRun.time = 82

        singleRun.fill_basic_volume_dict_with_unassigned_volume()

        golden_basic_dist = {}
        golden_basic_time = {}
        for i in types.BASIC_RUN_TYPES_DICTIONARY.keys():
            golden_basic_dist[i] = 0
            golden_basic_time[i] = 0

        golden_basic_dist[types.BASIC_RUN_TYPES_ENUM.M] = 10
        golden_basic_dist[types.BASIC_RUN_TYPES_ENUM.T] = 5
        golden_basic_time[types.BASIC_RUN_TYPES_ENUM.M] = 40*60
        golden_basic_time[types.BASIC_RUN_TYPES_ENUM.T] = 17*60
        #See singleRun distance and time
        golden_basic_dist[types.BASIC_RUN_TYPES_ENUM.E] = 5
        golden_basic_time[types.BASIC_RUN_TYPES_ENUM.E] = 25*60


        for i in types.BASIC_RUN_TYPES_DICTIONARY.keys():
            self.assertAlmostEqual(
                            singleRun.basic_dist[i],
                            golden_basic_dist[i],
                            2)
            self.assertAlmostEqual(
                            singleRun.basic_time[i],
                            golden_basic_time[i],
                            2)

    def test_assign_to_easy_regardless_of_activity_type_if_no_struct(self):
        # The spare time and basic type is assigned to the easy type in
        # running activities if it is not specified as a structure

        singleRun = single.SingleRun()
        singleRun.type = types.RUN_TYPES_ENUM.M
        singleRun.distance = 10
        singleRun.time = 60
        #Note that by default basic_dist and basic_time are empty

        singleRun.fill_basic_volume_dict_with_unassigned_volume()

        golden_basic_dist = {}
        golden_basic_time = {}
        for i in types.BASIC_RUN_TYPES_DICTIONARY.keys():
            golden_basic_dist[i] = 0
            golden_basic_time[i] = 0

        golden_basic_dist[types.BASIC_RUN_TYPES_ENUM.E] = 10
        golden_basic_time[types.BASIC_RUN_TYPES_ENUM.E] = 60*60


        for i in types.BASIC_RUN_TYPES_DICTIONARY.keys():
            self.assertAlmostEqual(
                            singleRun.basic_dist[i],
                            golden_basic_dist[i],
                            2)
            self.assertAlmostEqual(
                            singleRun.basic_time[i],
                            golden_basic_time[i],
                            2)

    def test_load_json_struct_and_assign_to_E_type(self):
        # Although the single run is of type T, the spare
        # time and distance is assigned to the E type
        singleRun = single.SingleRun()

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

        self.assertEqual(singleRun.time, 75)
        self.assertEqual(singleRun.climb, 110)
        self.assertAlmostEqual(singleRun.vspeed, 88.0, 2)
        self.assertEqual(singleRun.where, "Park")
        self.assertEqual(singleRun.route, "Lap 1")
        self.assertEqual(singleRun.notes, "Feeling good!")
        self.assertEqual(singleRun.is_trail_running, False)
        self.assertEqual(singleRun.feeling, 5)
        dateObj = datetime.datetime.strptime("26/11/2018", "%d/%m/%Y").date()
        self.assertEqual(singleRun.date, dateObj)

        golden_basic_dist = {}
        golden_basic_time = {}
        golden_basic_pace = {}
        for i in types.BASIC_RUN_TYPES_DICTIONARY.keys():
            golden_basic_dist[i] = 0
            golden_basic_time[i] = 0
            golden_basic_pace[i] = None

        golden_basic_dist[types.BASIC_RUN_TYPES_ENUM.E] = 7.96
        golden_basic_dist[types.BASIC_RUN_TYPES_ENUM.T] = 5.84
        golden_basic_time[types.BASIC_RUN_TYPES_ENUM.E] = 3121.76
        golden_basic_time[types.BASIC_RUN_TYPES_ENUM.T] = 1378.24
        golden_basic_pace[types.BASIC_RUN_TYPES_ENUM.E] = 392.1809
        golden_basic_pace[types.BASIC_RUN_TYPES_ENUM.T] = 236

        for i in types.BASIC_RUN_TYPES_DICTIONARY.keys():
            self.assertAlmostEqual(
                            singleRun.basic_dist[i],
                            golden_basic_dist[i],
                            2)
            self.assertAlmostEqual(
                            singleRun.basic_pace[i],
                            golden_basic_pace[i],
                            2)
            self.assertAlmostEqual(
                            singleRun.basic_time[i],
                            golden_basic_time[i],
                            2)



    def test_load_json_no_struct(self):
        singleRun = single.SingleRun()

        parsed_json = {
                        "type": "E",
                        "trail": True,
                        "date": "26-11-2018",
                        "time": "1h15min",
                        "distance": 15,
                      }

        singleRun.load_json(parsed_json)

        self.assertEqual(singleRun.time, 75)
        self.assertEqual(singleRun.climb, 0)
        self.assertEqual(singleRun.where, "")
        self.assertEqual(singleRun.route, "")
        self.assertEqual(singleRun.feeling, None)
        self.assertEqual(singleRun.is_trail_running, True)
        dateObj = datetime.datetime.strptime("26/11/2018", "%d/%m/%Y").date()
        self.assertEqual(singleRun.date, dateObj)

        golden_basic_dist = {}
        golden_basic_time = {}
        golden_basic_pace = {}
        for i in types.BASIC_RUN_TYPES_DICTIONARY.keys():
            golden_basic_dist[i] = 0
            golden_basic_time[i] = 0
            golden_basic_pace[i] = None

        golden_basic_dist[types.BASIC_RUN_TYPES_ENUM.E] = 15
        golden_basic_time[types.BASIC_RUN_TYPES_ENUM.E] = 75*60
        golden_basic_pace[types.BASIC_RUN_TYPES_ENUM.E] = 300

        for i in types.BASIC_RUN_TYPES_DICTIONARY.keys():
            self.assertAlmostEqual(
                            singleRun.basic_dist[i],
                            golden_basic_dist[i],
                            2)
            self.assertAlmostEqual(
                            singleRun.basic_pace[i],
                            golden_basic_pace[i],
                            2)
            self.assertAlmostEqual(
                            singleRun.basic_time[i],
                            golden_basic_time[i],
                            2)

    def test_load_json_cross_training(self):
        # All dist/time/pace are assigned to key X in dictionary
        singleRun = single.SingleRun()

        parsed_json = {
                        "type": "X",
                        "date": "26-11-2018",
                        "time": "1h15min",
                        "distance": 15,
                      }

        singleRun.load_json(parsed_json)

        self.assertEqual(singleRun.time, 75)
        self.assertEqual(singleRun.climb, 0)
        self.assertEqual(singleRun.where, "")
        self.assertEqual(singleRun.route, "")
        self.assertEqual(singleRun.feeling, None)
        self.assertEqual(singleRun.is_trail_running, False)
        dateObj = datetime.datetime.strptime("26/11/2018", "%d/%m/%Y").date()
        self.assertEqual(singleRun.date, dateObj)

        golden_basic_dist = {}
        golden_basic_time = {}
        golden_basic_pace = {}
        for i in types.BASIC_RUN_TYPES_DICTIONARY.keys():
            golden_basic_dist[i] = 0
            golden_basic_time[i] = 0
            golden_basic_pace[i] = None

        golden_basic_dist[types.BASIC_RUN_TYPES_ENUM.X] = 15
        golden_basic_time[types.BASIC_RUN_TYPES_ENUM.X] = 75*60
        golden_basic_pace[types.BASIC_RUN_TYPES_ENUM.X] = 300

        for i in types.BASIC_RUN_TYPES_DICTIONARY.keys():
            self.assertAlmostEqual(
                            singleRun.basic_dist[i],
                            golden_basic_dist[i],
                            2)
            self.assertAlmostEqual(
                            singleRun.basic_pace[i],
                            golden_basic_pace[i],
                            2)
            self.assertAlmostEqual(
                            singleRun.basic_time[i],
                            golden_basic_time[i],
                            2)

    def test_load_json_cross_training_with_struct(self):
        # We can assign data to any basic type with an X activity.
        # In the case of cross training activities, the remaining
        # is assigned to the cross training activity type
        singleRun = single.SingleRun()

        parsed_json = {
                        "type": "X",
                        "date": "26-11-2018",
                        "time": "1h 15m",
                        "distance": 16,
                        "structure": [
                            {"type":"M", "distance":12, "time":"1h"}
                        ]
                      }

        singleRun.load_json(parsed_json)

        self.assertEqual(singleRun.time, 75)
        self.assertEqual(singleRun.climb, 0)
        self.assertEqual(singleRun.where, "")
        self.assertEqual(singleRun.route, "")
        self.assertEqual(singleRun.feeling, None)
        self.assertEqual(singleRun.is_trail_running, False)
        dateObj = datetime.datetime.strptime("26/11/2018", "%d/%m/%Y").date()
        self.assertEqual(singleRun.date, dateObj)

        golden_basic_dist = {}
        golden_basic_time = {}
        golden_basic_pace = {}
        for i in types.BASIC_RUN_TYPES_DICTIONARY.keys():
            golden_basic_dist[i] = 0
            golden_basic_time[i] = 0
            golden_basic_pace[i] = None

        golden_basic_dist[types.BASIC_RUN_TYPES_ENUM.M] = 12
        golden_basic_dist[types.BASIC_RUN_TYPES_ENUM.X] = 4
        golden_basic_time[types.BASIC_RUN_TYPES_ENUM.M] = 60*60
        golden_basic_time[types.BASIC_RUN_TYPES_ENUM.X] = 15*60
        golden_basic_pace[types.BASIC_RUN_TYPES_ENUM.M] = 300
        golden_basic_pace[types.BASIC_RUN_TYPES_ENUM.X] = 225

        for i in types.BASIC_RUN_TYPES_DICTIONARY.keys():
            self.assertAlmostEqual(
                            singleRun.basic_dist[i],
                            golden_basic_dist[i],
                            2)
            self.assertAlmostEqual(
                            singleRun.basic_pace[i],
                            golden_basic_pace[i],
                            2)
            self.assertAlmostEqual(
                            singleRun.basic_time[i],
                            golden_basic_time[i],
                            2)

    def test_load_json_assign_to_E_if_no_struct(self):
        # If no structure is defined, time and distance are assigned
        # to easy type regardless of type
        singleRun = single.SingleRun()

        parsed_json = {
                        "type": "T",
                        "date": "01-01-2020",
                        "time": "1h",
                        "distance": 14
                      }

        singleRun.load_json(parsed_json)

        self.assertEqual(singleRun.time, 60)
        self.assertEqual(singleRun.distance, 14)
        self.assertEqual(singleRun.climb, 0)
        self.assertEqual(singleRun.where, "")
        self.assertEqual(singleRun.route, "")
        self.assertEqual(singleRun.feeling, None)
        self.assertEqual(singleRun.is_trail_running, False)
        dateObj = datetime.datetime.strptime("01/01/2020", "%d/%m/%Y").date()
        self.assertEqual(singleRun.date, dateObj)

        golden_basic_dist = {}
        golden_basic_time = {}
        golden_basic_pace = {}
        for i in types.BASIC_RUN_TYPES_DICTIONARY.keys():
            golden_basic_dist[i] = 0
            golden_basic_time[i] = 0
            golden_basic_pace[i] = None

        golden_basic_dist[types.BASIC_RUN_TYPES_ENUM.T] = 14
        golden_basic_pace[types.BASIC_RUN_TYPES_ENUM.T] = 257.1428
        golden_basic_time[types.BASIC_RUN_TYPES_ENUM.T] = 60*60

        for i in types.BASIC_RUN_TYPES_DICTIONARY.keys():
            self.assertAlmostEqual(
                            singleRun.basic_dist[i],
                            golden_basic_dist[i],
                            2)
            self.assertAlmostEqual(
                            singleRun.basic_pace[i],
                            golden_basic_pace[i],
                            2)
            self.assertAlmostEqual(
                            singleRun.basic_time[i],
                            golden_basic_time[i],
                            2)


def main():
    return unittest.main(exit=False)

if __name__ == "__main__":
    main()
