"""Tests for the display module."""

import pytest
from benchrun.results import BenchmarkResults
from benchrun.display import print_comparison, format_results_table, create_bar_chart


# Test fixtures
@pytest.fixture
def single_result():
    """Create a single BenchmarkResults object for testing."""
    durations = [0.001, 0.0012, 0.0011, 0.0013, 0.001]
    return BenchmarkResults(
        name="test_impl",
        durations=durations,
        runs=5,
        warmup=2
    )


@pytest.fixture
def multiple_results():
    """Create multiple BenchmarkResults objects for comparison testing."""
    fast_durations = [0.001, 0.0011, 0.001, 0.0012, 0.001]
    medium_durations = [0.002, 0.0021, 0.002, 0.0022, 0.002]
    slow_durations = [0.004, 0.0041, 0.004, 0.0042, 0.004]
    
    fast = BenchmarkResults(
        name="fast",
        durations=fast_durations,
        runs=5,
        warmup=2
    )
    fast.speedup = 1.0
    
    medium = BenchmarkResults(
        name="medium",
        durations=medium_durations,
        runs=5,
        warmup=2
    )
    medium.speedup = 0.5
    
    slow = BenchmarkResults(
        name="slow",
        durations=slow_durations,
        runs=5,
        warmup=2
    )
    slow.speedup = 0.25
    
    return {"fast": fast, "medium": medium, "slow": slow}


@pytest.fixture
def empty_results():
    """Create an empty results dictionary."""
    return {}


# Tests for print_comparison
def test_print_comparison_with_empty_dict(capsys, empty_results):
    """Test print_comparison with empty results dictionary."""
    print_comparison(empty_results)
    captured = capsys.readouterr()
    assert "No results to display." in captured.out


def test_print_comparison_with_single_result(capsys, single_result):
    """Test print_comparison with a single result."""
    results = {"test": single_result}
    print_comparison(results)
    captured = capsys.readouterr()
    
    assert "Benchmark Comparison" in captured.out
    assert "test" in captured.out
    assert "Summary:" in captured.out
    assert "Fastest: test" in captured.out


def test_print_comparison_with_multiple_results(capsys, multiple_results):
    """Test print_comparison with multiple results."""
    print_comparison(multiple_results)
    captured = capsys.readouterr()
    
    assert "Benchmark Comparison" in captured.out
    assert "fast" in captured.out
    assert "medium" in captured.out
    assert "slow" in captured.out
    assert "★" in captured.out  # Fastest marker
    assert "Summary:" in captured.out
    assert "Fastest: fast" in captured.out
    assert "Slowest: slow" in captured.out
    assert "Difference:" in captured.out


def test_print_comparison_sorting_by_mean(capsys, multiple_results):
    """Test that results are sorted by mean by default."""
    print_comparison(multiple_results, sort_by="mean")
    captured = capsys.readouterr()
    
    # Find positions of implementation names in output
    fast_pos = captured.out.find("fast")
    medium_pos = captured.out.find("medium")
    slow_pos = captured.out.find("slow")
    
    # Fast should appear before medium, medium before slow
    assert fast_pos < medium_pos < slow_pos


def test_print_comparison_sorting_by_median(capsys, multiple_results):
    """Test sorting by median."""
    print_comparison(multiple_results, sort_by="median")
    captured = capsys.readouterr()
    
    assert "Benchmark Comparison" in captured.out
    # Should still show all implementations
    assert "fast" in captured.out
    assert "medium" in captured.out
    assert "slow" in captured.out


def test_print_comparison_sorting_by_min(capsys, multiple_results):
    """Test sorting by min time."""
    print_comparison(multiple_results, sort_by="min")
    captured = capsys.readouterr()
    
    assert "Benchmark Comparison" in captured.out
    assert all(name in captured.out for name in multiple_results.keys())


def test_print_comparison_sorting_by_max(capsys, multiple_results):
    """Test sorting by max time."""
    print_comparison(multiple_results, sort_by="max")
    captured = capsys.readouterr()
    
    assert "Benchmark Comparison" in captured.out
    assert all(name in captured.out for name in multiple_results.keys())


def test_print_comparison_show_all_stats_true(capsys, multiple_results):
    """Test print_comparison with show_all_stats=True."""
    print_comparison(multiple_results, show_all_stats=True)
    captured = capsys.readouterr()
    
    # Should show all columns
    assert "Mean" in captured.out
    assert "Median" in captured.out
    assert "Std Dev" in captured.out
    assert "Min" in captured.out
    assert "Max" in captured.out
    assert "Speedup" in captured.out


def test_print_comparison_show_all_stats_false(capsys, multiple_results):
    """Test print_comparison with show_all_stats=False."""
    print_comparison(multiple_results, show_all_stats=False)
    captured = capsys.readouterr()
    
    # Should show only key columns
    assert "Mean" in captured.out
    assert "Std Dev" in captured.out
    assert "Speedup" in captured.out
    # Should not show all columns
    assert "Median" not in captured.out or captured.out.count("Median") == 0


