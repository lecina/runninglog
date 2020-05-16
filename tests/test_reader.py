import unittest
import os

from runninglog.io import reader

class TestReader(unittest.TestCase):
    def test_get_json_files_in_subdirs(self):
        datafolder = os.path.join(os.path.split(__file__)[0], 'data', 'test_get_json_files')
        files = reader.get_json_files_in_subdirs(datafolder)
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

def main():
    return unittest.main(exit=False)

if __name__ == "__main__":
    main()
