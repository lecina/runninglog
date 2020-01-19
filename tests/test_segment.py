from single_run import segment

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
