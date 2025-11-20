import unittest
import math
from pysyun_arithmetic_timeline import ArithmeticTimeline


class TimeLineSource:
    def process(self, data):
        return [
            {"time": 1, "value": 0.05},
            {"time": 2, "value": 0.02},
        ]


class ZeroSource:
    def process(self, data):
        return [
            {"time": 1, "value": 0.0},
            {"time": 2, "value": 0.0},
        ]


class NegativeSource:
    def process(self, data):
        return [
            {"time": 1, "value": -0.05},
            {"time": 2, "value": -0.02},
        ]


class TestMathUtils(unittest.TestCase):

    def assertTimelineAlmostEqual(self, result, expected, places=7):
        self.assertEqual(len(result), len(expected), "Timelines lengths differ")
        for i, (r, e) in enumerate(zip(result, expected)):
            self.assertEqual(r["time"], e["time"], f"Time mismatch at index {i}")
            self.assertAlmostEqual(float(r["value"]), float(e["value"]), places=places,
                                   msg=f"Value mismatch at index {i}")

    def test_add_with_positive_numbers(self):
        operation = ArithmeticTimeline(TimeLineSource()) + ArithmeticTimeline(TimeLineSource())
        result = operation.process([])

        expected = [
            {"time": 1, "value": 0.05 + 0.05},
            {"time": 2, "value": 0.02 + 0.02},
        ]
        self.assertTimelineAlmostEqual(result, expected)

    def test_add_with_zero(self):
        operation = ArithmeticTimeline(TimeLineSource()) + ArithmeticTimeline(ZeroSource())
        result = operation.process([])

        expected = [
            {"time": 1, "value": 0.05},
            {"time": 2, "value": 0.02},
        ]
        self.assertTimelineAlmostEqual(result, expected)

    def test_add_with_negative_numbers(self):
        operation = ArithmeticTimeline(TimeLineSource()) + ArithmeticTimeline(NegativeSource())
        result = operation.process([])

        expected = [
            {"time": 1, "value": 0.0},
            {"time": 2, "value": 0.0},
        ]
        self.assertTimelineAlmostEqual(result, expected)

    def test_divide_normal(self):
        operation = ArithmeticTimeline(TimeLineSource()) / ArithmeticTimeline(TimeLineSource())
        result = operation.process([])

        expected = [
            {"time": 1, "value": 1.0},
            {"time": 2, "value": 1.0},
        ]
        self.assertTimelineAlmostEqual(result, expected)

    def test_divide_by_zero(self):
        operation = ArithmeticTimeline(TimeLineSource()) / ArithmeticTimeline(ZeroSource())
        result = operation.process([])

        self.assertEqual(len(result), 2)
        for i, entry in enumerate(result):
            self.assertEqual(entry["time"], i + 1)
            self.assertTrue(math.isinf(entry["value"]), f"Expected infinity at index {i}, got {entry['value']}")


if __name__ == "__main__":
    unittest.main()
