import unittest
import datetime
import logging

import context
from runninglog.run import segment
from runninglog.run import types


logger = logging.getLogger()
logger.setLevel(logging.CRITICAL)


class TestSegment(unittest.TestCase):
    def test_fill_segment_distance_and_pace(self):
        dictionary = {
                        "type":"R", 
                        "distance":0.5, 
                        "pace":"3:15", 
                        "repetition":1
                    }
        sgmnt = segment.Segment()
        sgmnt.fill_segment(dictionary)

        self.assertEqual(sgmnt.type, types.BASIC_RUN_TYPES_ENUM.R)
        self.assertEqual(sgmnt.distance, 0.5)
        self.assertEqual(sgmnt.time, 97.5)
        self.assertEqual(sgmnt.pace, 195)
        self.assertEqual(sgmnt.climb, 0)
        self.assertEqual(sgmnt.bpm, None)
        self.assertEqual(sgmnt.date, None)
        self.assertEqual(sgmnt.repetition, 1)

    def test_fill_segment_distance_and_time(self):
        dictionary = {
                        "type":"I", 
                        "distance":1, 
                        "time":"3min15sec", 
                        "climb":10,
                        "bpm":160, 
                        "date":"31-01-2020", 
                        "repetition":2
                    }
        sgmnt = segment.Segment()
        sgmnt.fill_segment(dictionary)

        self.assertEqual(sgmnt.type, types.BASIC_RUN_TYPES_ENUM.I)
        self.assertEqual(sgmnt.distance, 1)
        self.assertEqual(sgmnt.time, 195)
        self.assertEqual(sgmnt.pace, 195)
        self.assertEqual(sgmnt.climb, 10)
        self.assertEqual(sgmnt.bpm, 160)
        self.assertEqual(sgmnt.date, datetime.datetime.strptime("31-01-2020", "%d-%m-%Y").date())
        self.assertEqual(sgmnt.repetition, 2)

    def test_fill_segment_distance_pace_and_time(self):
        dictionary = {
                        "type":"T", 
                        "distance" : 2.99, 
                        "pace":"12:21", 
                        "bpm":172, 
                        "time":"37min05sec",
                        "repetition":2
                    }
        sgmnt = segment.Segment()
        sgmnt.fill_segment(dictionary)

        self.assertEqual(sgmnt.type, types.BASIC_RUN_TYPES_ENUM.T)
        self.assertEqual(sgmnt.distance, 2.99)
        self.assertEqual(sgmnt.time, 2215.59)
        self.assertEqual(sgmnt.pace, 741)
        self.assertEqual(sgmnt.climb, 0)
        self.assertEqual(sgmnt.bpm, 172)
        self.assertEqual(sgmnt.date, None)
        self.assertEqual(sgmnt.repetition, 2)

    def test_fill_segment_invalid_type_raises_exception(self):
        dictionary = {"type":"AAA"}
        sgmnt = segment.Segment()
        with self.assertRaises(ValueError):
            sgmnt.fill_segment(dictionary)

def main():
    return unittest.main(exit=False)

if __name__ == "__main__":
    main()
