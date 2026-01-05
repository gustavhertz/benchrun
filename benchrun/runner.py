"""Benchmark runner for comparing multiple implementations."""

import time
import logging
from typing import Callable, Dict, Optional, List
from benchrun.results import BenchmarkResults
from benchrun.comparison import calculate_comparisons

logger = logging.getLogger(__name__)


class BenchmarkRunner:
    """Runner for benchmarking and comparing multiple function implementations.
    
    This class allows you to add multiple implementations of the same functionality
    and compare their performance.
    
    Example:
        >>> runner = BenchmarkRunner(runs=100, warmup=10)
        >>> runner.add_implementation(lambda: sum(range(1000)), "list_sum")
        >>> runner.add_implementation(lambda: sum(i for i in range(1000)), "gen_sum")
        >>> results = runner.run()
        >>> runner.print_comparison()
    """
    
    def __init__(self, runs: int = 100, warmup: int = 0):
        """Initialize the benchmark runner.
        
        Args:
            runs: Number of timed executions per implementation (default: 100)
            warmup: Number of untimed warmup executions (default: 0)
        """
        self.runs = runs
        self.warmup = warmup
        self.implementations: Dict[str, Callable] = {}
        self.results: Optional[Dict[str, BenchmarkResults]] = None
        self._impl_counter = 0
        
        logger.debug(f"BenchmarkRunner initialized: runs={runs}, warmup={warmup}")
    
    def add_implementation(self, func: Callable, name: Optional[str] = None) -> "BenchmarkRunner":
        """Add a function implementation to benchmark.
        
        Args:
            func: The function to benchmark
            name: Optional name for the implementation. If not provided,
                  uses func.__name__ or generates a name like 'impl_1'
        
        Returns:
            Self for method chaining
        
        Example:
            >>> runner = BenchmarkRunner()
            >>> runner.add_implementation(my_func, "optimized")
            >>> runner.add_implementation(other_func)  # Uses function name
        """
        if name is None:
            # Try to use function name, fall back to generated name
            if hasattr(func, '__name__') and func.__name__ != '<lambda>':
                name = func.__name__
            else:
                self._impl_counter += 1
                name = f"impl_{self._impl_counter}"
        
        # Ensure unique names
        original_name = name
        counter = 1
        while name in self.implementations:
            name = f"{original_name}_{counter}"
            counter += 1
        
        self.implementations[name] = func
        logger.debug(f"Implementation registered: '{name}'")
        logger.info(f"Added implementation: {name}")
        return self
    
    def run(self) -> Dict[str, BenchmarkResults]:
        """Run benchmarks for all registered implementations.
        
        Returns:
            Dictionary mapping implementation names to their BenchmarkResults
        
        Raises:
            ValueError: If no implementations have been added
        
        Example:
            >>> runner = BenchmarkRunner(runs=50)
            >>> runner.add_implementation(func1, "v1")
            >>> runner.add_implementation(func2, "v2")
            >>> results = runner.run()
            >>> print(results["v1"].mean)
        """
        if not self.implementations:
            logger.error("No implementations added")
            raise ValueError("No implementations added. Use add_implementation() first.")
        
        logger.info(f"Starting benchmark run: {len(self.implementations)} implementations, {self.runs} runs each, {self.warmup} warmup")
        self.results = {}
        
        for idx, (name, func) in enumerate(self.implementations.items(), 1):
            logger.info(f"Benchmarking implementation {idx}/{len(self.implementations)}: '{name}'")
            logger.debug(f"Starting warmup for '{name}': {self.warmup} runs")
            
            # Warmup runs
            for _ in range(self.warmup):
                func()
            
            if self.warmup > 0:
                logger.debug(f"Warmup complete for '{name}'")
            
            # Timed runs
            logger.debug(f"Starting timed runs for '{name}': {self.runs} runs")
            durations = []
            progress_interval = max(1, self.runs // 10)
            
            for i in range(self.runs):
                start = time.perf_counter()
                func()
                end = time.perf_counter()
                duration = end - start
                durations.append(duration)
                
                # Log progress for long-running benchmarks
                if self.runs >= 100 and (i + 1) % progress_interval == 0:
                    logger.debug(f"'{name}' progress: {i + 1}/{self.runs} runs complete")
            
            # Create results
            result = BenchmarkResults(
                name=name,
                durations=durations,
                runs=self.runs,
                warmup=self.warmup
            )
            self.results[name] = result
            
            logger.debug(f"'{name}' complete: mean={result.mean:.6f}s, min={result.min_time:.6f}s, max={result.max_time:.6f}s")
            logger.info(f"Completed '{name}': mean={result.format_time(result.mean)}")
        
        # Calculate comparisons
        logger.debug("Calculating performance comparisons")
        calculate_comparisons(self.results)
        
        # Log comparison summary
        if self.results:
            fastest_name = min(self.results.keys(), key=lambda k: self.results[k].mean)
            fastest_time = self.results[fastest_name].mean
            logger.info(f"Benchmark complete. Fastest: '{fastest_name}' ({self.results[fastest_name].format_time(fastest_time)})")
        
        return self.results
    
    def print_comparison(self, sort_by: str = "mean", show_all_stats: bool = True) -> None:
        """Print a comparison table of all benchmark results.
        
        Args:
            sort_by: Metric to sort by ('mean', 'median', 'min', 'max'). Default: 'mean'
            show_all_stats: Whether to show all statistics or just key metrics. Default: True
        
        Raises:
            ValueError: If run() hasn't been called yet
        
        Example:
            >>> runner = BenchmarkRunner(runs=100)
            >>> runner.add_implementation(func1, "v1")
            >>> runner.add_implementation(func2, "v2")
            >>> runner.run()
            >>> runner.print_comparison()
        """
        if self.results is None:
            logger.error("print_comparison called before run()")
            raise ValueError("No results available. Call run() first.")
        
        logger.debug(f"Printing comparison table: sort_by={sort_by}, show_all_stats={show_all_stats}")
        from benchrun.display import print_comparison
        print_comparison(self.results, sort_by=sort_by, show_all_stats=show_all_stats)
    
    def get_results(self) -> Optional[Dict[str, BenchmarkResults]]:
        """Get the benchmark results.
        
        Returns:
            Dictionary of results, or None if run() hasn't been called
        """
        return self.results
    
    def clear(self) -> None:
        """Clear all implementations and results."""
        logger.debug("Clearing all implementations and results")
        self.implementations.clear()
        self.results = None
        self._impl_counter = 0
        logger.info("Runner cleared")