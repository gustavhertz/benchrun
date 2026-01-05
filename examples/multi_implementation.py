"""Example demonstrating multi-implementation benchmarking."""

from benchrun import BenchmarkRunner


def sum_with_loop():
    """Sum using a for loop."""
    total = 0
    for i in range(1000):
        total += i
    return total


def sum_with_builtin():
    """Sum using built-in sum function."""
    return sum(range(1000))


def sum_with_generator():
    """Sum using a generator expression."""
    return sum(i for i in range(1000))


def sum_with_list_comp():
    """Sum using list comprehension."""
    return sum([i for i in range(1000)])


def main():
    """Run the benchmark comparison."""
    print("Benchmarking different sum implementations...\n")
    
    # Create a benchmark runner
    runner = BenchmarkRunner(runs=1000, warmup=100)
    
    # Add implementations
    runner.add_implementation(sum_with_loop, "for_loop")
    runner.add_implementation(sum_with_builtin, "builtin_sum")
    runner.add_implementation(sum_with_generator, "generator")
    runner.add_implementation(sum_with_list_comp, "list_comp")
    
    # Run benchmarks
    print("Running benchmarks...")
    results = runner.run()
    
    # Print comparison
    runner.print_comparison()
    
    # Access individual results
    print("\nDetailed results for 'builtin_sum':")
    print(results["builtin_sum"])
    
    # Print with different sorting
    print("\n" + "=" * 100)
    print("Sorted by median time:")
    runner.print_comparison(sort_by="median", show_all_stats=False)


if __name__ == "__main__":
    main()