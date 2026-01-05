"""benchrun - Minimal package for benchmarking Python implementations.

This package provides high-resolution timing utilities for benchmarking
Python code with support for warmup runs and raw timing data access.
"""

from benchrun.core import benchmark

__version__ = "0.1.0"
__all__ = ["benchmark"]
