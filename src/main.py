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
        processes.append(Process(f"P{i+1}",arrivalTime,burstTime))

    scheduler=Scheduler(processes)
    while True:
        print("\nChoose a scheduling algorithm to run: ")
        print("1. First Come First Serve (FCFS)")
        print("2. Shortest Job First (SJF)")
        print("3. Shortest Remaining Time First (FCFS tie-break)")
        print("4. Shortest Remaining Time First (Priority tie-break")
        print("5. Exit")

        choice=safeInput("Enter your choice: ")
        if choice==1:
            results=scheduler.firstComeFirstServe()
            print("\nFirst Come First Serve Results:")
        elif choice==2:
            results=scheduler.shortestJobFirst()
            print("\nShortest Job First Results:")
        elif choice==3:
            results=scheduler.shortestRemainingTimeFirstFCFS()
            print("\nSRTF (FCFS tie-break) results")
        elif choice==4:
            results=scheduler.shortestRemainingTimeFirstPriority()
            print("\nSRTF (Priority tie-break) results")
        elif choice==5:
            print("Exiting program.")
            break
        else:
            print("Invalid choice. Please try again.")
            continue

        for metric,value in results.items():
            print(f"{metric}: {value:.2f}")

        continueChoice=input("\nWould you like to run another algorithm? (yes/no): ").strip().lower()
        if continueChoice !="yes":
            print("Exiting program.")
            break


