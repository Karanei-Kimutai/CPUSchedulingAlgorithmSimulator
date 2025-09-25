"""
Interactive main program for the CPU Scheduling Simulator.

This script:
 - prompts the user for generation options (arrival/burst/priority patterns),
 - prompts for context switch time and Round Robin quantum,
 - generates a dataset (saved to src/outputs/process_data.xlsx),
 - runs all scheduling algorithms in scheduler.py,
 - prints numeric results, and saves comparison graphs to src/outputs/graphs.
"""

from utils import safeInput, ensureDirectoryExists
from dataGenerator import DataGenerator
from scheduler import Scheduler
import os
from resultsVisualiser import saveMetricGraphs


def main():
    print("CPU Scheduling Simulator\n")
    print("This simulator simulates the following scheduling algorithms: FCFS, SJF, SRTF(FCFS tie-break), SRTF(Priority tie-break), Priority Scheduling and Round Robin")

    numberOfProcesses = safeInput("Enter number of processes (e.g., 100): ", int)

    print("\nArrival time pattern options:")
    print(" Sequential - process i arrives at time i (controlled load)")
    print("  Random     - arrival times randomly scattered")
    print("  Bursty     - arrivals clustered into bursts")
    arrivalPattern = safeInput("Choose arrival pattern (sequential/random/bursty): ", str, ["sequential", "random", "bursty"])

    print("\nBurst time pattern options:")
    print("  fixed  - every process has same burst time (fairness tests)")
    print("  random - burst times are uniform random")
    print("  heavy  - heavy-tailed distribution (many short jobs, few long)")
    burstPattern = safeInput("Choose burst pattern (fixed/random/heavy): ", str, ["fixed", "random", "heavy"])

    print("\nPriority pattern options:")
    print("  uniform - all processes share same priority (baseline)")
    print("  random  - priorities uniformly random")
    print("  skewed  - most processes get high priority, a few low")
    priorityPattern = safeInput("Choose priority pattern (uniform/random/skewed): ", str, ["uniform", "random", "skewed"])

    contextSwitchTime = safeInput("\nEnter context switch time (non-negative integer, e.g., 0 or 1): ", int)
    roundRobinQuantum = safeInput("Enter Round Robin time quantum (e.g., 2 or 4): ", int)

    # Ensure outputs directories exist
    outputDirectory = "outputs"
    graphsDirectory = os.path.join(outputDirectory, "graphs")
    ensureDirectoryExists(outputDirectory)
    ensureDirectoryExists(graphsDirectory)

    # Data generation
    dataGenerator = DataGenerator(outputDirectory)
    processList = dataGenerator.generateProcesses(
        numberOfProcesses,
        arrivalPattern=arrivalPattern,
        burstPattern=burstPattern,
        priorityPattern=priorityPattern
    )

    # Run scheduler algorithms
    scheduler = Scheduler(processList, contextSwitchTime=contextSwitchTime)

    print("\nRunning scheduling algorithms — this may take a moment for large N...\n")

    resultsByAlgorithm = {}
    resultsByAlgorithm["FCFS"] = scheduler.firstComeFirstServe()
    resultsByAlgorithm["SJF"] = scheduler.shortestJobFirst()
    resultsByAlgorithm["SRTF (FCFS tie-break)"] = scheduler.shortestRemainingTimeFirstFCFS()
    resultsByAlgorithm["SRTF (Priority tie-break)"] = scheduler.shortestRemainingTimeFirstPriority()
    resultsByAlgorithm["Priority (Non-preemptive)"] = scheduler.priorityNonPreemptive()
    resultsByAlgorithm["Priority (Preemptive)"] = scheduler.priorityPreemptive()
    resultsByAlgorithm[f"Round Robin (q={roundRobinQuantum})"] = scheduler.roundRobin(roundRobinQuantum)

    # Print numeric results
    print("=== Numerical Results ===")
    for algorithmName, metricDict in resultsByAlgorithm.items():
        print(f"\n--- {algorithmName} ---")
        for metricName, metricValue in metricDict.items():
            print(f"{metricName}: {metricValue:.4f}")

    # Save graphs
    print("\nGenerating graphs...")
    saveMetricGraphs(resultsByAlgorithm, graphsDirectory)

    print(f"\nAll done. Process dataset and graphs saved under: {outputDirectory}")


if __name__ == "__main__":
    main()