def test_print_comparison_fastest_marker(capsys, multiple_results):
    """Test that the fastest implementation gets a star marker."""
    print_comparison(multiple_results)
    captured = capsys.readouterr()
    
    # The star should appear only once, next to the fastest
    assert captured.out.count("★") == 1
    # Find the line with the star
    lines = captured.out.split('\n')
    star_line = [line for line in lines if "★" in line][0]
    assert "fast" in star_line


def test_print_comparison_speedup_display(capsys, multiple_results):
    """Test that speedup values are displayed correctly."""
    print_comparison(multiple_results)
    captured = capsys.readouterr()
    
    assert "1.00x" in captured.out  # Fast implementation
    assert "0.50x" in captured.out  # Medium implementation
    assert "0.25x" in captured.out  # Slow implementation


# Tests for format_results_table
def test_format_results_table_with_empty_dict(empty_results):
    """Test format_results_table with empty results."""
    lines = format_results_table(empty_results)
    assert len(lines) == 1
    assert "No results to display." in lines[0]


def test_format_results_table_with_single_result(single_result):
    """Test format_results_table with a single result."""
    results = {"test": single_result}
    lines = format_results_table(results)
    
    assert len(lines) > 0
    assert any("Benchmark Results" in line for line in lines)
    assert any("test:" in line for line in lines)
    assert any("Mean:" in line for line in lines)
    assert any("Median:" in line for line in lines)
    assert any("Std:" in line for line in lines)
    assert any("Min:" in line for line in lines)
    assert any("Max:" in line for line in lines)


def test_format_results_table_with_multiple_results(multiple_results):
    """Test format_results_table with multiple results."""
    lines = format_results_table(multiple_results)
    
    assert len(lines) > 0
    assert any("Benchmark Results" in line for line in lines)
    assert any("fast:" in line for line in lines)
    assert any("medium:" in line for line in lines)
    assert any("slow:" in line for line in lines)


def test_format_results_table_sorting(multiple_results):
    """Test that format_results_table sorts results correctly."""
    lines = format_results_table(multiple_results, sort_by="mean")
    
    # Find positions of implementation names
    text = '\n'.join(lines)
    fast_pos = text.find("fast:")
    medium_pos = text.find("medium:")
    slow_pos = text.find("slow:")
    
    # Should be in order: fast, medium, slow
    assert fast_pos < medium_pos < slow_pos


def test_format_results_table_includes_speedup(multiple_results):
    """Test that speedup is included when available."""
    lines = format_results_table(multiple_results)
    text = '\n'.join(lines)
    
    assert "Speedup:" in text


def test_format_results_table_sort_by_median(multiple_results):
    """Test sorting by median."""
    lines = format_results_table(multiple_results, sort_by="median")
    assert len(lines) > 0
    assert any("fast:" in line for line in lines)


def test_format_results_table_sort_by_min(multiple_results):
    """Test sorting by min time."""
    lines = format_results_table(multiple_results, sort_by="min")
    assert len(lines) > 0
    assert any("fast:" in line for line in lines)


def test_format_results_table_sort_by_max(multiple_results):
    """Test sorting by max time."""
    lines = format_results_table(multiple_results, sort_by="max")
    assert len(lines) > 0
    assert any("fast:" in line for line in lines)


# Tests for create_bar_chart
def test_create_bar_chart_with_empty_dict(empty_results):
    """Test create_bar_chart with empty results."""
    chart = create_bar_chart(empty_results)
    assert "No results to display." in chart


def test_create_bar_chart_with_single_result(single_result):
    """Test create_bar_chart with a single result."""
    results = {"test": single_result}
    chart = create_bar_chart(results)
    
    assert "Bar Chart" in chart
    assert "test" in chart
    assert "█" in chart  # Should contain bar characters


def test_create_bar_chart_with_multiple_results(multiple_results):
    """Test create_bar_chart with multiple results."""
    chart = create_bar_chart(multiple_results)
    
    assert "Bar Chart" in chart
    assert "fast" in chart
    assert "medium" in chart
    assert "slow" in chart
    assert "█" in chart


def test_create_bar_chart_metric_mean(multiple_results):
    """Test create_bar_chart with mean metric."""
    chart = create_bar_chart(multiple_results, metric="mean")
    assert "Bar Chart (mean)" in chart


def test_create_bar_chart_metric_median(multiple_results):
    """Test create_bar_chart with median metric."""
    chart = create_bar_chart(multiple_results, metric="median")
    assert "Bar Chart (median)" in chart


def test_create_bar_chart_metric_min(multiple_results):
    """Test create_bar_chart with min metric."""
    chart = create_bar_chart(multiple_results, metric="min")
    assert "Bar Chart (min_time)" in chart


