# src/scheduler.py

"""
Scheduler module: implements CPU scheduling algorithms and performance calculations.

Priority convention: higher numeric value = higher priority.
All methods return a dictionary with keys:
  "Average Waiting Time", "Average Turnaround Time", "Average Response Time", "Throughput"
"""

from copy import deepcopy
from collections import deque
from typing import List, Dict
from process import Process


class Scheduler:
    def __init__(self, processes: List[Process], contextSwitchTime: int = 0):
        """
        Initialize scheduler.

        Args:
            processes: list of Process objects (will not be mutated; deep copies are used).
            contextSwitchTime: fixed overhead (int) applied when switching CPU between processes.
        """
        self.originalProcesses = deepcopy(processes)
        self.contextSwitchTime = int(contextSwitchTime)

    # ---------------- Utility ---------------- #

    def _makeProcessCopy(self) -> List[Process]:
        """Return a deep copy of the original processes to run a scheduling algorithm on."""
        return deepcopy(self.originalProcesses)

    def _computePerformance(self, finishedProcesses: List[Process]) -> Dict[str, float]:
        """
        Compute average waiting time, turnaround time, response time and throughput.

        Assumes each Process in finishedProcesses has completionTime set.
        """
        numberOfProcesses = len(finishedProcesses)
        if numberOfProcesses == 0:
            return {
                "Average Waiting Time": 0.0,
                "Average Turnaround Time": 0.0,
                "Average Response Time": 0.0,
                "Throughput": 0.0,
            }

        totalWaitingTime = sum(p.waitingTime for p in finishedProcesses)
        totalTurnaroundTime = sum(p.turnaroundTime for p in finishedProcesses)
        # responseTime can be -1 for processes that never started (shouldn't happen); treat as 0 for safety
        totalResponseTime = sum((p.responseTime if p.responseTime >= 0 else 0) for p in finishedProcesses)

        averageWaitingTime = totalWaitingTime / numberOfProcesses
        averageTurnaroundTime = totalTurnaroundTime / numberOfProcesses
        averageResponseTime = totalResponseTime / numberOfProcesses

        totalTime = max((p.completionTime for p in finishedProcesses), default=0)
        throughput = numberOfProcesses / totalTime if totalTime > 0 else 0.0

        return {
            "Average Waiting Time": averageWaitingTime,
            "Average Turnaround Time": averageTurnaroundTime,
            "Average Response Time": averageResponseTime,
            "Throughput": throughput,
        }

    # ---------------- Algorithms ---------------- #

    def firstComeFirstServe(self) -> Dict[str, float]:
        """
        FCFS (non-preemptive).
        """
        processes = self._makeProcessCopy()
        processes.sort(key=lambda p: p.arrivalTime)

        currentTime = 0
        previousProcessId = None
        finishedProcesses: List[Process] = []

        for process in processes:
            # advance time if CPU idle
            if currentTime < process.arrivalTime:
                currentTime = process.arrivalTime
                previousProcessId = None

            # apply context switch if switching from another process
            if previousProcessId is not None and previousProcessId != process.processId:
                currentTime += self.contextSwitchTime

            # set response time if first scheduled
            if process.responseTime == -1:
                process.responseTime = currentTime - process.arrivalTime

            # run to completion
            currentTime += process.burstTime
            process.completionTime = currentTime
            process.turnaroundTime = process.completionTime - process.arrivalTime
            process.waitingTime = process.turnaroundTime - process.originalBurstTime

            finishedProcesses.append(process)
            previousProcessId = process.processId

        return self._computePerformance(finishedProcesses)

    def shortestJobFirst(self) -> Dict[str, float]:
        """
        SJF (non-preemptive), tie-break by arrival time.
        """
        processes = self._makeProcessCopy()
        processes_left = sorted(processes, key=lambda p: p.arrivalTime)

        currentTime = 0
        previousProcessId = None
        finishedProcesses: List[Process] = []

        while processes_left:
            readyProcesses = [p for p in processes_left if p.arrivalTime <= currentTime]
            if not readyProcesses:
                # jump to the next arrival
                currentTime = processes_left[0].arrivalTime
                previousProcessId = None
                continue

            # pick smallest burst; tie by arrival time
            currentProcess = min(readyProcesses, key=lambda p: (p.burstTime, p.arrivalTime))
            processes_left.remove(currentProcess)

            if previousProcessId is not None and previousProcessId != currentProcess.processId:
                currentTime += self.contextSwitchTime

            if currentProcess.responseTime == -1:
                currentProcess.responseTime = currentTime - currentProcess.arrivalTime

            currentTime += currentProcess.burstTime
            currentProcess.completionTime = currentTime
            currentProcess.turnaroundTime = currentProcess.completionTime - currentProcess.arrivalTime
            currentProcess.waitingTime = currentProcess.turnaroundTime - currentProcess.originalBurstTime

            finishedProcesses.append(currentProcess)
            previousProcessId = currentProcess.processId

        return self._computePerformance(finishedProcesses)

    def shortestRemainingTimeFirstFCFS(self) -> Dict[str, float]:
        """
        SRTF preemptive; tie-break by earliest arrival (FCFS).
        """
        processes = self._makeProcessCopy()
        remainingTimeMap = {p.processId: p.burstTime for p in processes}
        processes_left = sorted(processes, key=lambda p: p.arrivalTime)

        currentTime = 0
        previousProcessId = None
        finishedProcesses: List[Process] = []
        completedCount = 0
        totalProcesses = len(processes)

        while completedCount < totalProcesses:
            # gather ready processes
            readyProcesses = [p for p in processes_left if p.arrivalTime <= currentTime and remainingTimeMap[p.processId] > 0]

            if not readyProcesses:
                # idle -> advance time
                if processes_left:
                    currentTime = processes_left[0].arrivalTime
                    previousProcessId = None
                else:
                    break
                continue

            # choose by smallest remaining then earliest arrival
            readyProcesses.sort(key=lambda p: (remainingTimeMap[p.processId], p.arrivalTime))
            currentProcess = readyProcesses[0]
            pid = currentProcess.processId

            # if switching, account for context switch
            if previousProcessId is not None and previousProcessId != pid:
                currentTime += self.contextSwitchTime

            if currentProcess.responseTime == -1:
                currentProcess.responseTime = currentTime - currentProcess.arrivalTime

            # execute one time unit
            remainingTimeMap[pid] -= 1
            currentTime += 1

            if remainingTimeMap[pid] == 0:
                # finished
                currentProcess.completionTime = currentTime
                currentProcess.turnaroundTime = currentProcess.completionTime - currentProcess.arrivalTime
                currentProcess.waitingTime = currentProcess.turnaroundTime - currentProcess.originalBurstTime
                finishedProcesses.append(currentProcess)
                completedCount += 1
                previousProcessId = pid
            else:
                previousProcessId = pid

        return self._computePerformance(finishedProcesses)

    def shortestRemainingTimeFirstPriority(self) -> Dict[str, float]:
        """
        SRTF preemptive; tie-break by higher priority (higher numeric value = higher priority).
        When remaining times are equal, the process with the higher priority is chosen.
        """
        processes = self._makeProcessCopy()
        remainingTimeMap = {p.processId: p.burstTime for p in processes}
        processes_left = sorted(processes, key=lambda p: p.arrivalTime)

        currentTime = 0
        previousProcessId = None
        finishedProcesses: List[Process] = []
        completedCount = 0
        totalProcesses = len(processes)

        while completedCount < totalProcesses:
            readyProcesses = [p for p in processes_left if p.arrivalTime <= currentTime and remainingTimeMap[p.processId] > 0]

            if not readyProcesses:
                if processes_left:
                    currentTime = processes_left[0].arrivalTime
                    previousProcessId = None
                else:
                    break
                continue

            # choose by remaining time then by negative priority (so larger priority wins)
            readyProcesses.sort(key=lambda p: (remainingTimeMap[p.processId], -p.priority, p.arrivalTime))
            currentProcess = readyProcesses[0]
            pid = currentProcess.processId

            if previousProcessId is not None and previousProcessId != pid:
                currentTime += self.contextSwitchTime

            if currentProcess.responseTime == -1:
                currentProcess.responseTime = currentTime - currentProcess.arrivalTime

            remainingTimeMap[pid] -= 1
            currentTime += 1

            if remainingTimeMap[pid] == 0:
                currentProcess.completionTime = currentTime
                currentProcess.turnaroundTime = currentProcess.completionTime - currentProcess.arrivalTime
                currentProcess.waitingTime = currentProcess.turnaroundTime - currentProcess.originalBurstTime
                finishedProcesses.append(currentProcess)
                completedCount += 1
                previousProcessId = pid
            else:
                previousProcessId = pid

        return self._computePerformance(finishedProcesses)

    def priorityNonPreemptive(self) -> Dict[str, float]:
        """
        Non-preemptive priority scheduling (higher numeric value = higher priority).
        Tie-break by arrival time.
        """
        processes = self._makeProcessCopy()
        processes_left = sorted(processes, key=lambda p: p.arrivalTime)

        currentTime = 0
        previousProcessId = None
        finishedProcesses: List[Process] = []

        while processes_left:
            readyProcesses = [p for p in processes_left if p.arrivalTime <= currentTime]
            if not readyProcesses:
                currentTime = processes_left[0].arrivalTime
                previousProcessId = None
                continue

            # choose highest priority (max). tie-break by arrival time
            readyProcesses.sort(key=lambda p: (-p.priority, p.arrivalTime))
            currentProcess = readyProcesses[0]
            processes_left.remove(currentProcess)

            if previousProcessId is not None and previousProcessId != currentProcess.processId:
                currentTime += self.contextSwitchTime

            if currentProcess.responseTime == -1:
                currentProcess.responseTime = currentTime - currentProcess.arrivalTime

            currentTime += currentProcess.burstTime
            currentProcess.completionTime = currentTime
            currentProcess.turnaroundTime = currentProcess.completionTime - currentProcess.arrivalTime
            currentProcess.waitingTime = currentProcess.turnaroundTime - currentProcess.originalBurstTime

            finishedProcesses.append(currentProcess)
            previousProcessId = currentProcess.processId

        return self._computePerformance(finishedProcesses)

    def priorityPreemptive(self) -> Dict[str, float]:
        """
        Preemptive priority scheduling (higher numeric value = higher priority).
        At each time unit, pick the ready process with highest priority; tie-breaker: smaller remaining time then arrival time.
        """
        processes = self._makeProcessCopy()
        remainingTimeMap = {p.processId: p.burstTime for p in processes}
        processes_left = sorted(processes, key=lambda p: p.arrivalTime)

        currentTime = 0
        previousProcessId = None
        finishedProcesses: List[Process] = []
        completedCount = 0
        totalProcesses = len(processes)

        while completedCount < totalProcesses:
            readyProcesses = [p for p in processes_left if p.arrivalTime <= currentTime and remainingTimeMap[p.processId] > 0]

            if not readyProcesses:
                if processes_left:
                    currentTime = processes_left[0].arrivalTime
                    previousProcessId = None
                else:
                    break
                continue

            # choose by priority (max), then remaining time, then arrival
            readyProcesses.sort(key=lambda p: (-p.priority, remainingTimeMap[p.processId], p.arrivalTime))
            currentProcess = readyProcesses[0]
            pid = currentProcess.processId

            if previousProcessId is not None and previousProcessId != pid:
                currentTime += self.contextSwitchTime

            if currentProcess.responseTime == -1:
                currentProcess.responseTime = currentTime - currentProcess.arrivalTime

            # execute one time unit
            remainingTimeMap[pid] -= 1
            currentTime += 1

            if remainingTimeMap[pid] == 0:
                currentProcess.completionTime = currentTime
                currentProcess.turnaroundTime = currentProcess.completionTime - currentProcess.arrivalTime
                currentProcess.waitingTime = currentProcess.turnaroundTime - currentProcess.originalBurstTime
                finishedProcesses.append(currentProcess)
                completedCount += 1
                previousProcessId = pid
            else:
                previousProcessId = pid

        return self._computePerformance(finishedProcesses)

    def roundRobin(self, timeQuantum: int) -> Dict[str, float]:
        """
        Round Robin scheduling. timeQuantum is required.
        Context switch overhead is applied whenever the CPU switches to a different process.
        """
        if timeQuantum <= 0:
            raise ValueError("timeQuantum must be a positive integer")

        processes = self._makeProcessCopy()
        processes.sort(key=lambda p: p.arrivalTime)

        remainingTimeMap = {p.processId: p.burstTime for p in processes}
        arrivalIndex = 0
        readyQueue = deque()
        currentTime = 0
        previousProcessId = None
        finishedProcesses: List[Process] = []
        totalProcesses = len(processes)

        # helper to enqueue arrivals up to currentTime
        def enqueueArrivals():
            nonlocal arrivalIndex
            while arrivalIndex < totalProcesses and processes[arrivalIndex].arrivalTime <= currentTime:
                readyQueue.append(processes[arrivalIndex])
                arrivalIndex += 1

        # start by enqueuing arrivals at time 0
        enqueueArrivals()

        while len(finishedProcesses) < totalProcesses:
            if not readyQueue:
                # idle: fast-forward to next arrival
                if arrivalIndex < totalProcesses:
                    currentTime = processes[arrivalIndex].arrivalTime
                    enqueueArrivals()
                    previousProcessId = None
                else:
                    break
                continue

            currentProcess = readyQueue.popleft()
            pid = currentProcess.processId

            # apply context switch time if switching between different processes
            if previousProcessId is not None and previousProcessId != pid:
                currentTime += self.contextSwitchTime

            # set response time if first time running
            if currentProcess.responseTime == -1:
                currentProcess.responseTime = currentTime - currentProcess.arrivalTime

            # execute for a quantum or remaining time
            executionTime = min(timeQuantum, remainingTimeMap[pid])
            remainingTimeMap[pid] -= executionTime
            currentTime += executionTime

            # enqueue arrivals that came during the execution window
            enqueueArrivals()

            if remainingTimeMap[pid] == 0:
                # finished
                currentProcess.completionTime = currentTime
                currentProcess.turnaroundTime = currentProcess.completionTime - currentProcess.arrivalTime
                currentProcess.waitingTime = currentProcess.turnaroundTime - currentProcess.originalBurstTime
                finishedProcesses.append(currentProcess)
                previousProcessId = pid
            else:
                # requeue for next round
                readyQueue.append(currentProcess)
                previousProcessId = pid

        return self._computePerformance(finishedProcesses)
