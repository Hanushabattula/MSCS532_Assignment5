
"""
MSCS 532 - Assignment 5
Quicksort Algorithm: Implementation, Analysis, and Randomization

This program includes:
1. Deterministic Quicksort using the last element as pivot
2. Randomized Quicksort using a randomly selected pivot
3. Correctness tests for both algorithms
4. Runtime, comparison-count, and recursion-depth benchmarks
5. Experiments with random, sorted, reverse-sorted, and repeated data

Run:
    python assignment5.py
"""

import random
import statistics
import sys
import time


# ------------------------------------------------------------
# Experiment configuration
# ------------------------------------------------------------

SEED = 532
INPUT_SIZES = [100, 500, 1000, 2000, 4000]
REPEATS = 5

# Worst-case Quicksort recursion can reach O(n) levels.
# Increase the limit to accommodate the planned experiments.
sys.setrecursionlimit(10000)


# ------------------------------------------------------------
# Partition function
# ------------------------------------------------------------

def partition(arr, low, high):
    """
    Partition the subarray using Lomuto partitioning.

    The last element is selected as the pivot.
    Values <= pivot move to its left.
    Values > pivot remain to its right.

    Returns the pivot's final sorted index.
    """

    pivot = arr[high]
    i = low - 1

    # Examine each element before the pivot.
    for j in range(low, high):

        if arr[j] <= pivot:
            i += 1

            # Move the smaller value into the left region.
            arr[i], arr[j] = arr[j], arr[i]

    # Place the pivot between the two regions.
    arr[i + 1], arr[high] = arr[high], arr[i + 1]

    return i + 1


# ------------------------------------------------------------
# Shared statistics helper
# ------------------------------------------------------------

def update_statistics(stats, comparisons, depth):
    """Record comparisons and maximum active partition depth."""

    if stats is not None:
        stats["comparisons"] += comparisons
        stats["max_depth"] = max(stats["max_depth"], depth)


# ------------------------------------------------------------
# Deterministic Quicksort
# ------------------------------------------------------------

def deterministic_quicksort(
    arr, low=0, high=None, stats=None, depth=1
):
    """
    Sort an array in place using deterministic Quicksort.

    The last element of each subarray is selected as pivot.

    Best case: O(n log n)
    Average case: O(n log n)
    Worst case: O(n^2)
    """

    if high is None:
        high = len(arr) - 1

    if low < high:

        # A partition of m elements performs m - 1 comparisons.
        update_statistics(stats, high - low, depth)

        pivot_index = partition(arr, low, high)

        # Recursively sort the left partition.
        deterministic_quicksort(
            arr, low, pivot_index - 1, stats, depth + 1
        )

        # Recursively sort the right partition.
        deterministic_quicksort(
            arr, pivot_index + 1, high, stats, depth + 1
        )


# ------------------------------------------------------------
# Randomized Quicksort
# ------------------------------------------------------------

def randomized_quicksort(
    arr, low=0, high=None, stats=None, depth=1, rng=None
):
    """
    Sort an array in place using randomized Quicksort.

    A pivot is selected uniformly at random from the
    current subarray and moved to the last position.

    Expected time: O(n log n)
    Worst-case time: O(n^2)
    """

    if high is None:
        high = len(arr) - 1

    if rng is None:
        rng = random

    if low < high:

        update_statistics(stats, high - low, depth)

        # Select a random pivot from the current subarray.
        random_index = rng.randint(low, high)

        # Move the selected pivot to the last position.
        arr[random_index], arr[high] = (
            arr[high], arr[random_index]
        )

        pivot_index = partition(arr, low, high)

        # Recursively sort the left partition.
        randomized_quicksort(
            arr, low, pivot_index - 1,
            stats, depth + 1, rng
        )

        # Recursively sort the right partition.
        randomized_quicksort(
            arr, pivot_index + 1, high,
            stats, depth + 1, rng
        )


# ------------------------------------------------------------
# Correctness tests
# ------------------------------------------------------------

def run_correctness_tests():
    """Verify both algorithms against Python's sorted()."""

    fixed_cases = [
        [],                         # Empty array
        [7],                        # Single element
        [2, 1],                     # Two elements
        [5, 5, 5, 5, 5],            # All equal
        [1, 2, 3, 4, 5, 6],         # Already sorted
        [6, 5, 4, 3, 2, 1],         # Reverse sorted
        [8, 3, 5, 1, 9, 3, 7],      # Duplicates
        [-4, 10, 0, -4, 3],         # Negative values
        [0, 0, 0],                  # Zeros
        [100, -100, 50, -50, 0]     # Mixed values
    ]

    rng = random.Random(SEED)

    # Generate 300 additional random test arrays.
    random_cases = [
        [
            rng.randint(-50, 50)
            for _ in range(rng.randint(0, 60))
        ]
        for _ in range(300)
    ]

    algorithms = [
        deterministic_quicksort,
        randomized_quicksort
    ]

    total_tests = 0

    for algorithm in algorithms:

        for case in fixed_cases + random_cases:

            test_data = case.copy()

            algorithm(test_data)

            # Compare the result against Python's sorted().
            assert test_data == sorted(case), (
                f"{algorithm.__name__} failed: {case}"
            )

            total_tests += 1

    print(f"All {total_tests} correctness tests passed.")
    print(
        "Tested empty arrays, duplicates, negative numbers,"
    )
    print(
        "sorted data, reverse-sorted data, and random arrays."
    )


