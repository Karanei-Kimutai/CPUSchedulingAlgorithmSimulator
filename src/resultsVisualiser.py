"""
Results visualizer: creates and saves bar charts that compare algorithms for each metric.

Saves PNG files to outputs/graphs/
"""

import os
import matplotlib.pyplot as plt
from typing import Dict
from utils import ensureDirectoryExists


def saveMetricGraphs(resultsByAlgorithm: Dict[str, Dict[str, float]], outputDirectory: str = "outputs/graphs") -> None:
    """
    Given resultsByAlgorithm (mapping algorithmName -> {metricName: value}),
    create a bar chart for each metric and save to outputDirectory.

    Args:
        resultsByAlgorithm: dict mapping algorithm names to metric dicts
        outputDirectory: path where graphs should be saved
    """
    outputDirectory = ensureDirectoryExists(outputDirectory)

    # Derive metric names from first algorithm's metric dict
    firstAlgorithmMetrics = next(iter(resultsByAlgorithm.values()))
    metricNames = list(firstAlgorithmMetrics.keys())

    for metricName in metricNames:
        algorithmNames = list(resultsByAlgorithm.keys())
        metricValues = [resultsByAlgorithm[algorithmName][metricName] for algorithmName in algorithmNames]

        plt.figure(figsize=(8, 5))
        bars = plt.bar(algorithmNames, metricValues, edgecolor="black")
        plt.title(f"{metricName} — Comparison")
        plt.ylabel(metricName)
        plt.xlabel("Scheduling Algorithm")
        plt.xticks(rotation=25, ha="right")
        plt.tight_layout()

        # annotate bars with values
        for bar in bars:
            height = bar.get_height()
            plt.annotate(f"{height:.4f}", xy=(bar.get_x() + bar.get_width()/2, height), xytext=(0, 3), textcoords="offset points", ha="center", va="bottom", fontsize=8)

        fileName = f"{metricName.replace(' ', '_').lower()}.png"
        filePath = os.path.join(outputDirectory, fileName)
        plt.savefig(filePath)
        plt.close()
        print(f"Saved graph: {filePath}")
