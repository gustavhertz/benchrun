"""Utilities for comparing benchmark results."""

from typing import Dict
from benchrun.results import BenchmarkResults


def calculate_comparisons(results: Dict[str, BenchmarkResults]) -> None:
    """Calculate comparison metrics for all results.
    
    This function modifies the results in-place, adding speedup and
    relative_performance metrics.
    
    Args:
        results: Dictionary mapping implementation names to BenchmarkResults
    
    The fastest implementation gets:
        - speedup = 1.0
        - relative_performance = 100.0
    
    Other implementations get:
        - speedup = fastest_time / their_time
        - relative_performance = (fastest_time / their_time) * 100
    """
    if not results:
        return
    
    # Find the fastest implementation based on mean time
    fastest_name = min(results.keys(), key=lambda k: results[k].mean)
    fastest_time = results[fastest_name].mean
    
    # Calculate relative metrics for all implementations
    for name, result in results.items():
        if result.mean > 0:
            result.speedup = fastest_time / result.mean
            result.relative_performance = (fastest_time / result.mean) * 100
        else:
            result.speedup = 1.0
            result.relative_performance = 100.0


def get_fastest(results: Dict[str, BenchmarkResults], metric: str = "mean") -> str:
    """Get the name of the fastest implementation.
    
    Args:
        results: Dictionary mapping implementation names to BenchmarkResults
        metric: Metric to compare ('mean', 'median', 'min'). Default: 'mean'
    
    Returns:
        Name of the fastest implementation
    
    Raises:
        ValueError: If results is empty or metric is invalid
    """
    if not results:
        raise ValueError("No results to compare")
    
    valid_metrics = {"mean", "median", "min", "min_time"}
    if metric not in valid_metrics:
        raise ValueError(f"Invalid metric '{metric}'. Must be one of {valid_metrics}")
    
    # Normalize metric name
    if metric == "min":
        metric = "min_time"
    
    return min(results.keys(), key=lambda k: getattr(results[k], metric))


def get_slowest(results: Dict[str, BenchmarkResults], metric: str = "mean") -> str:
    """Get the name of the slowest implementation.
    
    Args:
        results: Dictionary mapping implementation names to BenchmarkResults
        metric: Metric to compare ('mean', 'median', 'max'). Default: 'mean'
    
    Returns:
        Name of the slowest implementation
    
    Raises:
        ValueError: If results is empty or metric is invalid
    """
    if not results:
        raise ValueError("No results to compare")
    
    valid_metrics = {"mean", "median", "max", "max_time"}
    if metric not in valid_metrics:
        raise ValueError(f"Invalid metric '{metric}'. Must be one of {valid_metrics}")
    
    # Normalize metric name
    if metric == "max":
        metric = "max_time"
    
    return max(results.keys(), key=lambda k: getattr(results[k], metric))


def calculate_speedup(baseline: BenchmarkResults, comparison: BenchmarkResults, 
                     metric: str = "mean") -> float:
    """Calculate speedup of comparison relative to baseline.
    
    Args:
        baseline: Baseline benchmark results
        comparison: Comparison benchmark results
        metric: Metric to use for comparison. Default: 'mean'
    
    Returns:
        Speedup factor (baseline_time / comparison_time)
        Values > 1.0 mean comparison is faster
        Values < 1.0 mean comparison is slower
    """
    if metric == "min":
        metric = "min_time"
    elif metric == "max":
        metric = "max_time"
    
    baseline_time = getattr(baseline, metric)
    comparison_time = getattr(comparison, metric)
    
    if comparison_time == 0:
        return float('inf')
    
    return baseline_time / comparison_time