# ------------------------------------------------------------
# Dataset generation
# ------------------------------------------------------------

def make_datasets(n, rng):
    """Create four input distributions for each input size."""

    return {
        "Random": [
            rng.randint(1, 10 * n)
            for _ in range(n)
        ],

        "Sorted": list(range(n)),

        "Reverse Sorted": list(range(n, 0, -1)),

        "Repeated Elements": [
            rng.randint(1, 10)
            for _ in range(n)
        ]
    }


# ------------------------------------------------------------
# Runtime measurement
# ------------------------------------------------------------

def median_time(
    sort_function, data, repeats=REPEATS, seed=SEED
):
    """
    Measure median execution time over repeated runs.

    Every run sorts a fresh copy of the same input.
    Randomized Quicksort uses seeded random generators
    to make the experiment reproducible.
    """

    times = []
    expected = sorted(data)

    for run in range(repeats):

        test_data = data.copy()

        start = time.perf_counter()

        if sort_function is randomized_quicksort:

            rng = random.Random(seed + run)

            sort_function(test_data, rng=rng)

        else:
            sort_function(test_data)

        elapsed = time.perf_counter() - start

        # Verify that the benchmark result is correct.
        assert test_data == expected, (
            f"Incorrect result from {sort_function.__name__}"
        )

        times.append(elapsed)

    return statistics.median(times)


# ------------------------------------------------------------
# Comparison and recursion-depth measurement
# ------------------------------------------------------------

def measure_stats(sort_function, data, seed=SEED):
    """
    Record pivot comparisons and active partition depth.

    Maximum depth counts partitioning levels rather than
    empty or single-element base-case calls.
    """

    stats = {
        "comparisons": 0,
        "max_depth": 0
    }

    test_data = data.copy()

    if sort_function is randomized_quicksort:

        rng = random.Random(seed)

        sort_function(
            test_data,
            stats=stats,
            rng=rng
        )

    else:

        sort_function(
            test_data,
            stats=stats
        )

    assert test_data == sorted(data)

    return stats["comparisons"], stats["max_depth"]


# ------------------------------------------------------------
# Benchmark experiments
# ------------------------------------------------------------

def run_benchmark():
    """Compare both Quicksort implementations."""

    dataset_rng = random.Random(SEED)

    print("\nRUNNING TIME COMPARISON")
    print("Median execution time over five runs (seconds)")
    print("-" * 65)

    print(
        f"{'Size':>6}  "
        f"{'Distribution':<18}"
        f"{'Randomized':>13}"
        f"{'Deterministic':>17}"
    )

    results = []

    for n in INPUT_SIZES:

        datasets = make_datasets(n, dataset_rng)

        for name, data in datasets.items():

            randomized_time = median_time(
                randomized_quicksort, data
            )

            deterministic_time = median_time(
                deterministic_quicksort, data
            )

            randomized_comparisons, randomized_depth = (
                measure_stats(randomized_quicksort, data)
            )

            deterministic_comparisons, deterministic_depth = (
                measure_stats(deterministic_quicksort, data)
            )

            results.append({
                "size": n,
                "distribution": name,
                "randomized_time": randomized_time,
                "deterministic_time": deterministic_time,
                "randomized_comparisons": randomized_comparisons,
                "randomized_depth": randomized_depth,
                "deterministic_comparisons": deterministic_comparisons,
                "deterministic_depth": deterministic_depth
            })

            print(
                f"{n:>6}  "
                f"{name:<18}"
                f"{randomized_time:>13.6f}"
                f"{deterministic_time:>17.6f}"
            )

    print("\nCOMPARISONS AND RECURSION DEPTH")
    print("-" * 85)

    print(
        f"{'Size':>6}  "
        f"{'Distribution':<18}"
        f"{'Rand Cmp':>12}"
        f"{'Rand Depth':>12}"
        f"{'Det Cmp':>12}"
        f"{'Det Depth':>12}"
    )

    for row in results:

        print(
            f"{row['size']:>6}  "
            f"{row['distribution']:<18}"
            f"{row['randomized_comparisons']:>12}"
            f"{row['randomized_depth']:>12}"
            f"{row['deterministic_comparisons']:>12}"
            f"{row['deterministic_depth']:>12}"
        )

    return results


# ------------------------------------------------------------
# Main program
# ------------------------------------------------------------

if __name__ == "__main__":

    original = [8, 3, 5, 1, 9, 3, 7]

    print("MSCS 532 - ASSIGNMENT 5")
    print("Quicksort Implementation and Performance Analysis")
    print("=" * 60)

    print("\nDEMONSTRATION")

    print("Original Array:       ", original)

    deterministic_data = original.copy()

    deterministic_quicksort(deterministic_data)

    print("Deterministic Result: ", deterministic_data)

    randomized_data = original.copy()

    randomized_quicksort(
        randomized_data,
        rng=random.Random(SEED)
    )

    print("Randomized Result:    ", randomized_data)

    print("\nCORRECTNESS TESTS")

    run_correctness_tests()

    run_benchmark()

    print("\nAll experiments completed successfully.")
