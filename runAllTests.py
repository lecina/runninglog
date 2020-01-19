import unittest

import tests.test_all_runs as tAllRuns
import tests.test_single_run as tSingleRun
import tests.test_segment as tSegment
#import tests.single_test as tSing

def main():
    testSuite = unittest.TestSuite()

    testSuite.addTest(unittest.makeSuite(tAllRuns.TestAllRuns))
    testSuite.addTest(unittest.makeSuite(tSingleRun.TestSingleRun))
    testSuite.addTest(unittest.makeSuite(tSegment.TestSegment))
    #testSuite.addTest(unittest.makeSuite(tSing.TestSingleTest))

    runner = unittest.TextTestRunner()
    runner.run(testSuite)

if __name__ == "__main__":
    main()

