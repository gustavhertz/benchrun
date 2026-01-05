"""Advanced usage example for benchrun.

This example demonstrates advanced features:
- Benchmarking with different parameters
- Statistical analysis and percentiles
- Memory-intensive operations
- Complex comparison scenarios
- Result visualization and reporting
"""

from benchrun import benchmark
import random
import statistics


def list_comprehension(n):
    """Create list using list comprehension."""
    return [i * 2 for i in range(n)]


def map_function(n):
    """Create list using map function."""
    return list(map(lambda x: x * 2, range(n)))


def generator_expression(n):
    """Create list using generator expression."""
    return list(i * 2 for i in range(n))


def sort_builtin(data):
    """Sort using built-in sorted()."""
    return sorted(data)


def sort_method(data):
    """Sort using list.sort() method."""
    data_copy = data.copy()
    data_copy.sort()
    return data_copy


def string_concatenation(n):
    """Concatenate strings using + operator."""
    result = ""
    for i in range(n):
        result += str(i)
    return result


def string_join(n):
    """Concatenate strings using join()."""
    return "".join(str(i) for i in range(n))


def dict_lookup(data, keys):
    """Perform dictionary lookups."""
    return [data.get(key) for key in keys]


def list_search(data, keys):
    """Perform linear search in list."""
    return [key for key in keys if key in data]


if __name__ == "__main__":
    print("=" * 70)
    print("BenchRun - Advanced Usage Examples")
    print("=" * 70)
    
    # Example 1: Comparing list creation methods
    print("\n1. List Creation Methods Comparison:")
    print("   Testing with 10,000 elements...")
    n = 10000
    
    methods = [
        ("List Comprehension", lambda: list_comprehension(n)),
        ("Map Function", lambda: map_function(n)),
        ("Generator Expression", lambda: generator_expression(n)),
    ]
    
    results = []
    for name, func in methods:
        result = benchmark(func, iterations=500)
        results.append((name, result))
        print(f"   {name:25s} - Mean: {result.mean*1000:.3f}ms, Std: {result.std*1000:.3f}ms")
    
    fastest = min(results, key=lambda x: x[1].mean)
    print(f"\n   Fastest method: {fastest[0]}")
    
    # Example 2: Sorting algorithms comparison
    print("\n2. Sorting Methods Comparison:")
    test_data = [random.randint(1, 1000) for _ in range(5000)]
    print(f"   Sorting {len(test_data)} random integers...")
    
    sort_result1 = benchmark(lambda: sort_builtin(test_data), iterations=200)
    sort_result2 = benchmark(lambda: sort_method(test_data), iterations=200)
    
    print(f"   sorted() function - Mean: {sort_result1.mean*1000:.3f}ms")
    print(f"   list.sort() method - Mean: {sort_result2.mean*1000:.3f}ms")
    print(f"   Difference: {abs(sort_result1.mean - sort_result2.mean)*1000:.3f}ms")
    
    # Example 3: String concatenation performance
    print("\n3. String Concatenation Performance:")
    n = 1000
    print(f"   Concatenating {n} strings...")
    
    concat_result = benchmark(lambda: string_concatenation(n), iterations=100)
    join_result = benchmark(lambda: string_join(n), iterations=100)
    
    print(f"   + operator - Mean: {concat_result.mean*1000:.3f}ms")
    print(f"   join() method - Mean: {join_result.mean*1000:.3f}ms")
    print(f"   Speedup: {concat_result.mean / join_result.mean:.2f}x")
    
    # Example 4: Dictionary vs List lookup
    print("\n4. Dictionary vs List Lookup Performance:")
    size = 1000
    lookup_keys = random.sample(range(size * 2), 100)
    
    dict_data = {i: f"value_{i}" for i in range(size)}
    list_data = list(range(size))
    
    dict_result = benchmark(lambda: dict_lookup(dict_data, lookup_keys), iterations=500)
    list_result = benchmark(lambda: list_search(list_data, lookup_keys), iterations=500)
    
    print(f"   Dictionary lookup - Mean: {dict_result.mean*1000:.3f}ms")
    print(f"   List search - Mean: {list_result.mean*1000:.3f}ms")
    print(f"   Dictionary is {list_result.mean / dict_result.mean:.2f}x faster")
    
    # Example 5: Statistical analysis
    print("\n5. Detailed Statistical Analysis:")
    result = benchmark(lambda: sum(range(50000)), iterations=1000)
    
    print(f"   Iterations: {len(result.times)}")
    print(f"   Mean: {result.mean*1000:.3f}ms")
    print(f"   Median: {result.median*1000:.3f}ms")
    print(f"   Std Dev: {result.std*1000:.3f}ms")
    print(f"   Min: {result.min*1000:.3f}ms")
    print(f"   Max: {result.max*1000:.3f}ms")
    print(f"   Range: {(result.max - result.min)*1000:.3f}ms")
    
    # Calculate percentiles
    p25 = statistics.quantiles(result.times, n=4)[0]
    p75 = statistics.quantiles(result.times, n=4)[2]
    p95 = statistics.quantiles(result.times, n=20)[18]
    p99 = statistics.quantiles(result.times, n=100)[98]
    
    print(f"   25th percentile: {p25*1000:.3f}ms")
    print(f"   75th percentile: {p75*1000:.3f}ms")
    print(f"   95th percentile: {p95*1000:.3f}ms")
    print(f"   99th percentile: {p99*1000:.3f}ms")
    
    # Example 6: Warmup effect demonstration
    print("\n6. Warmup Effect Demonstration:")
    print("   Without warmup:")
    result_no_warmup = benchmark(lambda: fibonacci_iterative(30), iterations=100, warmup=0)
    print(f"   First 5 times: {[f'{t*1000:.3f}ms' for t in result_no_warmup.times[:5]]}")
    print(f"   Mean: {result_no_warmup.mean*1000:.3f}ms")
    
    print("\n   With 10 warmup runs:")
    result_with_warmup = benchmark(lambda: fibonacci_iterative(30), iterations=100, warmup=10)
    print(f"   First 5 times: {[f'{t*1000:.3f}ms' for t in result_with_warmup.times[:5]]}")
    print(f"   Mean: {result_with_warmup.mean*1000:.3f}ms")
    
    print("\n" + "=" * 70)
    print("Advanced examples completed successfully!")
    print("=" * 70)


def fibonacci_iterative(n):
    """Calculate fibonacci number iteratively."""
    if n <= 1:
        return n
    a, b = 0, 1
    for _ in range(n - 1):
        a, b = b, a + b
    return b
