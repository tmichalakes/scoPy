import unittest
from datetime import datetime, timezone
from RightAscension import calculate_out_vector_angle

class TestCalculateOutVectorAngle(unittest.TestCase):
    def assertAngleAlmostEqual(self, actual, expected, percent=5.0):
        tolerance = abs(expected) * percent / 100.0
        self.assertTrue(abs(actual - expected) <= tolerance,
                        f"{actual} != {expected} within {percent}% tolerance")

    def test_spring_equinox(self):
        dt = datetime(2026, 3, 21, 0, 0, 0, tzinfo=timezone.utc)
        angle = calculate_out_vector_angle(dt)
        self.assertAngleAlmostEqual(angle, 0.0)

    def test_summer_solstice(self):
        dt = datetime(2026, 6, 21, 0, 0, 0, tzinfo=timezone.utc)
        angle = calculate_out_vector_angle(dt)
        self.assertAngleAlmostEqual(angle, 90.0)

    def test_autumn_equinox(self):
        dt = datetime(2026, 9, 23, 0, 0, 0, tzinfo=timezone.utc)
        angle = calculate_out_vector_angle(dt)
        self.assertAngleAlmostEqual(angle, 180.0)

    def test_winter_solstice(self):
        dt = datetime(2026, 12, 21, 0, 0, 0, tzinfo=timezone.utc)
        angle = calculate_out_vector_angle(dt)
        self.assertAngleAlmostEqual(angle, 270.0)

if __name__ == "__main__":
    unittest.main()
