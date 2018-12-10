import unittest
import single_run

class TestSingleRun(unittest.TestCase):
    def test_parse_totaldistance1(self):
        singleRun = single_run.SingleRun()
        parsed_dist = singleRun.parse_total_distance("9.8km")
        self.assertEqual(parsed_dist, 9.8)

    def test_parse_totaldistance2(self):
        singleRun = single_run.SingleRun()
        parsed_dist = singleRun.parse_total_distance(9.8)
        self.assertEqual(parsed_dist, 9.8)

    def test_parse_totaldistance3(self):
        singleRun = single_run.SingleRun()
        parsed_dist = singleRun.parse_total_distance("9.8KM")
        self.assertEqual(parsed_dist, 9.8)

    def test_parse_totaldistance4(self):
        singleRun = single_run.SingleRun()
        parsed_dist = singleRun.parse_total_distance("9km")
        self.assertEqual(parsed_dist, 9)

    def test_parse_totaldistance5(self):
        singleRun = single_run.SingleRun()
        parsed_dist = singleRun.parse_total_distance("9")
        self.assertEqual(parsed_dist, 9)

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

    def test_parse_totaltime4(self):
        #change code in parse_total_time so that test passes
        singleRun = single_run.SingleRun()
        parsed_time = singleRun.parse_total_time("1h30min30s")
        self.assertEqual(parsed_time, 90.5)

    def test_parse_totaltime5(self):
        singleRun = single_run.SingleRun()
        parsed_time = singleRun.parse_total_time("1h30m30seg")
        self.assertEqual(parsed_time, 90.5)

def main():
    return unittest.main(exit=False)

if __name__ == "__main__":
    main()