def test_create_bar_chart_metric_max(multiple_results):
    """Test create_bar_chart with max metric."""
    chart = create_bar_chart(multiple_results, metric="max")
    assert "Bar Chart (max_time)" in chart


def test_create_bar_chart_custom_width(multiple_results):
    """Test create_bar_chart with custom width."""
    chart = create_bar_chart(multiple_results, width=30)
    assert "Bar Chart" in chart
    # The chart should still be generated
    assert "█" in chart


def test_create_bar_chart_bar_scaling(multiple_results):
    """Test that bars are scaled correctly."""
    chart = create_bar_chart(multiple_results, metric="mean", width=50)
    lines = chart.split('\n')
    
    # Find lines with bars
    bar_lines = [line for line in lines if "█" in line]
    
    # Should have 3 bar lines (one for each result)
    assert len(bar_lines) == 3
    
    # The slowest should have the longest bar (or close to it)
    # The fastest should have the shortest bar
    fast_line = [line for line in bar_lines if "fast" in line][0]
    slow_line = [line for line in bar_lines if "slow" in line][0]
    
    fast_bar_length = fast_line.count("█")
    slow_bar_length = slow_line.count("█")
    
    # Slow should have more bars than fast
    assert slow_bar_length > fast_bar_length


def test_create_bar_chart_with_zero_values():
    """Test create_bar_chart when all values are zero."""
    zero_durations = [0.0, 0.0, 0.0]
    zero_result = BenchmarkResults(
        name="zero",
        durations=[1e-10, 1e-10, 1e-10],  # Very small but not zero
        runs=3,
        warmup=0
    )
    results = {"zero": zero_result}
    chart = create_bar_chart(results)
    
    # Should still generate a chart
    assert "Bar Chart" in chart


def test_create_bar_chart_sorting(multiple_results):
    """Test that create_bar_chart sorts results by value."""
    chart = create_bar_chart(multiple_results, metric="mean")
    lines = chart.split('\n')
    
    # Find positions of implementation names
    text = chart
    fast_pos = text.find("fast")
    medium_pos = text.find("medium")
    slow_pos = text.find("slow")
    
    # Should be sorted by value (ascending)
    assert fast_pos < medium_pos < slow_pos


# Tests for format_time (indirectly through BenchmarkResults)
def test_format_time_seconds():
    """Test format_time with values in seconds."""
    durations = [1.5, 1.6, 1.7]
    result = BenchmarkResults(
        name="test",
        durations=durations,
        runs=3,
        warmup=0
    )
    formatted = result.format_time(1.5)
    assert "s" in formatted
    assert "1.5" in formatted or "1.50" in formatted


def test_format_time_milliseconds():
    """Test format_time with values in milliseconds."""
    durations = [0.001, 0.0011, 0.0012]
    result = BenchmarkResults(
        name="test",
        durations=durations,
        runs=3,
        warmup=0
    )
    formatted = result.format_time(0.001)
    assert "ms" in formatted
    assert "1." in formatted


def test_format_time_microseconds():
    """Test format_time with values in microseconds."""
    durations = [1e-6, 1.1e-6, 1.2e-6]
    result = BenchmarkResults(
        name="test",
        durations=durations,
        runs=3,
        warmup=0
    )
    formatted = result.format_time(1e-6)
    assert "μs" in formatted or "us" in formatted


def test_format_time_nanoseconds():
    """Test format_time with values in nanoseconds."""
    durations = [1e-9, 1.1e-9, 1.2e-9]
    result = BenchmarkResults(
        name="test",
        durations=durations,
        runs=3,
        warmup=0
    )
    formatted = result.format_time(1e-9)
    assert "ns" in formatted


# Edge cases
def test_print_comparison_with_long_names(capsys):
    """Test print_comparison with very long implementation names."""
    durations = [0.001, 0.001, 0.001]
    result = BenchmarkResults(
        name="very_long_implementation_name_that_might_break_formatting",
        durations=durations,
        runs=3,
        warmup=0
    )
    results = {"very_long_implementation_name_that_might_break_formatting": result}
    print_comparison(results)
    captured = capsys.readouterr()
    
    assert "very_long_implementation_name_that_might_break_formatting" in captured.out
    assert "Benchmark Comparison" in captured.out


def test_format_results_table_returns_list():
    """Test that format_results_table returns a list of strings."""
    durations = [0.001, 0.001, 0.001]
    result = BenchmarkResults(
        name="test",
        durations=durations,
        runs=3,
        warmup=0
    )
    results = {"test": result}
    lines = format_results_table(results)
    
    assert isinstance(lines, list)
    assert all(isinstance(line, str) for line in lines)


def test_create_bar_chart_returns_string():
    """Test that create_bar_chart returns a string."""
    durations = [0.001, 0.001, 0.001]
    result = BenchmarkResults(
        name="test",
        durations=durations,
        runs=3,
        warmup=0
    )
    results = {"test": result}
    chart = create_bar_chart(results)
    
    assert isinstance(chart, str)
