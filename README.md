# MSCS 532 Assignment 5 – Quicksort Algorithm: Implementation, Analysis, and Randomization

This project contains my implementation and analysis for Assignment 5 in MSCS 532 – Algorithms and Data Structures.

## Files

- `assignment5.py` – Deterministic and randomized Quicksort, correctness tests, and performance benchmarks.
- `Hanusha_Assignment_5.docx` – Written report containing design choices, complexity analysis, and empirical results.
- `README.md` – Project information and instructions.

## How to Run

1. Make sure Python 3 is installed.
2. Download or clone this repository.
3. Open a terminal in the project folder.
4. Run:

```bash
python assignment5.py
```

No additional libraries are required.

## What the Program Does

The program demonstrates both sorting algorithms, performs 620 correctness tests, and compares performance across five input sizes (100, 500, 1000, 2000, and 4000) and four input distributions: random, sorted, reverse-sorted, and repeated elements.

Execution times are measured using the median of five runs. The program also reports comparison counts and maximum recursion depth.

## Summary of Findings

- Both algorithms performed efficiently on random inputs.
- Deterministic Quicksort showed O(n²) behavior on sorted and reverse-sorted inputs.
- Randomized Quicksort performed substantially better on sorted and reverse-sorted inputs.
- Both algorithms slowed down with many repeated values because of the two-way Lomuto partitioning scheme.

The detailed analysis and experimental results are included in the Word report.
