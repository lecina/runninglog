import context

from single_run import segment
from single_run import runTypes

import unittest
import datetime

class TestSegment(unittest.TestCase):
    def test_parse_totaldistance1(self):
        sgmnt = segment.Segment()
        parsed_dist = sgmnt.parse_distance("9.8km")
        self.assertEqual(parsed_dist, 9.8)

    def test_parse_totaldistance2(self):
        sgmnt = segment.Segment()
        parsed_dist = sgmnt.parse_distance(9.8)
        self.assertEqual(parsed_dist, 9.8)

    def test_parse_totaldistance3(self):
        sgmnt = segment.Segment()
        parsed_dist = sgmnt.parse_distance("9.8KM")
        self.assertEqual(parsed_dist, 9.8)

    def test_parse_totaldistance4(self):
        sgmnt = segment.Segment()
        parsed_dist = sgmnt.parse_distance("9km")
        self.assertEqual(parsed_dist, 9)

    def test_parse_totaldistance5(self):
        sgmnt = segment.Segment()
        parsed_dist = sgmnt.parse_distance("9")
        self.assertEqual(parsed_dist, 9)

    def test_parse_totaldistance6(self):
        sgmnt = segment.Segment()
        parsed_dist = sgmnt.parse_distance("9.03")
        self.assertEqual(parsed_dist, 9.03)

    def test_parse_totaltime1(self):
        sgmnt = segment.Segment()
        parsed_time = sgmnt.parse_time("1h")
        self.assertEqual(parsed_time, 60)

    def test_parse_totaltime2(self):
        sgmnt = segment.Segment()
        parsed_time = sgmnt.parse_time("1m")
        self.assertEqual(parsed_time, 1)

    def test_parse_totaltime3(self):
        sgmnt = segment.Segment()
        parsed_time = sgmnt.parse_time("30s")
        self.assertEqual(parsed_time, 0.5)

    def test_parse_totaltime4(self):
        sgmnt = segment.Segment()
        parsed_time = sgmnt.parse_time("1h 30 min 30s")
        self.assertEqual(parsed_time, 90.5)

    def test_parse_totaltime5(self):
        sgmnt = segment.Segment()
        parsed_time = sgmnt.parse_time("1h30min30s")
        self.assertEqual(parsed_time, 90.5)

    def test_parse_totaltime6(self):
        sgmnt = segment.Segment()
        parsed_time = sgmnt.parse_time("1h30m30seg")
        self.assertEqual(parsed_time, 90.5)

    def test_parse_totaltime7(self):
        sgmnt = segment.Segment()
        parsed_time = sgmnt.parse_time("1h30mi30seg")
        self.assertEqual(parsed_time, 90.5)

    def test_parse_totaltime8(self):
        sgmnt = segment.Segment()
        parsed_time = sgmnt.parse_time("1h30mn30seg")
        self.assertEqual(parsed_time, 90.5)

    def test_parse_totaltime9(self):
        sgmnt = segment.Segment()
        parsed_time = sgmnt.parse_time("1hr30mn30seg")
        self.assertEqual(parsed_time, 90.5)

    def test_parse_pace(self):
        sgmnt = segment.Segment()
        parsed_time = sgmnt.parse_pace("3:56")
        self.assertEqual(parsed_time, 236)

    def test_parse_pace2(self):
        sgmnt = segment.Segment()
        parsed_time = sgmnt.parse_pace(240)
        self.assertEqual(parsed_time, 240)

    def test_create_segment(self):
        dictionary = {"type":"R", "distance":0.5, "pace":"3:15"}
        sgmnt = segment.Segment()
        sgmnt.create_segment(dictionary,repetition_number=1)

        self.assertEqual(sgmnt.type, runTypes.BASIC_RUN_TYPES_ENUM.R)
        self.assertEqual(sgmnt.distance, 0.5)
        self.assertEqual(sgmnt.time, 97.5)
        self.assertEqual(sgmnt.pace, 195)
        self.assertEqual(sgmnt.climb, 0)
        self.assertEqual(sgmnt.bpm, None)
        self.assertEqual(sgmnt.date, None)
        self.assertEqual(sgmnt.repetition, 1)

    def test_create_segment2(self):
        dictionary = {"type":"I", "distance":1, "time":"3min15sec", "climb":10, "bpm":160, "date":"31-01-2020"}
        sgmnt = segment.Segment()
        sgmnt.create_segment(dictionary,repetition_number=2)

        self.assertEqual(sgmnt.type, runTypes.BASIC_RUN_TYPES_ENUM.I)
        self.assertEqual(sgmnt.distance, 1)
        self.assertEqual(sgmnt.time, 195)
        self.assertEqual(sgmnt.pace, 195)
        self.assertEqual(sgmnt.climb, 10)
        self.assertEqual(sgmnt.bpm, 160)
        self.assertEqual(sgmnt.date, datetime.datetime.strptime("31-01-2020", "%d-%m-%Y").date())
        self.assertEqual(sgmnt.repetition, 2)

    def test_create_segment3(self):
        dictionary = {"type":"T", "distance" : 2.99, "pace":"12:21", "bpm":172, "time":"37min05sec"}
        sgmnt = segment.Segment()
        sgmnt.create_segment(dictionary,repetition_number=2)

        self.assertEqual(sgmnt.type, runTypes.BASIC_RUN_TYPES_ENUM.T)
        self.assertEqual(sgmnt.distance, 2.99)
        self.assertEqual(sgmnt.time, 2215.59)
        self.assertEqual(sgmnt.pace, 741)
        self.assertEqual(sgmnt.climb, 0)
        self.assertEqual(sgmnt.bpm, 172)
        self.assertEqual(sgmnt.date, None)
        self.assertEqual(sgmnt.repetition, 2)

