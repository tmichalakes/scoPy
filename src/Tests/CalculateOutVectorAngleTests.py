import unittest
from datetime import datetime, timezone
from Astromath.RightAscension import CalculateOutVectorAngle

class TestCalculateOutVectorAngle(unittest.TestCase):
    def assertAngleAlmostEqual(self, actual, expected, degreeTolerance=5.0):
        diff1 = abs(actual - expected)
        diff2 = abs(actual - (expected + 360))
        self.assertTrue(
            diff1 <= degreeTolerance or diff2 <= degreeTolerance,
            f"{actual} != {expected} (diff={diff1}) or {expected}+360 (diff={diff2}) within {degreeTolerance} degrees tolerance"
        )

    def test_spring_equinox(self):
        dt = datetime(2026, 3, 21, 0, 0, 0, tzinfo=timezone.utc)
        angle = CalculateOutVectorAngle(dt)
        self.assertAngleAlmostEqual(angle, 180.0)

    def test_summer_solstice(self):
        dt = datetime(2026, 6, 21, 0, 0, 0, tzinfo=timezone.utc)
        angle = CalculateOutVectorAngle(dt)
        self.assertAngleAlmostEqual(angle, 270.0)

    def test_autumn_equinox(self):
        dt = datetime(2026, 9, 23, 0, 0, 0, tzinfo=timezone.utc)
        angle = CalculateOutVectorAngle(dt)
        self.assertAngleAlmostEqual(angle, 0.0)

    def test_winter_solstice(self):
        dt = datetime(2026, 12, 21, 0, 0, 0, tzinfo=timezone.utc)
        angle = CalculateOutVectorAngle(dt)
        self.assertAngleAlmostEqual(angle, 90.0)

if __name__ == "__main__":
    unittest.main()
