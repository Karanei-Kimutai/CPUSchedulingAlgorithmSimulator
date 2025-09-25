CPU Scheduling Algorithm Simulator
==================================

Overview
--------

The **CPU Scheduling Algorithm Simulator** is a Python-based application designed to simulate and compare multiple CPU scheduling algorithms.It provides both an **educational tool** for students learning operating systems and a **practical analysis tool** for experimenting with scheduling strategies.

The simulator allows users to:

*   Input or generate a large number of processes (e.g., 1000).
    
*   Configure scheduling algorithms with context switching overhead.
    
*   View performance metrics numerically and compare them visually through graphs.
    

Features
--------

*   Implementation of **seven CPU scheduling algorithms**:
    
    *   First-Come-First-Serve (FCFS)
        
    *   Shortest Job First (SJF)
        
    *   Shortest Remaining Time First (SRTF) with FCFS tie-breaking
        
    *   Shortest Remaining Time First (SRTF) with Priority tie-breaking
        
    *   Priority Scheduling (Non-Preemptive)
        
    *   Priority Scheduling (Preemptive)
        
    *   Round Robin (configurable quantum)
        
*   **Performance metrics calculated for each algorithm**:
    
    *   Average Waiting Time
        
    *   Average Turnaround Time
        
    *   Average Response Time
        
    *   Throughput
        
*   **Interactive command-line interface (CLI)** with safe user input:
    
    *   Users can choose **arrival time distribution** (uniform, exponential, normal).
        
    *   Users can choose **burst time distribution** (short jobs, mixed, long jobs).
        
    *   Users can enter a **constant context switch time**.
        
*   **Automated process dataset generation** for large simulations.
    
*   **Graphical output**:
    
    *   Each metric is plotted separately (Waiting, Turnaround, Response, Throughput).
        
    *   Graphs are saved in an outputs/ directory inside the project.
        
*   **Unit tests** verifying correctness of all algorithms.
    

Scheduling Algorithms Explained
-------------------------------

### First-Come-First-Serve (FCFS)

Non-preemptive. Processes are executed in order of arrival. Simple, but long jobs delay shorter ones (convoy effect).

### Shortest Job First (SJF)

Non-preemptive. Picks the process with the smallest burst time. Minimizes waiting time but requires knowledge of job lengths.

### Shortest Remaining Time First (SRTF) with FCFS Tie-Break

Preemptive. Always executes the process with the smallest remaining burst. Ties are resolved by earliest arrival.

### Shortest Remaining Time First (SRTF) with Priority Tie-Break

Preemptive. Same as above, but ties are broken by priority (higher number = higher priority).

### Priority Scheduling (Non-Preemptive)

Executes the process with the highest priority among the available ones. Ties can be resolved with arrival order.

### Priority Scheduling (Preemptive)

Preemptive. A new higher-priority process can interrupt the currently running process.

### Round Robin

Preemptive. Each process gets CPU for a fixed time quantum, then goes to the back of the ready queue. Fair and widely used in time-sharing systems.

Implementation Details
----------------------

### Process Class (process.py)

Represents a process with attributes:

*   processId (unique identifier)
    
*   arrivalTime
    
*   burstTime
    
*   priority
    
*   Metrics: completionTime, turnaroundTime, waitingTime, responseTime
    
*   originalBurstTime for resetting in preemptive scheduling
    

### Scheduler Class (scheduler.py)

Implements all algorithms and metrics calculation.Key methods include:

*   resetProcesses() – resets process state before each run
    
*   calculatePerformance() – computes average metrics and throughput
    
*   Algorithm methods (firstComeFirstServe, shortestJobFirst, etc.)
    
*   roundRobin(quantum) – accepts a time quantum
    
*   Algorithms account for **contextSwitchTime** when processes switch
    

### Data Generation (dataGenerator.py)

Automatically generates processes:

*   User chooses **arrival time distribution** (uniform, normal, exponential).
    
*   User chooses **burst time distribution** (short, mixed, long).
    
*   User specifies **number of processes** (e.g., 1000).
    
*   Generated processes are exported to an Excel/CSV file in outputs/.
    

### Graphing (graphGenerator.py)

*   Generates **comparison graphs** for each metric across algorithms.
    
*   Saves results in outputs/graphs/.
    

### Utility Functions (utils.py)

*   safeInput(prompt) – ensures valid non-negative integer input
    
*   safeFloatInput(prompt) – ensures valid float input (for switch times)
    
*   safeChoiceInput(prompt, choices) – ensures valid menu selections
    

### Main Program (main.py)

The interactive entry point:

1.  Asks user for number of processes.
    
2.  Lets user choose between **manual input** or **automatic dataset generation**.
    
3.  Prompts for arrival/burst distribution (if generating).
    
4.  Prompts for context switch time.
    
5.  Runs all scheduling algorithms on the dataset.
    
6.  Displays performance results in the CLI.
    
7.  Saves comparison graphs in the outputs/ folder.
    

### Testing (testSimulator.py)

Unit tests covering all algorithms with a fixed dataset of 4 processes to validate correctness.

How to Run the Simulator
------------------------

1.  Ensure you have **Python 3.x** installed.
    
2.  pip install -r requirements.txt
    
3.  python src/main.py
    
4.  Follow the prompts to configure the simulation and view results.
    

Running Tests
-------------

To verify algorithms

python src/testSimulator.py   `

Output
------

*   Numerical results are displayed in the terminal.
    
*   Graphs are saved in outputs/graphs/.
    
*   Example graph: comparison of Average Waiting Time across algorithms.
    

Educational Value
-----------------

This simulator demonstrates:

*   The trade-offs between scheduling algorithms.
    
*   The effect of **preemptive vs non-preemptive** scheduling.
    
*   How **process characteristics** affect scheduling outcomes.
    
*   The impact of **context switching overhead**.
    
*   How large datasets (e.g., 1000 processes) behave compared to small sets.
    

Limitations & Future Work
-------------------------

*   Assumes CPU-bound processes only (no I/O).
    
*   Uses synthetic distributions; real-world traces would provide deeper insights.
    
*   Gantt chart visualization not yet included.
    

Planned enhancements:

*   Add multi-level feedback queues.
    
*   Add Gantt chart visualization.
    
*   Support I/O burst modeling.
    
*   Extend dataset import/export capabilities.
    

Contributing
------------

We welcome contributions:

*   Ensure code follows naming conventions (camelCase, descriptive).
    
*   Add/update unit tests for new features.
    
*   Document changes clearly in README.
    

License
-------

This project is open source under the MIT License.