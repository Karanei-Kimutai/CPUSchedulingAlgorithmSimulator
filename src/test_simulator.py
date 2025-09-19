import unittest
from process import Process
from scheduler import Scheduler

class TestScheduler(unittest.TestCase):

    def setUp(self):
        """Set up a fixed list of processes for testing."""
        self.processes = [
            Process("P1", 0, 8, 2),
            Process("P2", 1, 4, 1),
            Process("P3", 2, 9, 3),
            Process("P4", 3, 5, 2),
        ]
        self.scheduler = Scheduler(self.processes)

    def test_fcfs(self):
        results = self.scheduler.firstComeFirstServe()
        # Values based on current implementation
        self.assertAlmostEqual(results["Average Waiting Time"], 8.75, places=2)
        self.assertAlmostEqual(results["Average Turnaround Time"], 15.25, places=2)
        self.assertAlmostEqual(results["Average Response Time"], 8.75, places=2)
        self.assertAlmostEqual(results["Throughput"], 4 / 26, places=3)

    def test_sjf(self):
        results = self.scheduler.shortestJobFirst()
        self.assertAlmostEqual(results["Average Waiting Time"], 7.75, places=2)
        self.assertAlmostEqual(results["Average Turnaround Time"], 14.25, places=2)
        self.assertAlmostEqual(results["Average Response Time"], 7.75, places=2)
        self.assertAlmostEqual(results["Throughput"], 4 / 26, places=3)

    def test_srtf_fcfs(self):
        results = self.scheduler.shortestRemainingTimeFirstFCFS()
        self.assertAlmostEqual(results["Average Waiting Time"], 6.50, places=2)
        self.assertAlmostEqual(results["Average Turnaround Time"], 13.00, places=2)
        self.assertAlmostEqual(results["Average Response Time"], 4.25, places=2)
        self.assertAlmostEqual(results["Throughput"], 4 / 26, places=3)

    def test_srtf_priority(self):
        results = self.scheduler.shortestRemainingTimeFirstPriority()
        self.assertAlmostEqual(results["Average Waiting Time"], 6.5, places=2)
        self.assertAlmostEqual(results["Average Turnaround Time"], 13.00, places=2)
        self.assertAlmostEqual(results["Average Response Time"], 4.25, places=2)
        self.assertAlmostEqual(results["Throughput"], 4 / 26, places=3)


if __name__ == "__main__":
    unittest.main()
