# benchrun

Minimal package for benchmarking Python implementations with high-resolution timing.

## Features

- **High-resolution timing** using `time.perf_counter()`
- **Warmup runs** to stabilize performance before measurement
- **Multiple implementation comparison** with automatic speedup calculations
- **Comprehensive statistics** including mean, median, std dev, min, max, and percentiles
- **Clean output formatting** with automatic unit selection (s, ms, μs, ns)
- **Simple API** - easy to use for quick benchmarks or detailed analysis

## Installation

```bash
pip install benchrun
```

## Quick Start

### Simple Comparison

Compare two implementations to see which is faster:

```python
from benchrun import BenchmarkRunner

def concatenate_with_plus():
    result = ""
    for i in range(100):
        result = result + str(i)
    return result

def concatenate_with_join():
    return ''.join(str(i) for i in range(100))

# Create runner and add implementations
runner = BenchmarkRunner(runs=500, warmup=50)
runner.add_implementation(concatenate_with_plus, "plus_operator")
runner.add_implementation(concatenate_with_join, "join_method")

# Run and display results
runner.run()
runner.print_comparison()
```

Output:
```
Benchmark Comparison
====================================================================================================

Implementation      Mean        Median      Std Dev     Min         Max         Speedup
────────────────────────────────────────────────────────────────────────────────────────────────────
join_method        15.234μs    15.100μs     1.234μs    14.200μs    18.900μs     1.00x ★
plus_operator      89.456μs    88.900μs     3.456μs    85.600μs    98.700μs     0.17x

Summary:
  Fastest: join_method (15.234μs)
  Slowest: plus_operator (89.456μs)
  Difference: 5.87x
```

### Multiple Implementations

Compare several approaches at once:

```python
from benchrun import BenchmarkRunner

def sum_with_loop():
    total = 0
    for i in range(1000):
        total += i
    return total

def sum_with_builtin():
    return sum(range(1000))

def sum_with_generator():
    return sum(i for i in range(1000))

def sum_with_list_comp():
    return sum([i for i in range(1000)])

runner = BenchmarkRunner(runs=1000, warmup=100)
runner.add_implementation(sum_with_loop, "for_loop")
runner.add_implementation(sum_with_builtin, "builtin_sum")
runner.add_implementation(sum_with_generator, "generator")
runner.add_implementation(sum_with_list_comp, "list_comp")

results = runner.run()
runner.print_comparison()
```

### Low-Level API

For more control, use the `benchmark` function directly:

```python
from benchrun import benchmark
import statistics

def my_function():
    return sum(range(1000))

# Get raw timing data
durations = benchmark(my_function, runs=100, warmup=10)

# Analyze results
print(f"Mean: {statistics.mean(durations)*1000:.3f}ms")
print(f"Median: {statistics.median(durations)*1000:.3f}ms")
print(f"Std Dev: {statistics.stdev(durations)*1000:.3f}ms")
print(f"Min: {min(durations)*1000:.3f}ms")
print(f"Max: {max(durations)*1000:.3f}ms")
```

## API Reference

### BenchmarkRunner

Main class for comparing multiple implementations.

```python
runner = BenchmarkRunner(runs=100, warmup=0)
```

**Parameters:**
- `runs` (int): Number of timed executions per implementation (default: 100)
- `warmup` (int): Number of untimed warmup executions (default: 0)

**Methods:**

- `add_implementation(func, name=None)`: Add a function to benchmark
  - `func`: Callable to benchmark
  - `name`: Optional name (uses function name if not provided)
  - Returns: self (for method chaining)

- `run()`: Execute all benchmarks
  - Returns: Dict[str, BenchmarkResults]

- `print_comparison(sort_by="mean", show_all_stats=True)`: Display formatted results
  - `sort_by`: Metric to sort by ("mean", "median", "min", "max")
  - `show_all_stats`: Show all statistics or just key metrics

- `get_results()`: Get benchmark results
  - Returns: Dict[str, BenchmarkResults] or None

- `clear()`: Clear all implementations and results

### benchmark()

Low-level function for timing a single callable.

```python
durations = benchmark(func, runs=100, warmup=0)
```

**Parameters:**
- `func` (Callable): Function to benchmark
- `runs` (int): Number of timed executions (default: 100)
- `warmup` (int): Number of untimed warmup executions (default: 0)

**Returns:**
- List[float]: Execution times in seconds for each run

### BenchmarkResults

Container for benchmark results with computed statistics.

**Attributes:**
- `name`: Implementation name
- `durations`: List of execution times
- `runs`: Number of timed runs
- `warmup`: Number of warmup runs
- `mean`: Mean execution time
- `median`: Median execution time
- `std_dev`: Standard deviation
- `min_time`: Minimum execution time
- `max_time`: Maximum execution time
- `percentile_95`: 95th percentile
- `percentile_99`: 99th percentile
- `speedup`: Speedup relative to fastest (set by comparison)
- `relative_performance`: Performance relative to fastest (set by comparison)

**Methods:**
- `format_time(time_value)`: Format time with appropriate units

## Examples

See the `examples/` directory for complete examples:

- `simple_comparison.py`: Basic comparison of two implementations
- `multi_implementation.py`: Comparing multiple approaches

## Why benchrun?

- **Minimal dependencies**: Pure Python, no external dependencies
- **Focused scope**: Does one thing well - timing code execution
- **Raw data access**: Get the actual timing data for custom analysis
- **Flexible**: Use high-level comparison tools or low-level timing functions
- **Accurate**: Uses `time.perf_counter()` for high-resolution monotonic timing

## Best Practices

1. **Use warmup runs**: Helps stabilize performance by warming up caches and JIT compilation
   ```python
   runner = BenchmarkRunner(runs=1000, warmup=100)
   ```

2. **Run enough iterations**: More runs give more stable statistics
   ```python
   # For fast operations, use more runs
   runner = BenchmarkRunner(runs=10000)
   ```

3. **Isolate what you're measuring**: Benchmark only the code you care about
   ```python
   # Good: measures only the operation
   def test_func():
       return sorted(data)
   
   # Bad: includes setup in timing
   def test_func():
       data = list(range(1000))
       return sorted(data)
   ```

4. **Use lambda for functions with arguments**:
   ```python
   data = list(range(1000))
   runner.add_implementation(lambda: sorted(data), "sorted")
   ```

## License

MIT License - see LICENSE file for details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Links

- **GitHub**: https://github.com/gustavhertz/benchrun
- **Issues**: https://github.com/gustavhertz/benchrun/issues