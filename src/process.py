class Process:
    """Represents a single process in CPU scheduling"""
    def __init__(self,processId,arrivalTime,burstTime,priority):
        self.processId=processId
        self.arrivalTime=arrivalTime
        self.burstTime=burstTime
        self.priority=priority

        #Values computed during scheduling
        self.completionTime=0
        self.turnaroundTime=0
        self.waitingTime=0
        self.responseTime=-1  #-1 means "not yet set"

        #Keep a copy of the original burst time (important for preemptive algorithms)
        self.originalBurstTime= burstTime