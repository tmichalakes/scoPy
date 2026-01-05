import unittest
from datetime import datetime, timezone
from RightAscension import calculate_out_vector_angle

class RightAscensionTests(unittest.TestCase):
    def assertAngleAlmostEqual(self, actual, expected, tolerance_deg=1.5):
        diff = abs(actual - expected)
        # Handle wrap-around at 360/0
        if actual + tolerance_deg > 360:
            wrapped_actual = actual - 360
            diff = abs(wrapped_actual - expected)
        # print(f"Actual: {actual:.2f}, Expected: {expected:.2f}, Difference: {abs(diff):.2f}° (Allowed: {tolerance_deg}°)")
        self.assertTrue(diff <= tolerance_deg,
                        f"{actual} != {expected} within {tolerance_deg} degrees tolerance")

    def test_calculate_out_vector_angle_spring_equinox(self):
        # print("Testing Spring Equinox")
        from RightAscension import calculate_out_vector_angle
        dt = datetime(2026, 3, 21, 0, 0, 0, tzinfo=timezone.utc)
        angle = calculate_out_vector_angle(dt)
        self.assertAngleAlmostEqual(angle, 180.0)

    def test_calculate_out_vector_angle_summer_solstice(self):
        # print("Testing Summer Solstice")
        from RightAscension import calculate_out_vector_angle
        dt = datetime(2026, 6, 21, 0, 0, 0, tzinfo=timezone.utc)
        angle = calculate_out_vector_angle(dt)
        self.assertAngleAlmostEqual(angle, 270.0)

    def test_calculate_out_vector_angle_autumn_equinox(self):
        # print("Testing Autumn Equinox")
        from RightAscension import calculate_out_vector_angle
        dt = datetime(2026, 9, 23, 0, 0, 0, tzinfo=timezone.utc)
        angle = calculate_out_vector_angle(dt)
        self.assertAngleAlmostEqual(angle, 0.0)

    def test_calculate_out_vector_angle_winter_solstice(self):
        # print("Testing Winter Solstice")
        from RightAscension import calculate_out_vector_angle
        dt = datetime(2026, 12, 21, 0, 0, 0, tzinfo=timezone.utc)
        angle = calculate_out_vector_angle(dt)
        self.assertAngleAlmostEqual(angle, 90.0)

    def test_angle_between_zenith_and_out_solar_9pm_solstices_equinox(self):
        from RightAscension import angle_between_zenith_and_out_solar
        from datetime import timezone, datetime
        # Dates for 9PM UTC for each event
        test_cases = [
            ("Spring Equinox", datetime(2026, 3, 21, 21, 0, 0, tzinfo=timezone.utc)),
            ("Summer Solstice", datetime(2026, 6, 21, 21, 0, 0, tzinfo=timezone.utc)),
            ("Autumn Equinox", datetime(2026, 9, 23, 21, 0, 0, tzinfo=timezone.utc)),
            ("Winter Solstice", datetime(2026, 12, 21, 21, 0, 0, tzinfo=timezone.utc)),
        ]
        for label, dt in test_cases:
            angle = angle_between_zenith_and_out_solar(dt)
            # print(f"{label} (UTC, 2026-{'%02d' % dt.month}-{'%02d' % dt.day} 21:00): {angle:.4f}° (Expected: ~-45°)")
            self.assertTrue(abs(angle + 45) < 2.0, f"Expected ~-45°, got {angle} for {label}")
        
    def test_angle_between_zenith_and_out_solar_2am_solstices_equinox(self):
        from RightAscension import angle_between_zenith_and_out_solar
        longitude = 0.0  # Use Greenwich/UTC for generality
        from datetime import timezone, datetime
        utc = timezone.utc
        # Dates for 2AM UTC for each event
        test_cases = [
            ("Spring Equinox", datetime(2026, 3, 21, 2, 0, 0, tzinfo=utc)),
            ("Summer Solstice", datetime(2026, 6, 21, 2, 0, 0, tzinfo=utc)),
            ("Autumn Equinox", datetime(2026, 9, 23, 2, 0, 0, tzinfo=utc)),
            ("Winter Solstice", datetime(2026, 12, 21, 2, 0, 0, tzinfo=utc)),
        ]
        for label, dt in test_cases:
            angle = angle_between_zenith_and_out_solar(dt)
            # print(f"{label} (UTC, 2026-{'%02d' % dt.month}-{'%02d' % dt.day} 02:00): {angle:.4f}° (Expected: ~+30°)")
            self.assertTrue(abs(angle - 30) < 2.0, f"Expected ~+30°, got {angle} for {label}")

    def test_angle_between_object_and_out(self):
        from RightAscension import angle_between_object_and_out, calculate_out_vector_angle
        from datetime import datetime, timezone
        dt = datetime(2026, 3, 21, 0, 0, 0, tzinfo=timezone.utc)

        # Case 1: object at same RA as out vector
        angle1 = angle_between_object_and_out(dt, "12h")
        # print(f"Object at out vector: {angle1:.2f}° (Expected: 0°)")
        self.assertTrue(abs(angle1) < 0.5, f"Expected 0°, got {angle1}")

        # Case 2: object at RA 9h (135°), should be -45° at vernal equinox (out vector at 180°)
        angle2 = angle_between_object_and_out(dt, "9h")
        # print(f"Object at RA 9h: {angle2:.2f}° (Expected: -45°)")
        self.assertTrue(abs(angle2 + 45) < 0.5, f"Expected -45°, got {angle2}")

    def test_angle_between_object_and_zenith_denver_9pm_ra13h(self):
        from RightAscension import angle_between_object_and_zenith
        from datetime import datetime, timedelta, timezone
        longitude = -104.9903
        # Denver local time (UTC-6 for simplicity)
        denver_tz = timezone(timedelta(hours=longitude / 15.0))
        dt = datetime(2026, 3, 21, 21, 0, 0, tzinfo=denver_tz)
        object_ra_str = "13h"
        angle = angle_between_object_and_zenith(dt, object_ra_str)
        # print(f"Denver 9PM, object RA 13h: {angle:.2f}° (Check expected value)")
        # No strict assertion, just print for manual inspection or future reference
        self.assertTrue(abs(angle - 60) < 2.0, f"Expected ~60°, got {angle}")

    def test_angle_between_object_and_zenith_various_ras(self):
        from RightAscension import angle_between_object_and_zenith
        from datetime import datetime, timedelta, timezone
        longitude = -104.9903
        denver_tz = timezone(timedelta(hours=-6))
        dt = datetime(2026, 3, 21, 21, 0, 0, tzinfo=denver_tz)
        # (RA string, expected angle)
        test_cases = [
            ("9h", 0),
            ("11h", 30),
            ("13h", 60),
            ("15h", 90),
            ("21h", 180),
        ]
        
        for ra_str, expected in test_cases:
            angle = angle_between_object_and_zenith(dt, ra_str)
            print(f"Denver 9PM, object RA {ra_str}: {angle:.2f}° (Expected: {expected}°)")
            self.assertTrue(abs(angle - expected) < 2.0, f"Expected {expected}°, got {angle} for RA {ra_str}")
    
if __name__ == '__main__':
    unittest.main()