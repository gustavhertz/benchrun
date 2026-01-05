# benchrun

Minimal package for benchmarking Python implementations with high-resolution timing, parameterized tests, custom metrics, and statistical analysis.

## Installation

```bash
pip install benchrun
```

For development:

```bash
pip install -e .
```

## Quick Start

### Simple Benchmarking

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

### Using the BenchmarkRunner (Recommended)

The `BenchmarkRunner` class provides a more powerful API with support for parameterized benchmarks, custom metrics, and automatic statistical analysis.

```python
from benchrun import BenchmarkRunner, benchmark

runner = BenchmarkRunner()

@benchmark(runner, name="list_comprehension")
def test_list_comp():
    return [x * 2 for x in range(1000)]

@benchmark(runner, name="map_function")
def test_map():
    return list(map(lambda x: x * 2, range(1000)))

# Run all benchmarks and get detailed statistics
results = runner.run_all(warmup=5, iterations=100)

for result in results:
    print(f"{result['name']}:")
    print(f"  Mean: {result['mean']:.6f}s")
    print(f"  Median: {result['median']:.6f}s")
    print(f"  Std Dev: {result['std_dev']:.6f}s")
```

## Features

- **High-resolution timing**: Uses `time.perf_counter()` for accurate measurements
- **Warmup runs**: Optional warmup iterations to stabilize performance
- **Parameterized benchmarks**: Test functions with different input parameters
- **Custom metrics**: Add your own metrics (memory usage, operation counts, etc.)
- **Statistical analysis**: Automatic calculation of mean, median, std dev, variance, min, max
- **Result comparison**: Easy comparison of multiple implementations
- **Decorator API**: Clean, intuitive decorator-based interface
- **Raw data access**: Returns all individual run durations for custom analysis

## API Reference

### BenchmarkRunner Class

The main class for organizing and running benchmarks.

```python
runner = BenchmarkRunner()
```

#### Methods

- `run_all(warmup=0, iterations=100)`: Run all registered benchmarks and return results
- `get_results()`: Get the results from the last run

### @benchmark Decorator

Decorator for registering functions to benchmark.

```python
@benchmark(runner, name="my_benchmark", params=None, warmup=None, iterations=None, metrics=None)
def my_function(param1, param2):
    # function code
    pass
```

#### Parameters

- `runner` (BenchmarkRunner): The runner instance to register with
- `name` (str, optional): Name for the benchmark (defaults to function name)
- `params` (dict, optional): Dictionary of parameter names to lists of values for parameterized testing
- `warmup` (int, optional): Number of warmup iterations (overrides runner default)
- `iterations` (int, optional): Number of timed iterations (overrides runner default)
- `metrics` (list, optional): List of custom metric functions

### Parameterized Benchmarks

Test your functions with different input parameters:

```python
runner = BenchmarkRunner()

@benchmark(runner, name="sorting", params={"size": [100, 1000, 10000]})
def test_sort(size):
    arr = list(range(size, 0, -1))
    arr.sort()
    return arr

results = runner.run_all(warmup=5, iterations=50)

# Results will include separate entries for each parameter combination
for result in results:
    size = result['params']['size']
    print(f"Size {size}: {result['mean']:.6f}s")
```

### Custom Metrics

Add custom metrics to track additional information:

```python
import tracemalloc

def memory_metric(func, *args, **kwargs):
    """Measure peak memory usage."""
    tracemalloc.start()
    result = func(*args, **kwargs)
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    return {"peak_memory_kb": peak / 1024}

@benchmark(runner, name="memory_test", metrics=[memory_metric])
def test_memory():
    return [i for i in range(100000)]

results = runner.run_all()
print(f"Peak memory: {results[0]['custom_metrics']['peak_memory_kb']:.2f} KB")
```

### Result Format

Each result dictionary contains:

```python
{
    'name': 'benchmark_name',
    'iterations': 100,
    'mean': 0.001234,      # seconds
    'median': 0.001230,    # seconds
    'std_dev': 0.000012,   # seconds
    'variance': 0.000000144,  # seconds²
    'min': 0.001210,       # seconds
    'max': 0.001260,       # seconds
    'durations': [...],    # list of all individual timings
    'params': {...},       # parameter values (if parameterized)
    'custom_metrics': {...}  # custom metric values (if any)
}
```

## Examples

The `examples/` directory contains two comprehensive examples:

### simple_benchmark.py

Demonstrates basic benchmarking usage:
- Simple function benchmarking
- Using the legacy `benchmark()` function
- Using the `BenchmarkRunner` class
- Basic result analysis

### advanced_benchmark.py

Demonstrates advanced features:
- **Parameterized benchmarks**: Testing with different data sizes
- **Custom metrics**: Memory usage tracking and operation counting
- **Result comparison**: Comparing multiple algorithm implementations
- **Statistical analysis**: Detailed performance statistics and stability assessment

Run the examples:

```bash
python examples/simple_benchmark.py
python examples/advanced_benchmark.py
```

## Legacy API

The original simple function-based API is still supported:

```python
from benchrun import benchmark

durations = benchmark(my_function, runs=100, warmup=10)
```

### Parameters

- `func` (callable): The function to benchmark
- `runs` (int, default=100): Number of timed executions
- `warmup` (int, default=0): Number of untimed warmup executions

### Returns

A list of float values representing the execution time in seconds for each run.

## Best Practices

1. **Use warmup runs**: Always include warmup iterations to let the system stabilize
2. **Run enough iterations**: Use at least 50-100 iterations for reliable statistics
3. **Isolate benchmarks**: Close other applications to reduce noise
4. **Test with realistic data**: Use parameter sizes that match your actual use case
5. **Check stability**: Look at the coefficient of variation (std_dev/mean) - lower is better
6. **Compare fairly**: Ensure all benchmarks run under the same conditions

## Requirements

- Python 3.8+

## License

MIT
