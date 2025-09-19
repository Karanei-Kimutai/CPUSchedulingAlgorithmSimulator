from process import Process
from utils import safePriorityInput

class Scheduler:
    """Implements different CPU scheduling algorithms."""
    def __init__(self, processes):
        self.processes=processes

    def resetProcesses(self):
        """Resets all processes before running another algorithm."""
        for process in self.processes:
            process.completionTime=0
            process.turnaroundTime=0
            process.waitingTime=0
            process.responseTime=-1
            process.burstTime=process.originalBurstTime  #restore burst time


    def calculatePerformance(self,finishedProcesses):
        """Calculate average metrics and throughput for a list of finished processes."""
        numberOfProcesses=len(finishedProcesses)

        totalWaitingTime=sum(process.waitingTime for process in finishedProcesses)
        totalTurnaroundTime=sum(process.turnaroundTime for process in finishedProcesses)
        totalResponseTime=sum(process.responseTime for process in finishedProcesses)

        averageWaitingTime=totalWaitingTime/numberOfProcesses
        averageTurnaroundTime= totalTurnaroundTime/numberOfProcesses
        averageResponseTime=totalResponseTime/numberOfProcesses

        totalTime=max(process.completionTime for process in finishedProcesses)
        throughput=numberOfProcesses/ totalTime

        return{
            "Average Waiting Time": averageWaitingTime,
            "Average Turnaround Time": averageTurnaroundTime,
            "Average Response Time": averageResponseTime,
            "Throughput": throughput,
        }

    #Scheduling algorithms
    def firstComeFirstServe(self):
        """First come first serve (non-preemptive)"""
        self.resetProcesses()
        currentTime=0
        finishedProcesses=[]

        """
        The sorted() function in Python takes a list and returns a new list where the elements are arranged in order, without changing the original list.
        In this case, we are sorting self.processes, which is a list of Process objects.
        The key argument tells sorted() what property of each object to use for comparison.
        Here, we use "key=lambda process: process.arrivalTime".
        lambda process: process.arrivalTime means: for each process, return its arrivalTime, and sort based on that.
        This ensures that the processes are arranged from the earliest arrivalTime to the latest arrivalTime.
        """
        for process in sorted(self.processes,key=lambda process:process.arrivalTime):
            if currentTime< process.arrivalTime:
                currentTime=process.arrivalTime
            if process.responseTime==-1:
                process.responseTime=currentTime-process.arrivalTime
            currentTime+= process.burstTime
            process.completionTime=currentTime
            process.turnaroundTime=process.completionTime-process.arrivalTime
            process.waitingTime=process.turnaroundTime-process.burstTime
            finishedProcesses.append(process)

        return self.calculatePerformance(finishedProcesses)

    def shortestJobFirst(self):
        """
        This method implements the non-preemptive Shortest Job First scheduling algorithm.
        It begins by resetting all process states and initializing the current time to zero.
        The algorithm maintains a list of unfinished processes and iterates until all processes are completed.
        At each step, it identifies all processes that have arrived by the current time.
        If no processes are available, it advances time to the next process arrival. From the available processes, it selects the one with the smallest burst time (shortest job).
        For the selected process, it calculates response time (if this is the first time it's scheduled), updates the current time by adding the process's burst time, then computes completion time, turnaround time, and waiting time.
        The completed process is moved to the finished list and removed from the pending list.
        Finally, it returns performance metrics for all completed processes.
        """
        self.resetProcesses()
        currentTime=0
        finishedProcesses=[]
        processesLeft=self.processes[:] #creates a copy of the self.processes list

        while processesLeft: #While the list is not empty, empty list= False and list with elements= True
            availableProcesses=[
                process for process in processesLeft if process.arrivalTime<= currentTime
            ]
            if not availableProcesses:
                currentTime=min(process.arrivalTime for process in processesLeft)
                continue

            currentProcess=min(availableProcesses, key=lambda process:process.burstTime)
            if currentProcess.responseTime==-1:
                currentProcess.responseTime=currentTime-currentProcess.arrivalTime
            currentTime+=currentProcess.burstTime
            currentProcess.completionTime=currentTime
            currentProcess.turnaroundTime=currentProcess.completionTime-currentProcess.arrivalTime
            currentProcess.waitingTime=currentProcess.turnaroundTime-currentProcess.burstTime
            finishedProcesses.append(currentProcess)
            processesLeft.remove(currentProcess)


        return self.calculatePerformance(finishedProcesses)


    def shortestRemainingTimeFirstFCFS(self):
        """
        This method implements the preemptive Shortest Remaining Time First algorithm with FCFS tie-breaking.
        It starts by resetting process states and initializing time to zero.
        The algorithm maintains separate lists for unfinished processes and a ready queue of processes that have arrived but not completed.
        It processes in time increments, checking for new arrivals at each time unit.
        If no processes are ready, it advances time to the next arrival.
        From the ready queue, it selects the process with the smallest remaining burst time, breaking ties by choosing the earliest arrival (FCFS).
        It records response time when a process first runs, then executes the process for one time unit.
        When a process completes (burst time reaches zero), it calculates completion metrics and moves it to the finished list.
        This continues until all processes are completed, then returns performance metrics.
        """
        self.resetProcesses()
        currentTime=0
        processesLeft=self.processes[:]
        finishedProcesses=[]
        readyQueue=[]

        while processesLeft or readyQueue:
            readyQueue.extend(
                [process for process in processesLeft if process.arrivalTime<= currentTime]
            )
            processesLeft=[process for process in processesLeft if process.arrivalTime > currentTime]
            if not readyQueue:
                currentTime=min(process.arrivalTime for process in processesLeft)
                continue
            currentProcess= min(readyQueue, key=lambda process:(process.burstTime,process.arrivalTime))
            if currentProcess.responseTime==-1:
                currentProcess.responseTime=currentTime-currentProcess.arrivalTime

            currentProcess.burstTime-=1
            currentTime+=1
            if currentProcess.burstTime==0:
                currentProcess.completionTime=currentTime
                currentProcess.turnaroundTime=currentProcess.completionTime-currentProcess.arrivalTime
                currentProcess.waitingTime=currentProcess.turnaroundTime-currentProcess.originalBurstTime
                finishedProcesses.append(currentProcess)
                readyQueue.remove(currentProcess)

        return self.calculatePerformance(finishedProcesses)


    def shortestRemainingTimeFirstPriority(self):
        """
        This method implements the preemptive Shortest Remaining Time First algorithm with priority-based tie-breaking.
        It first ensures all processes have priority values assigned, prompting for input if missing.
        Like the FCFS version, it maintains unfinished processes and a ready queue, processing in single time unit increments.
        The key difference is in tie-breaking: when multiple processes have the same remaining burst time, it selects the one with the highest priority (largest priority value).
        It updates response time on first execution, processes for one time unit, and handles completion by calculating final metrics.
        The algorithm continues until all processes finish, then returns comprehensive performance statistics including average waiting time, turnaround time, response time, and throughput.
        """
        #Ask for priorities
        for process in self.processes:
            if process.priority is None:
                process.priority=safePriorityInput(f"Enter priority for Process {process.processId}: ")
        self.resetProcesses()
        currentTime=0
        processesLeft=self.processes[:]
        finishedProcesses=[]
        readyQueue=[]

        while processesLeft or readyQueue:
            readyQueue.extend(
                [process for process in processesLeft if process.arrivalTime<=currentTime]
            )
            processesLeft=[process for process in processesLeft if process.arrivalTime> currentTime]

            if not readyQueue:
                currentTime=min(process.arrivalTime for process in processesLeft)
                continue

            currentProcess=min(
                readyQueue,key=lambda process: (process.burstTime,-process.priority)
            )
            if currentProcess.responseTime==-1:
                currentProcess.responseTime=currentTime-currentProcess.arrivalTime

            currentProcess.burstTime-=1
            currentTime+=1

            if currentProcess.burstTime==0:
                currentProcess.completionTime=currentTime
                currentProcess.turnaroundTime=currentProcess.completionTime-currentProcess.arrivalTime
                currentProcess.waitingTime=currentProcess.turnaroundTime-currentProcess.originalBurstTime
                finishedProcesses.append(currentProcess)
                readyQueue.remove(currentProcess)

        return self.calculatePerformance(finishedProcesses)



