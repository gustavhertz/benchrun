"""benchrun - Minimal package for benchmarking Python implementations."""

import logging
from benchrun.benchmark import benchmark
from benchrun.runner import BenchmarkRunner
from benchrun.results import BenchmarkResults
from benchrun.display import print_comparison

__version__ = "0.2.0"
__all__ = ["benchmark", "BenchmarkRunner", "BenchmarkResults", "print_comparison", "configure_logging"]


def configure_logging(level=logging.INFO, format_string=None):
    """Configure logging for benchrun with sensible defaults.
    
    Args:
        level: Logging level (default: logging.INFO)
               Use logging.DEBUG for detailed execution information
        format_string: Custom format string (default: includes timestamp, name, level, message)
    
    Example:
        >>> import benchrun
        >>> import logging
        >>> benchrun.configure_logging(level=logging.DEBUG)
        >>> # Now all benchrun operations will show debug output
    """
    if format_string is None:
        format_string = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    
    logging.basicConfig(
        level=level,
        format=format_string,
        datefmt='%Y-%m-%d %H:%M:%S'
    )