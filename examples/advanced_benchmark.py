"""Advanced benchmarking examples demonstrating parameterized tests, custom metrics, and result comparison."""

import sys
from pathlib import Path

# Add parent directory to path to import benchrun
sys.path.insert(0, str(Path(__file__).parent.parent))

from benchrun import BenchmarkRunner, benchmark
import time
import tracemalloc


# Example 1: Parameterized Benchmarks
print("=" * 60)
print("Example 1: Parameterized Benchmarks")
print("=" * 60)
print("Testing list operations with different data sizes\n")

runner = BenchmarkRunner()

@benchmark(runner, name="list_comprehension", params={"size": [100, 1000, 10000]})
def test_list_comprehension(size):
    """Test list comprehension performance with different sizes."""
    return [x * 2 for x in range(size)]

@benchmark(runner, name="map_function", params={"size": [100, 1000, 10000]})
def test_map_function(size):
    """Test map function performance with different sizes."""
    return list(map(lambda x: x * 2, range(size)))

# Run parameterized benchmarks
results = runner.run_all(warmup=5, iterations=50)

print("\nResults by parameter:")
for result in results:
    print(f"\n{result['name']} (size={result.get('params', {}).get('size', 'N/A')}):")
    print(f"  Mean: {result['mean']:.6f}s")
    print(f"  Median: {result['median']:.6f}s")
    print(f"  Std Dev: {result['std_dev']:.6f}s")


# Example 2: Custom Metrics
print("\n" + "=" * 60)
print("Example 2: Custom Metrics")
print("=" * 60)
print("Adding memory usage and operation count metrics\n")

runner2 = BenchmarkRunner()

def memory_metric(func, *args, **kwargs):
    """Custom metric to measure peak memory usage."""
    tracemalloc.start()
    result = func(*args, **kwargs)
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    return {"peak_memory_kb": peak / 1024}

def operation_counter(func, *args, **kwargs):
    """Custom metric to count operations (example: list length)."""
    result = func(*args, **kwargs)
    return {"operations": len(result) if hasattr(result, '__len__') else 0}

@benchmark(
    runner2,
    name="string_operations",
    params={"count": [100, 500, 1000]},
    metrics=[memory_metric, operation_counter]
)
def test_string_operations(count):
    """Test string concatenation with custom metrics."""
    result = []
    for i in range(count):
        result.append(f"String number {i}" * 10)
    return result

@benchmark(
    runner2,
    name="dict_operations",
    params={"count": [100, 500, 1000]},
    metrics=[memory_metric, operation_counter]
)
def test_dict_operations(count):
    """Test dictionary creation with custom metrics."""
    return {i: f"value_{i}" for i in range(count)}

results2 = runner2.run_all(warmup=3, iterations=30)

print("\nResults with custom metrics:")
for result in results2:
    print(f"\n{result['name']} (count={result.get('params', {}).get('count', 'N/A')}):")
    print(f"  Mean Time: {result['mean']:.6f}s")
    if 'custom_metrics' in result:
        for metric_name, metric_value in result['custom_metrics'].items():
            if isinstance(metric_value, (int, float)):
                print(f"  {metric_name}: {metric_value:.2f}")
            else:
                print(f"  {metric_name}: {metric_value}")


# Example 3: Result Comparison
print("\n" + "=" * 60)
print("Example 3: Result Comparison")
print("=" * 60)
print("Comparing different sorting algorithms\n")

runner3 = BenchmarkRunner()

@benchmark(runner3, name="bubble_sort", params={"size": [50, 100, 200]})
def test_bubble_sort(size):
    """Bubble sort implementation."""
    arr = list(range(size, 0, -1))
    n = len(arr)
    for i in range(n):
        for j in range(0, n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
    return arr

@benchmark(runner3, name="python_sort", params={"size": [50, 100, 200]})
def test_python_sort(size):
    """Python's built-in sort."""
    arr = list(range(size, 0, -1))
    arr.sort()
    return arr

@benchmark(runner3, name="sorted_function", params={"size": [50, 100, 200]})
def test_sorted_function(size):
    """Python's sorted() function."""
    arr = list(range(size, 0, -1))
    return sorted(arr)

results3 = runner3.run_all(warmup=5, iterations=50)

print("\nComparison of sorting algorithms:")
print(f"{'Algorithm':<20} {'Size':<10} {'Mean (s)':<15} {'Median (s)':<15} {'Std Dev (s)':<15}")
print("-" * 75)

for result in results3:
    size = result.get('params', {}).get('size', 'N/A')
    print(f"{result['name']:<20} {size:<10} {result['mean']:<15.6f} {result['median']:<15.6f} {result['std_dev']:<15.6f}")

# Group results by size for easier comparison
print("\n\nPerformance comparison by size:")
sizes = [50, 100, 200]
for size in sizes:
    print(f"\nSize {size}:")
    size_results = [r for r in results3 if r.get('params', {}).get('size') == size]
    if size_results:
        # Sort by mean time
        size_results.sort(key=lambda x: x['mean'])
        fastest = size_results[0]
        print(f"  Fastest: {fastest['name']} ({fastest['mean']:.6f}s)")
        
        for result in size_results[1:]:
            slowdown = result['mean'] / fastest['mean']
            print(f"  {result['name']}: {result['mean']:.6f}s ({slowdown:.2f}x slower)")


# Example 4: Statistical Analysis
print("\n" + "=" * 60)
print("Example 4: Statistical Analysis")
print("=" * 60)
print("Detailed statistics for a single benchmark\n")

runner4 = BenchmarkRunner()

@benchmark(runner4, name="fibonacci", params={"n": [10, 15, 20]})
def test_fibonacci(n):
    """Recursive fibonacci (intentionally inefficient for demonstration)."""
    if n <= 1:
        return n
    return test_fibonacci(n - 1) + test_fibonacci(n - 2)

results4 = runner4.run_all(warmup=2, iterations=20)

print("\nDetailed statistics:")
for result in results4:
    n = result.get('params', {}).get('n', 'N/A')
    print(f"\nFibonacci(n={n}):")
    print(f"  Iterations: {result['iterations']}")
    print(f"  Mean: {result['mean']:.6f}s")
    print(f"  Median: {result['median']:.6f}s")
    print(f"  Min: {result['min']:.6f}s")
    print(f"  Max: {result['max']:.6f}s")
    print(f"  Std Dev: {result['std_dev']:.6f}s")
    print(f"  Variance: {result['variance']:.9f}s²")
    
    # Calculate coefficient of variation (relative std dev)
    cv = (result['std_dev'] / result['mean']) * 100 if result['mean'] > 0 else 0
    print(f"  Coefficient of Variation: {cv:.2f}%")
    
    # Stability assessment
    if cv < 5:
        stability = "Very Stable"
    elif cv < 10:
        stability = "Stable"
    elif cv < 20:
        stability = "Moderate"
    else:
        stability = "Unstable"
    print(f"  Stability: {stability}")

print("\n" + "=" * 60)
print("All examples completed!")
print("=" * 60)
