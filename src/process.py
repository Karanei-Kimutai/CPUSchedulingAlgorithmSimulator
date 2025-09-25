class Process:
    """
    Represents a process in the CPU scheduling simulation.
    """

    def __init__(self, processId, arrivalTime, burstTime, priority=1):
        self.processId = processId
        self.arrivalTime = arrivalTime
        self.burstTime = burstTime
        self.originalBurstTime = burstTime
        self.priority = priority

        # Metrics initialized to defaults
        self.completionTime = 0
        self.turnaroundTime = 0
        self.waitingTime = 0
        self.responseTime = -1  # -1 means not yet responded
