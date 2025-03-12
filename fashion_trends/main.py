#!/usr/bin/env python
# main.py
import sys
import os
from fashion_trends.crew import FashionTrendsCrew


def run():
    """
    Run the fashion trends crew to generate a report.
    """
    # You can add any inputs here if needed
    inputs = {}

    # Ensure output directory exists
    os.makedirs('output', exist_ok=True)

    # Run the crew
    result = FashionTrendsCrew().crew().kickoff(inputs=inputs)

    print("\n\n====== FASHION TRENDS REPORT GENERATED ======")
    print("Check the output/fashion_trends_2025.md file for the report")

    return 0


if __name__ == "__main__":
    sys.exit(run())