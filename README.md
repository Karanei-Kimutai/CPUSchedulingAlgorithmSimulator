# CPU Scheduling Algorithm Simulator
# CPU Scheduler Simulator

## Overview

The CPU Scheduler Simulator is a Python-based application that demonstrates various CPU scheduling algorithms used in operating systems. This educational tool allows users to input processes with different characteristics and observe how different scheduling algorithms handle process execution, providing insights into their performance metrics.

## Features

- Implementation of four CPU scheduling algorithms:
  - First-Come-First-Serve (FCFS)
  - Shortest Job First (SJF)
  - Shortest Remaining Time First with FCFS tie-breaking
  - Shortest Remaining Time First with Priority tie-breaking
- Interactive command-line interface for process input and algorithm selection
- Comprehensive performance metrics calculation:
  - Average Waiting Time
  - Average Turnaround Time
  - Average Response Time
  - Throughput
- Unit testing suite to verify algorithm correctness

## Scheduling Algorithms Explained

### First-Come-First-Serve (FCFS)
A non-preemptive algorithm that executes processes in the order of their arrival. The first process to arrive is the first to be served. While simple to implement, it can lead to long waiting times for processes that arrive just after a long process.

### Shortest Job First (SJF)
A non-preemptive algorithm that selects the process with the smallest burst time from the available processes. This algorithm minimizes average waiting time but requires knowing the burst times in advance, which is often not practical in real systems.

### Shortest Remaining Time First (SRTF) with FCFS Tie-Breaking
A preemptive version of SJF where the scheduler always chooses the process with the shortest remaining execution time. If multiple processes have the same remaining time, the one that arrived first is selected. This algorithm can context-switch frequently but provides optimal average waiting time.

### Shortest Remaining Time First (SRTF) with Priority Tie-Breaking
Similar to the FCFS version but uses process priority to break ties when remaining times are equal. Higher priority values indicate higher priority. This approach allows for more control over process execution order.

## Code Implementation Details

### Process Class (`process.py`)
The `Process` class represents a single process with the following attributes:
- `processId`: Unique identifier for the process
- `arrivalTime`: Time when the process arrives in the system
- `burstTime`: CPU time required by the process
- `priority`: Priority level (higher number = higher priority)
- Computed metrics: completionTime, turnaroundTime, waitingTime, responseTime
- `originalBurstTime`: Stores the initial burst time for reset purposes

### Scheduler Class (`scheduler.py`)
The main class that implements all scheduling algorithms. Key methods include:

1. `resetProcesses()`: Resets all process states before running an algorithm
2. `calculatePerformance()`: Computes average metrics and throughput
3. `firstComeFirstServe()`: Implements FCFS scheduling
4. `shortestJobFirst()`: Implements SJF scheduling
5. `shortestRemainingTimeFirstFCFS()`: Implements SRTF with FCFS tie-breaking
6. `shortestRemainingTimeFirstPriority()`: Implements SRTF with priority tie-breaking

### Utility Functions (`utils.py`)
Contains helper functions for safe input handling:
- `safeInput()`: Ensures non-negative integer input
- `safePriorityInput()`: Ensures valid positive integer priority input

### Main Program (`main.py`)
The entry point of the application that:
1. Collects process information from the user
2. Presents a menu of scheduling algorithms
3. Executes the selected algorithm
4. Displays performance results
5. Allows running multiple algorithms in sequence

### Testing (`test_simulator.py`)
Comprehensive unit tests that verify the correctness of each scheduling algorithm using a fixed set of processes with known expected results.

## How to Run the Simulator

1. Ensure you have Python 3.x installed on your system
2. Clone or download the project files
3. Navigate to the project directory in your terminal/command prompt
4. Run the main program:
   ```
   python main.py
   ```
5. Follow the prompts to enter the number of processes and their details
6. Select a scheduling algorithm from the menu
7. View the results and choose to run another algorithm or exit

## Running Tests

To execute the unit tests and verify the algorithms:
```
python test_simulator.py
```

## Example Usage

1. Start the program and enter the number of processes (e.g., 3)
2. For each process, provide:
   - Arrival time (e.g., 0, 1, 2)
   - Burst time (e.g., 8, 4, 5)
   - Priority (for algorithms that use it)
3. Select an algorithm from the menu (e.g., 2 for SJF)
4. View the performance metrics:
   - Average Waiting Time
   - Average Turnaround Time
   - Average Response Time
   - Throughput
5. Choose to run another algorithm or exit

## Performance Metrics Explained

- **Waiting Time**: Total time a process spends waiting in the ready queue
- **Turnaround Time**: Total time from process arrival to completion (waiting + execution)
- **Response Time**: Time from process arrival to first response (first time it gets CPU)
- **Throughput**: Number of processes completed per unit time

## Educational Value

This simulator helps students and developers understand:
- The differences between various CPU scheduling algorithms
- How preemptive and non-preemptive scheduling differ
- The trade-offs between different scheduling strategies
- How to calculate and interpret performance metrics
- The importance of process characteristics (arrival time, burst time, priority) on scheduling outcomes

## Limitations and Future Enhancements

- Currently supports only a limited set of scheduling algorithms
- Does not visualize the scheduling process (Gantt charts)
- No support for I/O operations or process blocking
- Potential enhancements could include:
  - Additional scheduling algorithms (Round Robin, Priority Scheduling)
  - Graphical visualization of scheduling timelines
  - Support for I/O-bound processes
  - Comparative analysis of multiple algorithms

## Contributing

Contributions to improve the simulator are welcome. Please ensure:
- Code follows the existing style and conventions
- New features include appropriate unit tests
- Documentation is updated to reflect changes

## License

This project is open source and available under the MIT License.
