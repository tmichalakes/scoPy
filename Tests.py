import unittest
from RightAscension import RightAscension, MST_OFFSET_HOURS

SECONDS_OFFSET = 335.0
LATITUDE = 40.0000
LONGITUDE = -106.3993

class RightAscensionTests(unittest.TestCase): 
    def test_ConfirmOffsetSeconds(self):
        ra = RightAscension(0, 0, 0)
        offsetSeconds = ra.CurrentLocalSolarOffsetSeconds(LONGITUDE, MST_OFFSET_HOURS)

        percentOff = 100 * abs((SECONDS_OFFSET - offsetSeconds) / SECONDS_OFFSET)

        print(f"Percent off: {percentOff}%")

        self.assertLessEqual(percentOff, 0.5)

if __name__ == '__main__':
    unittest.main()