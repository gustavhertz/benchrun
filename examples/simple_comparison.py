"""Simple example comparing two implementations."""

from benchrun import BenchmarkRunner


def main():
    """Compare two simple implementations."""
    # Create runner
    runner = BenchmarkRunner(runs=500