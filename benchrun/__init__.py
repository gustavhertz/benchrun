"""benchrun - Minimal package for benchmarking Python implementations."""

from benchrun.benchmark import benchmark
from benchrun.runner import BenchmarkRunner
from benchrun.results import BenchmarkResults
from benchrun.display import print_comparison

__version__ = "0.2.0"
__all__ = ["benchmark", "BenchmarkRunner", "BenchmarkResults", "print_comparison"]