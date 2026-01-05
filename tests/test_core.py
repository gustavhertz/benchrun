"""Tests for the core benchmarking functionality."""

import time
import pytest
from benchrun.core import benchmark


# Test fixtures
@pytest.fixture
def simple_func():
    """A simple function for testing."""
    def func():
        return sum(range(100))
    return func


@pytest.fixture
def sleep_func():
    """A function that sleeps for a known duration."""
    def func():
        time.sleep(0.01)  # 10ms
    return func


# Basic functionality tests
def test_benchmark_returns_correct_number_of_results(simple_func):
    """Test that benchmark returns the correct number of results."""
    runs = 10
    durations = benchmark(simple_func, runs=runs)
    assert len(durations) == runs


def test_benchmark_returns_positive_floats(simple_func):
    """Test that all returned values are positive floats."""
    durations = benchmark(simple_func, runs=5)
    assert all(isinstance(d, float) for d in durations)
    assert all(d > 0 for d in durations)


def test_benchmark_with_different_runs_counts(simple_func):
    """Test benchmark with various run counts."""
    for runs in [1, 5, 10, 50, 100]:
        durations = benchmark(simple_func, runs=runs)
        assert len(durations) == runs


# Warmup tests
def test_warmup_does_not_affect_result_count(simple_func):
    """Test that warmup runs don't affect the number of results."""
    runs = 10
    warmup = 5
    durations = benchmark(simple_func, runs=runs, warmup=warmup)
    assert len(durations) == runs  # Should only return timed runs


def test_benchmark_with_zero_warmup(simple_func):
    """Test that zero warmup works correctly."""
    durations = benchmark(simple_func, runs=10, warmup=0)
    assert len(durations) == 10


def test_benchmark_with_warmup(simple_func):
    """Test that warmup parameter is accepted and doesn't break functionality."""
    durations = benchmark(simple_func, runs=10, warmup=5)
    assert len(durations) == 10
    assert all(d > 0 for d in durations)


# Different callable types
def test_benchmark_with_lambda():
    """Test benchmarking a lambda function."""
    durations = benchmark(lambda: sum(range(100)), runs=5)
    assert len(durations) == 5
    assert all(d > 0 for d in durations)


def test_benchmark_with_builtin_function():
    """Test benchmarking a built-in function."""
    test_list = list(range(1000))
    durations = benchmark(lambda: sorted(test_list), runs=5)
    assert len(durations) == 5
    assert all(d > 0 for d in durations)


def test_benchmark_with_method():
    """Test benchmarking a method."""
    class TestClass:
        def method(self):
            return sum(range(100))
    
    obj = TestClass()
    durations = benchmark(obj.method, runs=5)
    assert len(durations) == 5
    assert all(d > 0 for d in durations)


# Timing accuracy tests
def test_timing_accuracy_with_sleep(sleep_func):
    """Test that timing is reasonably accurate using sleep."""
    durations = benchmark(sleep_func, runs=3)
    
    # Each duration should be close to 10ms (0.01s)
    # Allow for some overhead and timing variance (8ms to 15ms)
    for duration in durations:
        assert 0.008 < duration < 0.015, f"Duration {duration} outside expected range"


def test_timing_consistency(simple_func):
    """Test that multiple runs produce consistent timing results."""
    durations = benchmark(simple_func, runs=20, warmup=5)
    
    # Calculate coefficient of variation (std/mean)
    # Should be relatively small for consistent measurements
    mean = sum(durations) / len(durations)
    variance = sum((d - mean) ** 2 for d in durations) / len(durations)
    std_dev = variance ** 0.5
    cv = std_dev / mean if mean > 0 else 0
    
    # Coefficient of variation should be reasonable (less than 50%)
    assert cv < 0.5, f"Timing too inconsistent: CV={cv}"


# Input validation tests
def test_non_callable_raises_type_error():
    """Test that passing a non-callable raises TypeError."""
    with pytest.raises(TypeError, match="func must be callable"):
        benchmark("not a function", runs=10)
    
    with pytest.raises(TypeError, match="func must be callable"):
        benchmark(123, runs=10)
    
    with pytest.raises(TypeError, match="func must be callable"):
        benchmark(None, runs=10)


def test_invalid_runs_raises_value_error(simple_func):
    """Test that invalid runs parameter raises ValueError."""
    with pytest.raises(ValueError, match="runs must be a positive integer"):
        benchmark(simple_func, runs=0)
    
    with pytest.raises(ValueError, match="runs must be a positive integer"):
        benchmark(simple_func, runs=-1)
    
    with pytest.raises(ValueError, match="runs must be a positive integer"):
        benchmark(simple_func, runs=-10)


def test_invalid_warmup_raises_value_error(simple_func):
    """Test that invalid warmup parameter raises ValueError."""
    with pytest.raises(ValueError, match="warmup must be a non-negative integer"):
        benchmark(simple_func, runs=10, warmup=-1)
    
    with pytest.raises(ValueError, match="warmup must be a non-negative integer"):
        benchmark(simple_func, runs=10, warmup=-5)


def test_non_integer_runs_raises_error(simple_func):
    """Test that non-integer runs parameter raises ValueError."""
    with pytest.raises(ValueError):
        benchmark(simple_func, runs=10.5)
    
    with pytest.raises(ValueError):
        benchmark(simple_func, runs="10")


def test_non_integer_warmup_raises_error(simple_func):
    """Test that non-integer warmup parameter raises ValueError."""
    with pytest.raises(ValueError):
        benchmark(simple_func, runs=10, warmup=5.5)
    
    with pytest.raises(ValueError):
        benchmark(simple_func, runs=10, warmup="5")


# Edge cases
def test_single_run(simple_func):
    """Test benchmark with a single run."""
    durations = benchmark(simple_func, runs=1)
    assert len(durations) == 1
    assert durations[0] > 0


def test_large_number_of_runs(simple_func):
    """Test benchmark with a large number of runs."""
    runs = 1000
    durations = benchmark(simple_func, runs=runs)
    assert len(durations) == runs
    assert all(d > 0 for d in durations)


def test_function_with_no_operations():
    """Test benchmarking a function that does nothing."""
    def empty_func():
        pass
    
    durations = benchmark(empty_func, runs=10)
    assert len(durations) == 10
    # Even empty function should have some measurable time
    assert all(d >= 0 for d in durations)


def test_function_that_returns_value(simple_func):
    """Test that function return values don't affect benchmarking."""
    durations = benchmark(simple_func, runs=5)
    assert len(durations) == 5
    # The function returns a value, but benchmark should still work
    assert all(d > 0 for d in durations)


# Integration test
def test_complete_benchmark_workflow():
    """Test a complete benchmarking workflow."""
    def test_func():
        return sum(i ** 2 for i in range(100))
    
    # Run benchmark with warmup
    durations = benchmark(test_func, runs=50, warmup=10)
    
    # Verify results
    assert len(durations) == 50
    assert all(isinstance(d, float) for d in durations)
    assert all(d > 0 for d in durations)
    
    # Calculate statistics
    min_time = min(durations)
    max_time = max(durations)
    avg_time = sum(durations) / len(durations)
    
    assert min_time <= avg_time <= max_time
    assert max_time < 1.0  # Should complete in less than 1 second
