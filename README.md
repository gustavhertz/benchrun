# BenchRun

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A minimal, high-precision Python benchmarking library for measuring code performance with statistical analysis.

## Features

- 🚀 **High-resolution timing** using `time.perf_counter()`
- 📊 **Statistical analysis** (mean, median, std dev, min, max)
- 🔥 **Warmup runs** to stabilize JIT compilation and caching
- 🎯 **Simple API** - just one function to learn
- 📦 **Zero dependencies** - pure Python implementation
- 🔬 **Precise measurements** for micro-benchmarks

## Installation

```bash
pip install benchrun
```

Or install from source:

```bash
git clone https://github.com/gustavhertz/benchrun.git
cd benchrun
pip install -e .
```

## Quick Start

```python
from benchrun import benchmark

# Benchmark a simple function
def my_function():
    return sum(range(1000))

result = benchmark(my_function)
print(f"Mean time: {result.mean:.6f}s")
print(f"Std dev: {result.std:.6f}s")
```

## API Reference

### `benchmark(func, iterations=100, warmup=0)`

Benchmark a callable function with high-precision timing.

**Parameters:**
- `func` (callable): The function to benchmark (no arguments)
- `iterations` (int, optional): Number of times to run the function. Default: 100
- `warmup` (int, optional): Number of warmup runs before measurement. Default: 0

**Returns:**
- `BenchmarkResult`: Object containing timing statistics

**BenchmarkResult attributes:**
- `times` (list[float]): Raw timing data for each iteration (in seconds)
- `mean` (float): Mean execution time
- `median` (float): Median execution time
- `std` (float): Standard deviation
- `min` (float): Minimum execution time
- `max` (float): Maximum execution time

## Usage Examples

### Basic Benchmarking

```python
from benchrun import benchmark

# Simple function benchmark
result = benchmark(lambda: sum(range(10000)))
print(f"Mean: {result.mean*1000:.3f}ms")
print(f"Median: {result.median*1000:.3f}ms")
print(f"Std Dev: {result.std*1000:.3f}ms")
```

### Custom Iterations

```python
# Run 1000 iterations for more stable results
result = benchmark(lambda: sorted([5,2,8,1,9]), iterations=1000)
print(f"Mean time: {result.mean*1000:.3f}ms")
```

### Warmup Runs

```python
# Use warmup runs to stabilize JIT compilation
result = benchmark(my_function, iterations=500, warmup=10)
print(f"Mean time (after warmup): {result.mean:.6f}s")
```

### Comparing Implementations

```python
def approach_a():
    return [x**2 for x in range(1000)]

def approach_b():
    return list(map(lambda x: x**2, range(1000)))

result_a = benchmark(approach_a, iterations=500)
result_b = benchmark(approach_b, iterations=500)

print(f"Approach A: {result_a.mean*1000:.3f}ms")
print(f"Approach B: {result_b.mean*1000:.3f}ms")
print(f"Speedup: {result_a.mean / result_b.mean:.2f}x")
```

### Accessing Raw Data

```python
result = benchmark(my_function, iterations=100)

# Access all timing measurements
print(f"All times: {result.times}")
print(f"First 5 runs: {result.times[:5]}")
print(f"Slowest run: {max(result.times)}")
print(f"Fastest run: {min(result.times)}")
```

## Example Files

The `examples/` directory contains two comprehensive example files:

### `basic_usage.py`
Demonstrates fundamental features:
- Simple function benchmarking
- Custom iteration counts
- Comparing recursive vs iterative implementations
- Using warmup runs
- Accessing raw timing data

Run it:
```bash
python examples/basic_usage.py
```

### `advanced_usage.py`
Shows advanced benchmarking scenarios:
- Comparing multiple implementations (list comprehension vs map vs generator)
- Sorting algorithm comparisons
- String concatenation performance
- Dictionary vs list lookup performance
- Detailed statistical analysis with percentiles
- Demonstrating warmup effects

Run it:
```bash
python examples/advanced_usage.py
```

## Best Practices

1. **Use enough iterations**: More iterations provide more stable results
   ```python
   # Good for fast operations
   result = benchmark(fast_func, iterations=10000)
   
   # Good for slow operations
   result = benchmark(slow_func, iterations=100)
   ```

2. **Use warmup for JIT-compiled code**: Python's JIT can affect initial runs
   ```python
   result = benchmark(func, iterations=1000, warmup=10)
   ```

3. **Minimize external factors**: Close other applications, disable background processes

4. **Benchmark in isolation**: Don't benchmark multiple things simultaneously

5. **Use lambda for parameterized functions**:
   ```python
   result = benchmark(lambda: my_func(arg1, arg2))
   ```

6. **Consider statistical significance**: Look at std dev and range
   ```python
   if result.std / result.mean > 0.1:  # High variance
       print("Results may be unstable, consider more iterations")
   ```

## Performance Tips

- For micro-benchmarks (< 1μs), use high iteration counts (10000+)
- For macro-benchmarks (> 1s), fewer iterations are needed (10-100)
- Warmup runs help stabilize results for code with JIT compilation
- The overhead of `benchmark()` itself is minimal (< 1μs per iteration)

## Development

### Running Tests

```bash
pip install -e ".[dev]"
pytest tests/
```

### Running Examples

```bash
python examples/basic_usage.py
python examples/advanced_usage.py
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Inspired by Python's `timeit` module but designed for easier statistical analysis
- Built with high-resolution timing using `time.perf_counter()`

## Changelog

### Version 0.1.0
- Initial release
- Core `benchmark()` function with statistical analysis
- Support for custom iterations and warmup runs
- Comprehensive example files
- Full documentation
