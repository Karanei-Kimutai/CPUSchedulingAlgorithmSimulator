from process import Process

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
        """Shortest Job First (non-preemptive)"""
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
        """SRTF (preemptive), ties broken for FCFS(earliest arrival)"""
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
        """SRTF(preemptive), ties broken by priority(higher value= higher priority)."""
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



