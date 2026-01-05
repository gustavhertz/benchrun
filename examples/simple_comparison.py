"""Simple example comparing two implementations."""

from benchrun import BenchmarkRunner


def concatenate_with_plus():
    """Concatenate strings using the + operator."""
    result = ""
    for i in range(100):
        result = result + str(i)
    return result


def concatenate_with_join():
    """Concatenate strings using ''.join()."""
    return ''.join(str(i) for i in range(100))


def main():
    """Compare two simple implementations."""
    print("Comparing string concatenation methods...\n")
    
    # Create runner
    runner = BenchmarkRunner(runs=500, warmup=50)
    
    # Add implementations
    runner.add_implementation(concatenate_with_plus, "plus_operator")
    runner.add_implementation(concatenate_with_join, "join_method")
    
    # Run benchmarks
    print("Running benchmarks...")
    results = runner.run()
    
    # Print comparison
    runner.print_comparison()
    
    # Show individual result details
    print("\nDetailed results for 'join_method':")
    print(results["join_method"])


if __name__ == "__main__":
    main()