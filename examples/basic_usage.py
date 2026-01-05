"""Basic usage example for benchrun.

This example demonstrates the fundamental features of benchrun:
- Simple function benchmarking
- Multiple iterations
- Statistical analysis of results
"""

from benchrun import benchmark
import time


def fibonacci_recursive(n):
    """Calculate fibonacci number recursively (inefficient)."""
    if n <= 1:
        return n
    return fibonacci_recursive(n - 1) + fibonacci_recursive(n - 2)


def fibonacci_iterative(n):
    """Calculate fibonacci number iteratively (efficient)."""
    if n <= 1:
        return n
    a, b = 0, 1
    for _ in range(n - 1):
        a, b = b, a + b
    return b


def slow_operation():
    """Simulate a slow operation."""
    time.sleep(0.01)
    return sum(range(1000))


if __name__ == "__main__":
    print("=" * 60)
    print("BenchRun - Basic Usage Examples")
    print("=" * 60)
    
    # Example 1: Simple benchmark with default iterations
    print("\n1. Simple benchmark (default 100 iterations):")
    result = benchmark(lambda: fibonacci_iterative(20))
    print(f"   Mean time: {result.mean:.6f}s")
    print(f"   Std dev: {result.std:.6f}s")
    print(f"   Min time: {result.min:.6f}s")
    print(f"   Max time: {result.max:.6f}s")
    
    # Example 2: Custom number of iterations
    print("\n2. Custom iterations (1000 runs):")
    result = benchmark(lambda: fibonacci_iterative(15), iterations=1000)
    print(f"   Mean time: {result.mean:.6f}s")
    print(f"   Median time: {result.median:.6f}s")
    
    # Example 3: Comparing two implementations
    print("\n3. Comparing recursive vs iterative fibonacci:")
    n = 25
    
    print(f"   Calculating fibonacci({n})...")
    result_recursive = benchmark(lambda: fibonacci_recursive(n), iterations=10)
    result_iterative = benchmark(lambda: fibonacci_iterative(n), iterations=10)
    
    print(f"   Recursive - Mean: {result_recursive.mean:.6f}s")
    print(f"   Iterative - Mean: {result_iterative.mean:.6f}s")
    print(f"   Speedup: {result_recursive.mean / result_iterative.mean:.2f}x")
    
    # Example 4: Benchmarking with warmup
    print("\n4. Benchmark with warmup runs:")
    result = benchmark(slow_operation, iterations=50, warmup=5)
    print(f"   Mean time: {result.mean:.6f}s")
    print(f"   Total runs: {len(result.times)}")
    
    # Example 5: Accessing raw timing data
    print("\n5. Accessing raw timing data:")
    result = benchmark(lambda: sum(range(10000)), iterations=20)
    print(f"   First 5 times: {[f'{t:.6f}' for t in result.times[:5]]}")
    print(f"   Last 5 times: {[f'{t:.6f}' for t in result.times[-5:]]}")
    
    print("\n" + "=" * 60)
    print("Examples completed successfully!")
    print("=" * 60)
