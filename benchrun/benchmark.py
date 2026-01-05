"""Core benchmarking functionality."""

import time
import logging
from typing import Callable, List

logger = logging.getLogger(__name__)


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
    logger.debug(f"Starting benchmark: runs={runs}, warmup={warmup}")
    
    # Warmup runs
    if warmup > 0:
        logger.debug(f"Starting warmup: {warmup} runs")
        for _ in range(warmup):
            func()
        logger.debug("Warmup complete")
    
    # Timed runs
    logger.debug(f"Starting timed runs: {runs} runs")
    durations = []
    progress_interval = max(1, runs // 10)  # Log every 10% or at least every run
    
    for i in range(runs):
        start = time.perf_counter()
        func()
        end = time.perf_counter()
        duration = end - start
        durations.append(duration)
        
        # Log progress for long-running benchmarks
        if runs >= 100 and (i + 1) % progress_interval == 0:
            logger.debug(f"Progress: {i + 1}/{runs} runs complete")
    
    # Calculate and log summary statistics
    if durations:
        mean = sum(durations) / len(durations)
        min_time = min(durations)
        max_time = max(durations)
        logger.debug(f"Benchmark complete: {runs} runs, mean={mean:.6f}s, min={min_time:.6f}s, max={max_time:.6f}s")
    
    return durations