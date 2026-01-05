# benchrun

Minimal package for benchmarking Python implementations with high-resolution timing.

## Installation

```bash
pip install benchrun
```

For development:

```bash
pip install -e .
```

## Quick Start

```python
from benchrun import benchmark

# Define a function to benchmark
def my_function():
    result = sum(range(1000))
    return result

# Run the benchmark
durations = benchmark(my_function, runs=100, warmup=10)

# Analyze results
print(f"Runs: {len(durations)}")
print(f"Min: {min(durations):.6f}s")
print(f"Max: {max(durations):.6f}s")
print(f"Mean: {sum(durations)/len(durations):.6f}s")
```

## Features

- **High-resolution timing**: Uses `time.perf_counter()` for accurate measurements
- **Warmup runs**: Optional warmup iterations to stabilize performance
- **Raw data access**: Returns all individual run durations for custom analysis
- **Simple API**: Single function interface for easy benchmarking

## Parameters

- `func` (callable): The function to benchmark
- `runs` (int, default=100): Number of timed executions
- `warmup` (int, default=0): Number of untimed warmup executions

## Returns

A list of float values representing the execution time in seconds for each run.

## Example Output

```python
durations = benchmark(lambda: sum(range(1000)), runs=5)
# [0.000023, 0.000021, 0.000022, 0.000021, 0.000023]
```

## Roadmap

This is the initial release focusing on core timing functionality. Future features planned:
- Statistical analysis (mean, median, standard deviation)
- Comparison utilities for multiple implementations
- Result formatting and reporting
- Memory profiling integration

## Requirements

- Python 3.8+

## License

MIT
