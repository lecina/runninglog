import unittest

import context
import test_all_runs as tAllRuns
import test_single_run as tSingleRun
import test_segment as tSegment
import test_single_run_fillers as tSingleRunFillers

def main():
    testSuite = unittest.TestSuite()

    testSuite.addTest(unittest.makeSuite(tAllRuns.TestAllRuns))
    testSuite.addTest(unittest.makeSuite(tSingleRun.TestSingleRun))
    testSuite.addTest(unittest.makeSuite(tSingleRunFillers.TestSingleRunFillers))
    testSuite.addTest(unittest.makeSuite(tSegment.TestSegment))
    #testSuite.addTest(unittest.makeSuite(tSing.TestSingleTest))

    runner = unittest.TextTestRunner()
    runner.run(testSuite)

if __name__ == "__main__":
    main()

