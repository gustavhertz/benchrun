"""Data structures for storing benchmark results."""

import statistics
from typing import List, Optional
from dataclasses import dataclass, field


@dataclass
class BenchmarkResults:
    """Container for benchmark results and statistics.
    
    Attributes:
        name: Name of the implementation
        durations: List of execution times in seconds
        runs: Number of timed runs
        warmup: Number of warmup runs
        mean: Mean execution time
        median: Median execution time
        std_dev: Standard deviation of execution times
        min_time: Minimum execution time
        max_time: Maximum execution time
        percentile_95: 95th percentile execution time
        percentile_99: 99th percentile execution time
        speedup: Speedup relative to baseline (set by comparison)
        relative_performance: Performance relative to fastest (set by comparison)
    """
    
    name: str
    durations: List[float]
    runs: int
    warmup: int
    mean: float = field(init=False)
    median: float = field(init=False)
    std_dev: float = field(init=False)
    min_time: float = field(init=False)
    max_time: float = field(init=False)
    percentile_95: float = field(init=False)
    percentile_99: float = field(init=False)
    speedup: Optional[float] = field(default=None, init=False)
    relative_performance: Optional[float] = field(default=None, init=False)
    
    def __post_init__(self):
        """Calculate statistics after initialization."""
        if not self.durations:
            raise ValueError("durations list cannot be empty")
        
        self.mean = statistics.mean(self.durations)
        self.median = statistics.median(self.durations)
        self.std_dev = statistics.stdev(self.durations) if len(self.durations) > 1 else 0.0
        self.min_time = min(self.durations)
        self.max_time = max(self.durations)
        
        # Calculate percentiles
        sorted_durations = sorted(self.durations)
        self.percentile_95 = self._percentile(sorted_durations, 95)
        self.percentile_99 = self._percentile(sorted_durations, 99)
    
    @staticmethod
    def _percentile(sorted_data: List[float], percentile: float) -> float:
        """Calculate percentile from sorted data.
        
        Args:
            sorted_data: Sorted list of values
            percentile: Percentile to calculate (0-100)
        
        Returns:
            The value at the given percentile
        """
        if not sorted_data:
            return 0.0
        
        k = (len(sorted_data) - 1) * (percentile / 100)
        f = int(k)
        c = f + 1
        
        if c >= len(sorted_data):
            return sorted_data[-1]
        
        d0 = sorted_data[f]
        d1 = sorted_data[c]
        return d0 + (d1 - d0) * (k - f)
    
    def format_time(self, time_value: float) -> str:
        """Format a time value with appropriate units.
        
        Args:
            time_value: Time in seconds
        
        Returns:
            Formatted string with appropriate unit (s, ms, μs, ns)
        """
        if time_value >= 1.0:
            return f"{time_value:.6f}s"
        elif time_value >= 1e-3:
            return f"{time_value * 1e3:.3f}ms"
        elif time_value >= 1e-6:
            return f"{time_value * 1e6:.3f}μs"
        else:
            return f"{time_value * 1e9:.3f}ns"
    
    def __str__(self) -> str:
        """String representation of results."""
        lines = [
            f"Benchmark Results: {self.name}",
            f"  Runs: {self.runs} (warmup: {self.warmup})",
            f"  Mean:   {self.format_time(self.mean)}",
            f"  Median: {self.format_time(self.median)}",
            f"  Std:    {self.format_time(self.std_dev)}",
            f"  Min:    {self.format_time(self.min_time)}",
            f"  Max:    {self.format_time(self.max_time)}",
        ]
        
        if self.speedup is not None:
            lines.append(f"  Speedup: {self.speedup:.2f}x")
        
        if self.relative_performance is not None:
            lines.append(f"  Relative: {self.relative_performance:.1f}%")
        
        return "\n".join(lines)