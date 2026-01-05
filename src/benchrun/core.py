"""Core benchmarking functionality.

This module provides the main benchmark function for timing code execution
with high-resolution monotonic timers.
"""

import time
from typing import Callable, List


def benchmark(
    func: Callable,
    runs: int = 100,
    warmup: int = 0
) -> List[float]:
    """Benchmark a callable by measuring its execution time over multiple runs.

    This function executes the provided callable multiple times and measures
    the execution duration of each run using a high-resolution monotonic timer
    (time.perf_counter). Optional warmup runs can be performed to stabilize
    performance before timing begins.

    Args:
        func: A callable object (function, lambda, method, etc.) to benchmark.
              The callable should not require arguments. Use lambda or functools.partial
              to wrap functions that need arguments.
        runs: Number of timed executions to perform. Must be greater than 0.
              Default is 100.
        warmup: Number of untimed warmup executions to perform before timing.
                Warmup runs help stabilize performance by warming up caches,
                JIT compilation, etc. Must be non-negative. Default is 0.

    Returns:
        A list of float values representing the execution time in seconds for
        each run. The list length equals the 'runs' parameter. Times are measured
        using time.perf_counter() which provides the highest available resolution.

    Raises:
        TypeError: If func is not callable.
        ValueError: If runs is less than 1 or warmup is negative.

    Examples:
        Basic usage:
        >>> def my_func():
        ...     return sum(range(1000))
        >>> durations = benchmark(my_func, runs=10)
        >>> len(durations)
        10
        >>> all(d > 0 for d in durations)
        True

        With warmup runs:
        >>> durations = benchmark(my_func, runs=50, warmup=10)
        >>> len(durations)  # Only timed runs are returned
        50

        Using lambda for functions with arguments:
        >>> durations = benchmark(lambda: sum(range(10000)), runs=20)
        >>> len(durations)
        20

        Analyzing results:
        >>> durations = benchmark(my_func, runs=100)
        >>> min_time = min(durations)
        >>> max_time = max(durations)
        >>> avg_time = sum(durations) / len(durations)
    """
    # Validate inputs
    if not callable(func):
        raise TypeError(f"func must be callable, got {type(func).__name__}")
    
    if not isinstance(runs, int) or runs < 1:
        raise ValueError(f"runs must be a positive integer, got {runs}")
    
    if not isinstance(warmup, int) or warmup < 0:
        raise ValueError(f"warmup must be a non-negative integer, got {warmup}")
    
    # Perform warmup runs (untimed)
    for _ in range(warmup):
        func()
    
    # Perform timed runs
    durations: List[float] = []
    for _ in range(runs):
        start_time = time.perf_counter()
        func()
        end_time = time.perf_counter()
        duration = end_time - start_time
        durations.append(duration)
    
    return durations
