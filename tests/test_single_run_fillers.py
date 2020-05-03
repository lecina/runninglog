import unittest
import datetime
import math

import context
from runninglog.run import single
from runninglog.run import types
from runninglog.constants import blockNames


class TestSingleRunFillers(unittest.TestCase):
    def test_fill_type_valid(self):
        singleRun = single.SingleRun()
        config_dict = {'type': blockNames.RunTypes.E}
        singleRun.fill_type(config_dict)
        self.assertEqual(
                singleRun.type,
                types.RUN_TYPES_ENUM.E)

    def test_fill_type_valid2(self):
        singleRun = single.SingleRun()
        config_dict = {'type': blockNames.RunTypes.T}
        singleRun.fill_type(config_dict)
        self.assertEqual(singleRun.type, types.RUN_TYPES_ENUM.T)

    def test_fill_type_missing(self):
        singleRun = single.SingleRun()
        config_dict = {}
        singleRun.fill_type(config_dict)
        self.assertEqual(singleRun.type, types.RUN_TYPES_ENUM.E)

    def test_fill_type_invalid(self):
        singleRun = single.SingleRun()

        config_dict = {'type':'aaa'}
        singleRun.fill_type(config_dict)
        self.assertEqual(singleRun.type, types.RUN_TYPES_ENUM.E)

    def test_fill_time_valid(self):
        singleRun = single.SingleRun()
        config_dict = {'time': '1h'}
        singleRun.fill_time(config_dict)
        self.assertEqual(singleRun.time, 60)

    def test_missing_time_raise_exception(self):
        singleRun = single.SingleRun()
        config_dict = {'invalid_key' : '1h'}
        with self.assertRaises(Exception):
            singleRun.fill_time(config_dict)

    def test_fill_distance_valid(self):
        singleRun = single.SingleRun()
        config_dict = {'distance': 10}
        singleRun.fill_distance(config_dict)
        self.assertEqual(singleRun.distance, 10)

    def test_missing_distance_raise_exception(self):
        singleRun = single.SingleRun()
        config_dict = {'invalid_key' : 10}
        with self.assertRaises(Exception):
            singleRun.fill_distance(config_dict)

    def test_fill_date_valid(self):
        singleRun = single.SingleRun()
        config_dict = {'date': '01/05/2020'}
        singleRun.fill_date(config_dict)
        dateObj = datetime.datetime.strptime("01/05/2020", "%d/%m/%Y").date()
        self.assertEqual(singleRun.date, dateObj)

    def test_missing_date_raise_exception(self):
        singleRun = single.SingleRun()
        config_dict = {'invalid_key' : '01/05/2020'}
        with self.assertRaises(Exception):
            singleRun.fill_date(config_dict)

    def test_fill_climb_valid(self):
        singleRun = single.SingleRun()
        config_dict = {'climb': 10}
        singleRun.fill_climb(config_dict)
        self.assertEqual(singleRun.climb, 10)

    def test_fill_climb_missing_value(self):
        singleRun = single.SingleRun()
        config_dict = {}
        singleRun.fill_type(config_dict)
        self.assertEqual(singleRun.climb, 0)

    def test_compute_vspeed(self):
        singleRun = single.SingleRun()
        config_dict = {'climb': 10}
        singleRun.climb = 600
        singleRun.time = 60
        singleRun.compute_vspeed()
        self.assertEqual(singleRun.vspeed, 600)

    def test_compute_vspeed_time_is_0(self):
        singleRun = single.SingleRun()
        config_dict = {'climb': 10}
        singleRun.climb = 600
        singleRun.time = 0
        singleRun.compute_vspeed()
        self.assertTrue(math.isnan(singleRun.vspeed))

    def test_fill_where(self):
        singleRun = single.SingleRun()
        config_dict = {'where': 'park'}
        singleRun.fill_where(config_dict)
        self.assertEqual(singleRun.where, 'park')

    def test_fill_where_missing(self):
        singleRun = single.SingleRun()
        config_dict = {}
        singleRun.fill_where(config_dict)
        self.assertEqual(singleRun.where, '')

    def test_fill_route(self):
        singleRun = single.SingleRun()
        config_dict = {'route': 'La Mitja'}
        singleRun.fill_route(config_dict)
        self.assertEqual(singleRun.route, 'La Mitja')

    def test_fill_route_missing(self):
        singleRun = single.SingleRun()
        config_dict = {}
        singleRun.fill_route(config_dict)
        self.assertEqual(singleRun.route, '')

    def test_fill_is_trail_running(self):
        singleRun = single.SingleRun()
        config_dict = {'trail': True}
        singleRun.fill_is_trail_running(config_dict)
        self.assertEqual(singleRun.is_trail_running, True)

    def test_fill_is_trail_running2(self):
        singleRun = single.SingleRun()
        config_dict = {'trail': 1}
        singleRun.fill_is_trail_running(config_dict)
        self.assertEqual(singleRun.is_trail_running, True)

    def test_fill_is_trail_running3(self):
        singleRun = single.SingleRun()
        config_dict = {'trail': False}
        singleRun.fill_is_trail_running(config_dict)
        self.assertEqual(singleRun.is_trail_running, False)

    def test_fill_is_trail_running_missing(self):
        singleRun = single.SingleRun()
        config_dict = {}
        singleRun.fill_is_trail_running(config_dict)
        self.assertEqual(singleRun.is_trail_running, False)

    def test_fill_feeling_valid(self):
        singleRun = single.SingleRun()
        config_dict = {'feeling': 5}
        singleRun.fill_feeling(config_dict)
        self.assertEqual(singleRun.feeling, 5)

    def test_fill_feeling_missing_value(self):
        singleRun = single.SingleRun()
        config_dict = {}
        singleRun.fill_feeling(config_dict)
        self.assertEqual(singleRun.feeling, None)

    def test_fill_notes(self):
        singleRun = single.SingleRun()
        config_dict = {'notes': 'Nice run!'}
        singleRun.fill_notes(config_dict)
        self.assertEqual(singleRun.notes, 'Nice run!')

    def test_fill_notes_missing(self):
        singleRun = single.SingleRun()
        config_dict = {}
        singleRun.fill_notes(config_dict)
        self.assertEqual(singleRun.notes, '')

def main():
    return unittest.main(exit=False)

if __name__ == "__main__":
    main()
