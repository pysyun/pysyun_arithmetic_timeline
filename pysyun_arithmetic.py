from pysyun_chain import Chainable, ChainedProcessor, ChainableGroup


class ArithmeticTimeline(Chainable):
    def __init__(self, processor):
        super().__init__(processor)
        self.operations = []  # List of (operation, timeline) tuples

    def process(self, data):
        # Process the input data through the wrapped processor
        result = self.processor.process(data)

        # If there are no arithmetic operations to perform, return processed data
        if not self.operations:
            return result

        # Process each operation in sequence
        for operation, other_timeline in self.operations:
            other_processed = other_timeline.processor.process(data)

            # Perform the arithmetic operation
            new_result = []
            for i in range(len(result)):
                time = result[i]['time']
                value1 = float(result[i]['value'])
                value2 = float(other_processed[i]['value'])

                if operation == '+':
                    new_value = value1 + value2
                elif operation == '-':
                    new_value = value1 - value2
                elif operation == '*':
                    new_value = value1 * value2
                elif operation == '/':
                    new_value = value1 / value2 if value2 != 0 else float('inf')

                new_result.append({'time': time, 'value': new_value})

            result = new_result

        return result

    def _add_operation(self, operation, other):
        if isinstance(other, ArithmeticTimeline):
            result = ArithmeticTimeline(self.processor)
            # Copy existing operations
            result.operations = self.operations.copy()
            # Add new operation
            result.operations.append((operation, other))
            return result
        raise TypeError("Unsupported operand type")

    def __add__(self, other):
        return self._add_operation('+', other)

    def __sub__(self, other):
        return self._add_operation('-', other)

    def __mul__(self, other):
        return self._add_operation('*', other)

    def __truediv__(self, other):
        return self._add_operation('/', other)

    def __or__(self, other):
        # Preserve the chainable behavior
        if isinstance(other, ChainableGroup):
            other.next_processor = self
            return other
        return Chainable(ChainedProcessor(self.processor, other.processor))