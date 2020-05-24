import unittest
import os
import logging

from runninglog.io import reader


logger = logging.getLogger()
logger.setLevel(logging.CRITICAL)


class TestReader(unittest.TestCase):
    def test_get_json_files_in_subdirs(self):
        datafolder = os.path.join(os.path.split(__file__)[0], 'data', 'test_get_json_files')
        files = reader.get_files_in_subdirs(datafolder, "*.json")
        files.sort()

        goldenData = [
                        os.path.join('1','2','a2.json'), 
                        os.path.join('1','2','b2.json'), 
                        os.path.join('1','a1.json'), 
                        'a.json', 
                        'b.json',
                    ]
        goldenData = [os.path.join(datafolder, f) for f in goldenData]

        self.assertEqual(files, goldenData)

    def test_load_files_in_dir(self):
        # Adding runs from different files
        # File 1: using "list" to define list of runs
        # File 2: different run
        # File 3: repeating file 1 run. Only one should be added

        datafolder = os.path.join(os.path.split(__file__)[0], 'data', 'test_load_files_in_dir')
        read_run_descs = reader.get_json_runs_in_subdirs(datafolder, verbose=False)

        golden_descs = [
            {
                "list": [ 
                    {
                        "type": "T",
                        "date": "26-11-2018",
                        "time": "1h15min",
                        "distance": 13.8,
                        "climb": 110,
                        "where":"Park",
                        "route":"Lap 1",
                        "feeling": 4,
                        "trail": True,
                        "structure":[
                            {"type":"E", "distance" : 2.36},
                            {"type":"T", "distance": 5.84, "pace":"3:56"},
                            {"type":"E", "distance" : 2.2}
                        ]
                    },
                    {
                        "type": "T",
                        "date": "26-11-2018",
                        "time": "1h15min",
                        "distance": 13.8,
                        "climb": 110, 
                        "where":"Park",
                        "route":"Lap 1",
                        "feeling": 4,
                        "trail": True,
                        "structure":[
                            {"type":"E", "distance" : 2.36},
                            {"type":"T", "distance": 5.84, "pace":"3:56"},
                            {"type":"E", "distance" : 2.2}
                        ]
                    }
                ]
            },
            {
                "type": "E",
                "date": "27-11-2018",
                "time": "1h",
                "distance": 12.2,
                "climb": 100, 
                "where":"Park2"
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

        self.assertEqual(len(read_run_descs), 3)

def main():
    return unittest.main(exit=False)

if __name__ == "__main__":
    main()
