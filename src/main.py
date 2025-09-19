from process import Process
from scheduler import Scheduler
from utils import safeInput
if __name__=="__main__":
    numberOfProcesses=safeInput("Enter number of processes:")
    processes=[]

    for i in range (numberOfProcesses):
        print(f"\nEnter details for process {i+1}")
        arrivalTime=safeInput("Enter arrival time: ")
        burstTime=safeInput("Enter burst time: ")
        priority=safeInput("Enter priority (higher number= higher priority) :")
        processes.append(Process(f"P{i+1}",arrivalTime,burstTime,priority))

    scheduler=Scheduler(processes)
    print("\n FCFS")
    print(scheduler.firstComeFirstServe())

    print("\n SJF")
    print(scheduler.shortestJobFirst())

    print("\n SRTF (FCFS as tie-break)")
    print(scheduler.shortestRemainingTimeFirstFCFS())

    print("\n SRTF (Priority as tie-break")
    print(scheduler.shortestRemainingTimeFirstPriority())