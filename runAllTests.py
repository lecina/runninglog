import unittest

import tests.test_all_runs as tAllRuns
import tests.test_single_run as tSingleRun

def main():
    testSuite = unittest.TestSuite()

    testSuite.addTest(unittest.makeSuite(tAllRuns.TestAllRuns))
    testSuite.addTest(unittest.makeSuite(tSingleRun.TestSingleRun))

    runner = unittest.TextTestRunner()
    runner.run(testSuite)

if __name__ == "__main__":
    main()

