# Pysyun ArithmeticTimeline

`ArithmeticTimeline` is a class that extends the functionality of `Chainable` to perform arithmetic operations on processed timeline data.

## Installation

```bash
pip install git+https://github.com/pysyun/pysyun_arithmetic_timeline.git
```

## Description

The class allows performing basic arithmetic operations (+, -, *, /) on the results of processing a single timeline with different processors. Within a single pipeline, all ArithmeticTimeline instances receive the same input timeline but process it using different processors, after which arithmetic operations are performed on these processing results. Each processing result is represented as a sequence of data points, where each point contains time and numeric value.

## Constructor

```python
def __init__(self, processor)
```

### Parameters:
- `processor`: Base processor for input data processing

## Main Methods

### process()

```python
def process(self, data)
```

Processes input data through the processor and performs all accumulated arithmetic operations.

#### Parameters:
- `data`: Input data for processing

#### Returns:
- List of dictionaries, where each dictionary contains 'time' and 'value' keys

#### Processing Features:
- If no operations are registered, returns the base processor's result
- Returns float('inf') when dividing by zero
- All values are converted to float before operations

### Arithmetic Operations

The class supports the following operations through standard Python operators:

- `__add__(self, other)`: Addition (`+`)
- `__sub__(self, other)`: Subtraction (`-`)
- `__mul__(self, other)`: Multiplication (`*`)
- `__truediv__(self, other)`: Division (`/`)

#### Operation Parameters:
- `other`: Another ArithmeticTimeline object

#### Returns:
- New ArithmeticTimeline object with the added operation

#### Exceptions:
- `TypeError`: If the operand is not an ArithmeticTimeline object

## Chainable Integration

### __or__()

```python
def __or__(self, other)
```

Provides compatibility with the processing chain system.

#### Parameters:
- `other`: Next processor in the chain

#### Returns:
- ChainableGroup if other is ChainableGroup
- Chainable with ChainedProcessor in other cases

## Usage Examples

```python
# Example 1: Simple difference between metrics
difference = (ArithmeticTimeline(ema) - ArithmeticTimeline(sma)).process(time_line)

# Example 2: Combining three metrics
combined = (ArithmeticTimeline(metric1) + ArithmeticTimeline(metric2) - ArithmeticTimeline(weight)).process(time_line)

# Example 3: Complex arithmetic operations
result = (
    ArithmeticTimeline(price) * ArithmeticTimeline(volume) / ArithmeticTimeline(total)
).process(time_line)

# Example 4: Using ChainableGroup for parallel processing
parallel_calc = (
    ChainableGroup(num_threads) 
    | (ArithmeticTimeline(metric1) + ArithmeticTimeline(metric2))
).process(time_lines)
```

## Notes

- Within a single pipeline, all ArithmeticTimeline instances work with the same input timeline
- Different results are achieved by using different processors to process this timeline
- Arithmetic operations are performed on the results of processing one timeline by different processors
- Operations are executed in the order they were added
- All arithmetic operations are performed pairwise for values with matching timestamps
- The class maintains immutability - each operation creates a new object

