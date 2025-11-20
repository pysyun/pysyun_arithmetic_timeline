# Pysyun ArithmeticTimeline

ArithmeticTimeline is a tiny utility on top of pysyun_chain that lets you compose arithmetic expressions over multiple processors applied to the same input timeline. It evaluates those processors and combines the results point-by-point using standard arithmetic operators.

- Compose timelines with +, -, *, /
- Works with any processor that exposes process(data) -> [{"time": T, "value": number}, ...]
- Immutable operations (every +, -, *, / returns a new ArithmeticTimeline)
- Integrates with Chainable and ChainableGroup from pysyun_chain

## Installation

```bash
pip install git+https://github.com/pysyun/pysyun_arithmetic_timeline.git
```

Dependencies:
- pysyun_chain (fetched via Git)
- setuptools (for local packaging)

## Quick start

```python
from pysyun_arithmetic_timeline import ArithmeticTimeline

# Example processors that conform to the interface:
class EMA:
    def process(self, data):
        # return [{"time": ..., "value": ...}, ...]
        ...

class SMA:
    def process(self, data):
        ...

timeline = [...]  # your raw data for processors

diff = (ArithmeticTimeline(EMA()) - ArithmeticTimeline(SMA())).process(timeline)
print(diff)  # [{"time": t1, "value": v1}, {"time": t2, "value": v2}, ...]
```

## What it does

Within a single pipeline, all ArithmeticTimeline instances receive the same input data. Each instance wraps a processor and runs it on the input. Then ArithmeticTimeline combines the processed results point-by-point:

- Addition: value1 + value2
- Subtraction: value1 - value2
- Multiplication: value1 * value2
- Division: value1 / value2 (yields float("inf") when dividing by zero)

All values are coerced to float before operations.

## Interface

### Constructor

```python
ArithmeticTimeline(processor)
```

- processor: Any object with method process(data) that returns a list of dicts with keys "time" and "value".

### process

```python
result = ArithmeticTimeline(processor).process(data)
```

- data: Input passed to underlying processors.
- Returns: List[{"time": ..., "value": float}]

Behavior:
- If no arithmetic operations were composed, returns processor.process(data).
- For division by zero, result value is float("inf").
- Operations are executed in the order they were added.

### Arithmetic operators

```python
a + b
a - b
a * b
a / b
```

- a and b must be ArithmeticTimeline instances.
- Returns a new ArithmeticTimeline with the operation appended (immutability).

Raises:
- TypeError if the right-hand operand is not an ArithmeticTimeline.

### Chainable integration

ArithmeticTimeline is Chainable-compatible.

```python
# With ChainableGroup (parallel pipelines)
from pysyun_chain import ChainableGroup

parallel = ChainableGroup(num_threads) | (ArithmeticTimeline(p1) + ArithmeticTimeline(p2))
out = parallel.process([data1, data2, ...])
```

```python
# Chaining with another Chainable
# Note: __or__ composes processors; make sure it fits your pipeline design.
pipeline = (ArithmeticTimeline(p1) + ArithmeticTimeline(p2)) | other_chainable
out = pipeline.process(data)
```

Notes on __or__:
- If other is ChainableGroup, the group is configured to run this ArithmeticTimeline next.
- Otherwise, a Chainable is returned with a ChainedProcessor(self.processor, other.processor).
  In this case, only the wrapped processor is chained; the arithmetic composition remains on this node.

## Usage examples

- Simple difference between metrics

```python
difference = (ArithmeticTimeline(ema) - ArithmeticTimeline(sma)).process(time_line)
```

- Combining three metrics

```python
combined = (
    ArithmeticTimeline(metric1)
    + ArithmeticTimeline(metric2)
    - ArithmeticTimeline(weight)
).process(time_line)
```

- Complex arithmetic

```python
result = (
    ArithmeticTimeline(price) * ArithmeticTimeline(volume) / ArithmeticTimeline(total)
).process(time_line)
```

- Parallel processing with ChainableGroup

```python
from pysyun_chain import ChainableGroup

parallel_calc = (
    ChainableGroup(num_threads)
    | (ArithmeticTimeline(metric1) + ArithmeticTimeline(metric2))
).process(time_lines)
```

- Using constants (wrap a constant as a processor)

```python
class Const:
    def __init__(self, c): self.c = float(c)
    def process(self, data):
        # mirror input length and timestamps from another processor, if needed
        return [{"time": x["time"], "value": self.c} for x in data]

scale_by_2 = ArithmeticTimeline(source) * ArithmeticTimeline(Const(2.0))
out = scale_by_2.process(time_line)
```

## Assumptions and alignment

- All wrapped processors are run on the same data input.
- The results of all processors must:
  - Have the same length.
  - Be ordered in the same sequence.
  - Correspond one-to-one by index (and ideally by the same "time" values).
- ArithmeticTimeline performs pairwise operations by index and carries over the time from the left operand.

If your processors can produce different lengths or time grids, pre-align/normalize them before composing.

## Immutability and performance

- Each arithmetic operator returns a new ArithmeticTimeline; the original is unchanged.
- For N operations, ArithmeticTimeline currently re-runs the right-hand processors during evaluation.
  Complexity is roughly O(N * M), where M is the number of points. Consider caching upstream results if needed.

## Error handling

- Division by zero yields float("inf").
- Non-ArithmeticTimeline operands in +, -, *, / raise TypeError.
- All values are coerced to float prior to arithmetic.

## Running tests

```bash
# (optional) create and activate a virtual environment
pip install -r requirements.txt
python -m unittest
```

## Recent updates

- Package/module name aligned to pysyun_arithmetic_timeline with a single public class ArithmeticTimeline.
- Clarified alignment assumptions and division-by-zero behavior.
- Improved Chainable/ChainableGroup integration notes.
- Expanded examples and added guidance for using constants.

