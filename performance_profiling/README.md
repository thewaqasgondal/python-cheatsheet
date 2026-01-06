# Performance Profiling Examples

This directory contains comprehensive examples of performance profiling and optimization techniques in Python.

## Files

- `cpu_memory_profiling.py` - Complete performance profiling tutorial covering CPU and memory analysis

## Prerequisites

```bash
pip install psutil>=5.8.0
pip install numpy>=1.21.0
# Optional for enhanced profiling:
pip install line_profiler>=3.5.0  # For line-by-line profiling
pip install memory_profiler>=0.60.0  # For detailed memory profiling
```

## Topics Covered

### cpu_memory_profiling.py

#### CPU Profiling with cProfile
- Profiling recursive vs memoized vs iterative algorithms
- Analyzing function call statistics
- Identifying performance bottlenecks
- Interpreting profiling output

#### Precise Timing with timeit
- Comparing algorithm implementations
- Measuring small code snippets
- Benchmarking with proper setup
- Statistical timing analysis

#### Memory Profiling
- Using tracemalloc for memory tracing
- System memory monitoring with psutil
- Memory usage over time
- Identifying memory leaks

#### Optimization Techniques
- List comprehensions vs traditional loops
- NumPy vectorization benefits
- String concatenation optimization
- Efficient data structure usage

#### Profiling Decorators
- Timing function execution
- Memory usage measurement
- Combining multiple profilers

#### Line-by-Line Profiling
- Installing and using line_profiler
- Detailed function analysis
- Identifying slow lines of code

## Running the Examples

```bash
python performance_profiling/cpu_memory_profiling.py
```

## Key Concepts

- **cProfile**: Deterministic CPU profiler for function-level analysis
- **timeit**: Precise timing for benchmarking code snippets
- **tracemalloc**: Memory allocation tracing
- **psutil**: System and process monitoring
- **line_profiler**: Line-by-line execution time analysis
- **Optimization**: Vectorization, caching, efficient algorithms

## Profiling Best Practices

1. **Profile before optimizing**: Use data to identify real bottlenecks
2. **Use appropriate tools**: Different profilers for different needs
3. **Measure multiple runs**: Account for variability and warm-up effects
4. **Profile realistic data**: Use production-like datasets
5. **Consider trade-offs**: Optimization may affect readability/maintainability

## Common Profiling Commands

```bash
# Basic cProfile usage
python -m cProfile script.py

# Save profile data
python -m cProfile -o profile.prof script.py

# Analyze saved profile
python -c "import pstats; pstats.Stats('profile.prof').sort_stats('cumulative').print_stats()"

# Line profiling
kernprof -l script.py
python -m line_profiler script.py.lprof

# Memory profiling
python -m memory_profiler script.py
```

## Performance Optimization Tips

- **Algorithm choice**: O(n²) vs O(n log n) can make orders of magnitude difference
- **Data structures**: Lists vs sets vs dicts for different access patterns
- **Vectorization**: Use NumPy for numerical operations
- **Caching**: @lru_cache for expensive computations
- **Lazy evaluation**: Generators instead of lists for large datasets
- **String operations**: join() instead of concatenation in loops