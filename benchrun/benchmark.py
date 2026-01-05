"""Core benchmarking functionality."""

import time
from typing import Callable, List


def benchmark(func: Callable, runs: int = 100, warmup: int = 0) -> List[float]:
    """Benchmark a function with high-resolution timing.
    
    Args:
        func: The function to benchmark
        runs: Number of timed executions (default: 100)
        warmup: Number of untimed warmup executions (default: 0)
    
    Returns:
        List of execution times in seconds for each run
    
    Example:
        >>> def my_func():
        ...     return sum(range(1000))
        >>> durations = benchmark(my_func, runs=10, warmup=5)
        >>> print(f"Mean: {sum(durations)/len(durations):.6f}s")
    """
    # Warmup runs
    for _ in range(warmup):
        func()
    
    # Timed runs
    durations = []
    for _ in range(runs):
        start = time.perf_counter()
        func()
        end = time.perf_counter()
        durations.append(end - start)
    
    return durations