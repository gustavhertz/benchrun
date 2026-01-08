"""Display and formatting utilities for benchmark results."""

from typing import Dict, List, Tuple
from benchrun.results import BenchmarkResults


def print_comparison(results: Dict[str, BenchmarkResults], 
                    sort_by: str = "mean",
                    show_all_stats: bool = True) -> None:
    """Print a formatted comparison table of benchmark results.
    
    Args:
        results: Dictionary mapping implementation names to BenchmarkResults
        sort_by: Metric to sort by ('mean', 'median', 'min', 'max'). Default: 'mean'
        show_all_stats: Whether to show all statistics. Default: True
    
    Example output:
        Benchmark Comparison
        ==========================================
        
        Implementation      Mean        Median      Std Dev     Min         Max         Speedup
        ─────────────────────────────────────────────────────────────────────────────────────────
        optimized          1.234ms     1.230ms     0.045ms     1.180ms     1.350ms     1.00x ★
        baseline           2.456ms     2.450ms     0.089ms     2.340ms     2.680ms     0.50x
        slow_version       4.890ms     4.870ms     0.156ms     4.650ms     5.230ms     0.25x
    """
    if not results:
        print("No results to display.")
        return
    
    # Normalize sort_by
    if sort_by == "min":
        sort_by = "min_time"
    elif sort_by == "max":
        sort_by = "max_time"
    
    # Sort results
    sorted_names = sorted(results.keys(), key=lambda k: getattr(results[k], sort_by))
    
    # Find the fastest for marking
    fastest_name = sorted_names[0]
    
    # Print header
    print("\nBenchmark Comparison")
    print("=" * 100)
    print()
    
    # Determine column widths
    max_name_len = max(len(name) for name in results.keys())
    name_width = max(max_name_len, len("Implementation"))
    
    # Print table header
    if show_all_stats:
        header = f"{'Implementation':<{name_width}}  {'Mean':>12}  {'Median':>12}  {'Std Dev':>12}  {'Min':>12}  {'Max':>12}  {'Speedup':>10}"
    else:
        header = f"{'Implementation':<{name_width}}  {'Mean':>12}  {'Std Dev':>12}  {'Speedup':>10}"
    
    print(header)
    print("─" * len(header))
    
    # Print results
    for name in sorted_names:
        result = results[name]
        is_fastest = (name == fastest_name)
        
        # Format times
        mean_str = result.format_time(result.mean)
        median_str = result.format_time(result.median)
        std_str = result.format_time(result.std_dev)
        min_str = result.format_time(result.min_time)
        max_str = result.format_time(result.max_time)
        
        # Format speedup
        speedup_str = f"{result.speedup:.2f}x" if result.speedup else "N/A"
        if is_fastest:
            speedup_str += " ★"
        
        # Print row
        if show_all_stats:
            print(f"{name:<{name_width}}  {mean_str:>12}  {median_str:>12}  {std_str:>12}  {min_str:>12}  {max_str:>12}  {speedup_str:>10}")
        else:
            print(f"{name:<{name_width}}  {mean_str:>12}  {std_str:>12}  {speedup_str:>10}")
    
    print()
    
    # Print summary
    fastest_result = results[fastest_name]
    slowest_name = sorted_names[-1]
    slowest_result = results[slowest_name]
    
    print("Summary:")
    print(f"  Fastest: {fastest_name} ({fastest_result.format_time(fastest_result.mean)})")
    print(f"  Slowest: {slowest_name} ({slowest_result.format_time(slowest_result.mean)})")
    
    if len(results) > 1:
        ratio = slowest_result.mean / fastest_result.mean
        print(f"  Difference: {ratio:.2f}x")
    
    print()


def format_results_table(results: Dict[str, BenchmarkResults], 
                        sort_by: str = "mean") -> List[str]:
    """Format results as a list of strings for custom display.
    
    Args:
        results: Dictionary mapping implementation names to BenchmarkResults
        sort_by: Metric to sort by ('mean', 'median', 'min', 'max'). Default: 'mean'
    
    Returns:
        List of formatted strings, one per line
    
    Example:
        >>> results = {"impl1": result1, "impl2": result2}
        >>> lines = format_results_table(results)
        >>> for line in lines:
        ...     print(line)
    """
    lines = []
    
    if not results:
        return ["No results to display."]
    
    # Normalize sort_by
    if sort_by == "min":
        sort_by = "min_time"
    elif sort_by == "max":
        sort_by = "max_time"
    
    # Sort results
    sorted_names = sorted(results.keys(), key=lambda k: getattr(results[k], sort_by))
    
    lines.append("")
    lines.append("Benchmark Results")
    lines.append("=" * 50)
    
    for name in sorted_names:
        result = results[name]
        lines.append("")
        lines.append(f"{name}:")
        lines.append(f"  Mean:   {result.format_time(result.mean)}")
        lines.append(f"  Median: {result.format_time(result.median)}")
        lines.append(f"  Std:    {result.format_time(result.std_dev)}")
        lines.append(f"  Min:    {result.format_time(result.min_time)}")
        lines.append(f"  Max:    {result.format_time(result.max_time)}")
        if result.speedup:
            lines.append(f"  Speedup: {result.speedup:.2f}x")
    
    return lines


def create_bar_chart(results: Dict[str, BenchmarkResults], 
                    metric: str = "mean",
                    width: int = 50) -> str:
    """Create a simple ASCII bar chart of results.
    
    Args:
        results: Dictionary mapping implementation names to BenchmarkResults
        metric: Metric to display ('mean', 'median', 'min', 'max'). Default: 'mean'
        width: Width of the longest bar in characters. Default: 50
    
    Returns:
        Formatted bar chart as a string
    
    Example:
        >>> results = {"fast": result1, "slow": result2}
        >>> chart = create_bar_chart(results, metric="mean", width=40)
        >>> print(chart)
        
        Bar Chart (mean)
        ================================================
        
        fast    ████████████  1.234ms
        slow    ████████████████████████  2.456ms
    """
    if not results:
        return "No results to display."
    
    # Normalize metric
    if metric == "min":
        metric = "min_time"
    elif metric == "max":
        metric = "max_time"
    
    # Get values
    values = [(name, getattr(results[name], metric)) for name in results.keys()]
    values.sort(key=lambda x: x[1])
    
    # Find max value for scaling
    max_value = max(v[1] for v in values)
    if max_value == 0:
        return "All values are zero."
    
    # Build chart
    lines = []
    lines.append("")
    lines.append(f"Bar Chart ({metric})")
    lines.append("=" * (width + 30))
    lines.append("")
    
    max_name_len = max(len(name) for name, _ in values)
    
    for name, value in values:
        bar_length = int((value / max_value) * width)
        bar = "█" * bar_length
        formatted_value = results[name].format_time(value)
        lines.append(f"{name:<{max_name_len}}  {bar}  {formatted_value}")
    
    lines.append("")
    
    return "\n".join(lines)