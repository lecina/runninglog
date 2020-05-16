import unittest
from datetime import datetime
import os
import pandas as pd

import context
from runninglog.run import all_runs, single, segment, types
from runninglog.reader import reader


class TestAllRuns(unittest.TestCase):
    def test_read_run(self):
        # Testing that the run is properly loaded, creating
        # corresponding structures
        run_desc = {
            "type": "T",
            "trail": True,
            "date": "26-11-2018",
            "time": "1h15min",
            "distance": 13.8,
            "climb": 110, 
            "where":"Park",
            "route":"Lap 1",
            "feeling": 4,
            "structure":[
                {"type":"E", "distance" : 2.36},
                {"type":"T", "distance": 5.84, "pace":"3:56"},
                {"type":"E", "distance" : 2.2}
            ]
        }

        allRuns = all_runs.AllRuns()
        singleRun = allRuns.read_run(run_desc)

        self.assertEqual(len(singleRun),1)
        singleRun = singleRun[0]

        goldenSingleRun = single.SingleRun()
        goldenSingleRun.type = types.RUN_TYPES_ENUM.T
        goldenSingleRun.time = 75
        goldenSingleRun.distance = 13.80
        goldenSingleRun.climb = 110
        goldenSingleRun.vspeed = 88
        goldenSingleRun.pace = 326.087
        goldenSingleRun.where = "Park"
        goldenSingleRun.route = "Lap 1"
        goldenSingleRun.is_trail_running = True
        goldenSingleRun.feeling = 4
        goldenSingleRun.date = datetime.strptime("26/11/2018", "%d/%m/%Y").date()

        # Build basic dictionaries
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

        goldenSingleRun.basic_dist = golden_basic_dist
        goldenSingleRun.basic_time = golden_basic_time
        goldenSingleRun.basic_pace = golden_basic_pace

        # Build segments
        segment1 = segment.Segment()
        segment1.type = types.BASIC_RUN_TYPES_ENUM.E
        segment1.distance = 2.36
        segment1.repetition = 0
        segment1.is_trail_running = True
        segment1.feeling = 4
        segment1.date = datetime.strptime("26/11/2018", "%d/%m/%Y").date()
        
        segment2 = segment.Segment()
        segment2.type = types.BASIC_RUN_TYPES_ENUM.T
        segment2.distance = 5.84
        segment2.pace = 236
        segment2.time = 1378.24
        segment2.repetition = 1
        segment2.is_trail_running = True
        segment2.feeling = 4
        segment2.date = datetime.strptime("26/11/2018", "%d/%m/%Y").date()

        segment3 = segment.Segment()
        segment3.type = types.BASIC_RUN_TYPES_ENUM.E
        segment3.distance = 2.2
        segment3.repetition = 2
        segment3.is_trail_running = True
        segment3.feeling = 4
        segment3.date = datetime.strptime("26/11/2018", "%d/%m/%Y").date()

        goldenSingleRun.structure = [
            segment1,
            segment2,
            segment3
        ]

        self.assertEqual(singleRun, goldenSingleRun)


    def test_read_run2(self):
        # Testing that the run is properly loaded, creating
        # corresponding structures

        #allRuns = all_runs.AllRuns()
        #datafile = os.path.join(os.path.split(__file__)[0], 'data', 'test_3.json')
        #singleRun = allRuns.read_run_in_file(datafile, verbose=False)

        run_desc = {
            "type": "E",
            "date": "27-11-2018",
            "time": "1h",
            "distance": 12.2,
            "climb": 100, 
            "where":"Park2"
        }

        allRuns = all_runs.AllRuns()
        singleRun = allRuns.read_run(run_desc)

        self.assertEqual(len(singleRun),1)
        singleRun = singleRun[0]

        goldenSingleRun = single.SingleRun()
        goldenSingleRun.type = types.RUN_TYPES_ENUM.E
        goldenSingleRun.time = 60
        goldenSingleRun.distance = 12.2
        goldenSingleRun.climb = 100
        goldenSingleRun.vspeed = 100
        goldenSingleRun.pace = 295.081967213 
        goldenSingleRun.trail_running = False
        goldenSingleRun.where = "Park2"
        goldenSingleRun.route = ""
        goldenSingleRun.date = datetime.strptime("27/11/2018", "%d/%m/%Y").date()

        # Build basic dictionaries
        golden_basic_dist = {}
        golden_basic_time = {}
        golden_basic_pace = {}
        for i in types.BASIC_RUN_TYPES_DICTIONARY.keys():
            golden_basic_dist[i] = 0
            golden_basic_time[i] = 0
            golden_basic_pace[i] = None
        golden_basic_dist[types.BASIC_RUN_TYPES_ENUM.E] = 12.2
        golden_basic_time[types.BASIC_RUN_TYPES_ENUM.E] = 3600
        golden_basic_pace[types.BASIC_RUN_TYPES_ENUM.E] = 295.081967213

        goldenSingleRun.basic_dist = golden_basic_dist
        goldenSingleRun.basic_time = golden_basic_time
        goldenSingleRun.basic_pace = golden_basic_pace

        self.assertEqual(singleRun, goldenSingleRun)

    def test_read_single_run3(self):
        # Testing that the run is properly loaded, creating
        # corresponding structures; List of runs correspond
        # to previous test

        #allRuns = all_runs.AllRuns()
        #datafile = os.path.join(os.path.split(__file__)[0], 'data', 'test_1.json')
        #singleRuns = allRuns.read_run_in_file(datafile, verbose=False)

        run_desc = {
            "list": [
                {
                    "type": "T",
                    "trail": True,
                    "date": "26-11-2018",
                    "time": "1h15min",
                    "distance": 13.8,
                    "climb": 110, 
                    "where":"Park",
                    "route":"Lap 1",
                    "feeling": 4,
                    "structure":[
                        {"type":"E", "distance" : 2.36},
                        {"type":"T", "distance": 5.84, "pace":"3:56"},
                        {"type":"E", "distance" : 2.2}
                    ]
                },
                {
                    "type": "E",
                    "date": "27-11-2018",
                    "time": "1h",
                    "distance": 12.2,
                    "climb": 100, 
                    "where":"Park2"
                }
            ]
        }

        allRuns = all_runs.AllRuns()
        singleRun = allRuns.read_run(run_desc)

        self.assertEqual(len(singleRun),2)

        # First run
        goldenSingleRun = single.SingleRun()
        goldenSingleRun.type = types.RUN_TYPES_ENUM.T
        goldenSingleRun.time = 75
        goldenSingleRun.distance = 13.80
        goldenSingleRun.climb = 110
        goldenSingleRun.vspeed = 88
        goldenSingleRun.pace = 326.087
        goldenSingleRun.where = "Park"
        goldenSingleRun.route = "Lap 1"
        goldenSingleRun.is_trail_running = True
        goldenSingleRun.feeling = 4
        goldenSingleRun.date = datetime.strptime("26/11/2018", "%d/%m/%Y").date()

        # Build basic dictionaries
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

        goldenSingleRun.basic_dist = golden_basic_dist
        goldenSingleRun.basic_time = golden_basic_time
        goldenSingleRun.basic_pace = golden_basic_pace

        # Build segments
        segment1 = segment.Segment()
        segment1.type = types.BASIC_RUN_TYPES_ENUM.E
        segment1.distance = 2.36
        segment1.repetition = 0
        segment1.feeling = 4
        segment1.is_trail_running = True
        segment1.date = datetime.strptime("26/11/2018", "%d/%m/%Y").date()
        
        segment2 = segment.Segment()
        segment2.type = types.BASIC_RUN_TYPES_ENUM.T
        segment2.distance = 5.84
        segment2.pace = 236
        segment2.time = 1378.24
        segment2.repetition = 1
        segment2.is_trail_running = True
        segment2.feeling = 4
        segment2.date = datetime.strptime("26/11/2018", "%d/%m/%Y").date()

        segment3 = segment.Segment()
        segment3.type = types.BASIC_RUN_TYPES_ENUM.E
        segment3.distance = 2.2
        segment3.repetition = 2
        segment3.is_trail_running = True
        segment3.feeling = 4
        segment3.date = datetime.strptime("26/11/2018", "%d/%m/%Y").date()

        goldenSingleRun.structure = [
            segment1,
            segment2,
            segment3
        ]

        # Second run
        goldenSingleRun2 = single.SingleRun()
        goldenSingleRun2.type = types.RUN_TYPES_ENUM.E
        goldenSingleRun2.time = 60
        goldenSingleRun2.distance = 12.2
        goldenSingleRun2.climb = 100
        goldenSingleRun2.vspeed = 100
        goldenSingleRun2.pace = 295.081967213 
        goldenSingleRun2.trail_running = False
        goldenSingleRun2.where = "Park2"
        goldenSingleRun2.route = ""
        goldenSingleRun2.date = datetime.strptime("27/11/2018", "%d/%m/%Y").date()

        # Build basic dictionaries
        golden_basic_dist = {}
        golden_basic_time = {}
        golden_basic_pace = {}
        for i in types.BASIC_RUN_TYPES_DICTIONARY.keys():
            golden_basic_dist[i] = 0
            golden_basic_time[i] = 0
            golden_basic_pace[i] = None
        golden_basic_dist[types.BASIC_RUN_TYPES_ENUM.E] = 12.2
        golden_basic_time[types.BASIC_RUN_TYPES_ENUM.E] = 3600
        golden_basic_pace[types.BASIC_RUN_TYPES_ENUM.E] = 295.081967213

        goldenSingleRun2.basic_dist = golden_basic_dist
        goldenSingleRun2.basic_time = golden_basic_time
        goldenSingleRun2.basic_pace = golden_basic_pace

        self.assertEqual(singleRun[0], goldenSingleRun)
        self.assertEqual(singleRun[1], goldenSingleRun2)

    def test_not_adding_duplicated_single_run(self):
        # Runs are repeated and is solely added once

        run_desc = {
            "list": [
                {
                    "type": "T",
                    "trail": True,
                    "date": "26-11-2018",
                    "time": "1h15min",
                    "distance": 13.8,
                    "climb": 110, 
                    "where":"Park",
                    "route":"Lap 1",
                    "feeling": 4,
                    "structure":[
                        {"type":"E", "distance" : 2.36},
                        {"type":"T", "distance": 5.84, "pace":"3:56"},
                        {"type":"E", "distance" : 2.2}
                    ]
                },
                {
                    "type": "T",
                    "trail": True,
                    "date": "26-11-2018",
                    "time": "1h15min",
                    "distance": 13.8,
                    "climb": 110, 
                    "where":"Park",
                    "route":"Lap 1",
                    "feeling": 4,
                    "structure":[
                        {"type":"E", "distance" : 2.36},
                        {"type":"T", "distance": 5.84, "pace":"3:56"},
                        {"type":"E", "distance" : 2.2}
                    ]
                }
            ]
        }

        allRuns = all_runs.AllRuns()
        singleRun = allRuns.read_run(run_desc)

        # 2 single runs read
        self.assertEqual(len(singleRun), 2)

        for run in singleRun:
            allRuns.add_run(run)

        # Only one is added
        self.assertEqual(len(allRuns.runs), 1)

    def test_adding_two_different_runs(self):
        # The first two runs are repeated and is solely added once

        run_desc = {
            "list": [
                {
                    "type": "T",
                    "trail": True,
                    "date": "26-11-2018",
                    "time": "1h15min",
                    "distance": 13.8,
                    "climb": 110, 
                    "where":"Park",
                    "route":"Lap 1",
                    "feeling": 4,
                    "structure":[
                        {"type":"E", "distance" : 2.36},
                        {"type":"T", "distance": 5.84, "pace":"3:56"},
                        {"type":"E", "distance" : 2.2}
                    ]
                },
                {
                    "type": "T",
                    "trail": True,
                    "date": "26-11-2018",
                    "time": "1h15min",
                    "distance": 13.8,
                    "climb": 110, 
                    "where":"Park",
                    "route":"Lap 1",
                    "feeling": 4,
                    "structure":[
                        {"type":"E", "distance" : 2.36},
                        {"type":"T", "distance": 5.84, "pace":"3:56"},
                        {"type":"E", "distance" : 2.2}
                    ]
                },
                {
                    "type": "E",
                    "date": "27-11-2018",
                    "time": "1h",
                    "distance": 12.2,
                    "climb": 100, 
                    "where":"Park2"
                }
            ]
        }

        allRuns = all_runs.AllRuns()
        singleRun = allRuns.read_run(run_desc)

        # 3 single runs read
        self.assertEqual(len(singleRun), 3)

        for run in singleRun:
            allRuns.add_run(run)

        # Only two are added
        self.assertEqual(len(allRuns.runs), 2)


    def test_load_files_in_dir(self):
        # Adding runs from different files
        # File 1: using "list" to define list of runs
        # File 2: different run
        # File 3: repeating file 1 run. Only one should be added

        allRuns = all_runs.AllRuns()
        datafolder = os.path.join(os.path.split(__file__)[0], 'data', 'test_load_files_in_dir')
        added_single_runs = allRuns.load_files_in_dir(datafolder)

        # First run
        goldenSingleRun = single.SingleRun()
        goldenSingleRun.type = types.RUN_TYPES_ENUM.T
        goldenSingleRun.time = 75
        goldenSingleRun.distance = 13.80
        goldenSingleRun.climb = 110
        goldenSingleRun.vspeed = 88
        goldenSingleRun.pace = 326.087
        goldenSingleRun.where = "Park"
        goldenSingleRun.route = "Lap 1"
        goldenSingleRun.is_trail_running = True
        goldenSingleRun.feeling = 4
        goldenSingleRun.date = datetime.strptime("26/11/2018", "%d/%m/%Y").date()

        # Build basic dictionaries
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

        goldenSingleRun.basic_dist = golden_basic_dist
        goldenSingleRun.basic_time = golden_basic_time
        goldenSingleRun.basic_pace = golden_basic_pace

        # Build segments
        segment1 = segment.Segment()
        segment1.type = types.BASIC_RUN_TYPES_ENUM.E
        segment1.distance = 2.36
        segment1.repetition = 0
        segment1.feeling = 4
        segment1.is_trail_running = True
        segment1.date = datetime.strptime("26/11/2018", "%d/%m/%Y").date()
        
        segment2 = segment.Segment()
        segment2.type = types.BASIC_RUN_TYPES_ENUM.T
        segment2.distance = 5.84
        segment2.pace = 236
        segment2.time = 1378.24
        segment2.repetition = 1
        segment2.is_trail_running = True
        segment2.feeling = 4
        segment2.date = datetime.strptime("26/11/2018", "%d/%m/%Y").date()

        segment3 = segment.Segment()
        segment3.type = types.BASIC_RUN_TYPES_ENUM.E
        segment3.distance = 2.2
        segment3.repetition = 2
        segment3.is_trail_running = True
        segment3.feeling = 4
        segment3.date = datetime.strptime("26/11/2018", "%d/%m/%Y").date()

        goldenSingleRun.structure = [
            segment1,
            segment2,
            segment3
        ]

        # Second run
        goldenSingleRun2 = single.SingleRun()
        goldenSingleRun2.type = types.RUN_TYPES_ENUM.E
        goldenSingleRun2.time = 60
        goldenSingleRun2.distance = 12.2
        goldenSingleRun2.climb = 100
        goldenSingleRun2.vspeed = 100
        goldenSingleRun2.pace = 295.081967213 
        goldenSingleRun2.trail_running = False
        goldenSingleRun2.where = "Park2"
        goldenSingleRun2.route = ""
        goldenSingleRun2.date = datetime.strptime("27/11/2018", "%d/%m/%Y").date()

        # Build basic dictionaries
        golden_basic_dist = {}
        golden_basic_time = {}
        golden_basic_pace = {}
        for i in types.BASIC_RUN_TYPES_DICTIONARY.keys():
            golden_basic_dist[i] = 0
            golden_basic_time[i] = 0
            golden_basic_pace[i] = None
        golden_basic_dist[types.BASIC_RUN_TYPES_ENUM.E] = 12.2
        golden_basic_time[types.BASIC_RUN_TYPES_ENUM.E] = 3600
        golden_basic_pace[types.BASIC_RUN_TYPES_ENUM.E] = 295.081967213

        goldenSingleRun2.basic_dist = golden_basic_dist
        goldenSingleRun2.basic_time = golden_basic_time
        goldenSingleRun2.basic_pace = golden_basic_pace

        self.assertEqual(len(allRuns.runs), 2)
        self.assertEqual(allRuns.runs[0], goldenSingleRun)
        self.assertEqual(allRuns.runs[1], goldenSingleRun2)

def main():
    return unittest.main(exit=False)

if __name__ == "__main__":
    main()
