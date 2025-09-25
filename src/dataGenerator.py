"""
DataGenerator: create synthetic process datasets and save them to an Excel file.

Generates:
 - Process ID
 - Arrival Time
 - Burst Time
 - Priority

Saves output to: src/outputs/process_data.xlsx
"""

import random
import pandas as pd
import os
from typing import List
from process import Process
from utils import ensureDirectoryExists


class DataGenerator:
    """
    Create and persist synthetic process datasets according to user-selected patterns.
    """

    def __init__(self, outputDirectory: str = "src/outputs"):
        self.outputDirectory = outputDirectory
        ensureDirectoryExists(self.outputDirectory)

    def generateProcesses(
        self,
        numberOfProcesses: int,
        arrivalPattern: str = "sequential",
        burstPattern: str = "random",
        priorityPattern: str = "random"
    ) -> List[Process]:
        """
        Generate a list of Process objects and save the dataset to Excel.

        Args:
            numberOfProcesses: number of processes to generate (int)
            arrivalPattern: 'sequential', 'random', or 'bursty'
            burstPattern: 'fixed', 'random', or 'heavy'
            priorityPattern: 'uniform', 'random', or 'skewed'

        Returns:
            List[Process]: generated Process objects (also saved to file)
        """
        # deterministic seed for reproducibility during experiments
        random.seed(42)

        # --- Arrival times ---
        if arrivalPattern == "sequential":
            arrivalTimes = [i for i in range(numberOfProcesses)]
        elif arrivalPattern == "random":
            maxArrival = max(1, numberOfProcesses // 2)
            arrivalTimes = [random.randint(0, maxArrival) for _ in range(numberOfProcesses)]
            arrivalTimes.sort()
        elif arrivalPattern == "bursty":
            # create clusters to simulate bursts
            clusterSize = max(1, numberOfProcesses // 10)
            arrivalTimes = []
            for i in range(numberOfProcesses):
                clusterBase = (i // clusterSize) * clusterSize
                arrivalTimes.append(clusterBase + random.randint(0, max(0, clusterSize // 2)))
        else:
            raise ValueError("Unknown arrivalPattern")

        # --- Burst times ---
        if burstPattern == "fixed":
            burstTimes = [5 for _ in range(numberOfProcesses)]
        elif burstPattern == "random":
            burstTimes = [random.randint(1, 15) for _ in range(numberOfProcesses)]
        elif burstPattern == "heavy":
            # heavy-tailed distribution: many small, some large
            burstTimes = [max(1, int(random.expovariate(1/5))) for _ in range(numberOfProcesses)]
        else:
            raise ValueError("Unknown burstPattern")

        # --- Priorities ---
        if priorityPattern == "uniform":
            priorities = [5 for _ in range(numberOfProcesses)]
        elif priorityPattern == "random":
            priorities = [random.randint(1, 10) for _ in range(numberOfProcesses)]
        elif priorityPattern == "skewed":
            # skewed: many low numbers (high priority), some high numbers
            choices = [1, 2, 3, 8, 9, 10]
            weights = [0.2, 0.2, 0.2, 0.15, 0.15, 0.1]
            priorities = [random.choices(choices, weights)[0] for _ in range(numberOfProcesses)]
        else:
            raise ValueError("Unknown priorityPattern")

        processList: List[Process] = []
        for index in range(numberOfProcesses):
            processId = f"P{index+1}"
            arrivalTime = int(arrivalTimes[index])
            burstTime = int(burstTimes[index])
            priorityValue = int(priorities[index])
            processObject = Process(processId, arrivalTime, burstTime, priorityValue)
            processList.append(processObject)

        # --- Save to Excel ---
        rows = [{
            "Process ID": process.processId,
            "Arrival Time": process.arrivalTime,
            "Burst Time": process.originalBurstTime,
            "Priority": process.priority
        } for process in processList]

        dataframe = pd.DataFrame(rows)
        outputFilePath = os.path.join(self.outputDirectory, "process_data.xlsx")
        dataframe.to_excel(outputFilePath, index=False)
        print(f"Saved generated process data to: {outputFilePath}")

        return processList
