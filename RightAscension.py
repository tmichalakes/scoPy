from datetime import datetime, timezone

EQUINOX_MONTH = 3
EQUINOX_DAY = 21

class RightAscension():
    def __init__(self, hours: float, minutes: float, seconds: float):
        self.hours = hours
        self.minutes = minutes
        self.seconds = seconds

    # Returns the current out RA in seconds - akin to the vector defined by the sun to the earth.
    # Corresponds to equatorial midnight Right ascension of 12H exactly on the vernal equinox and 
    # Corresponds to 
    def GetCurrentOutRADegrees(self) -> float:
        currentTime = datetime.now(timezone.utc)

        year = currentTime.year

        equinox = datetime(year, EQUINOX_MONTH, EQUINOX_DAY)
        
        # if we're in winter of the current year, we need to go back to the previous equinox
        if(equinox > currentTime):
            equinox = datetime(year - 1, EQUINOX_MONTH, EQUINOX_DAY)

        nextEquinox = datetime(equinox.year + 1, EQUINOX_MONTH, EQUINOX_DAY)

        totalYearSeconds = (nextEquinox - equinox).total_seconds()
        secondsSinceEquinox = (currentTime - equinox).total_seconds()

        return (secondsSinceEquinox / totalYearSeconds) * 360

    # provided a longitude (degrees), gives the exact solar time offset (in seconds) from UTC 0.0
    def GetSolarTimeMidnightOffsetSeconds(self, longitude: float) -> float:
        if longitude < -180.0 or longitude > 180.0:
            raise ValueError("Longitude must be between -180.0 and 180.0")
        
        longitude += 180 # convert longitude to be based on 360, 0 is the international date line
        
        return (longitude / 360.0) * (24 * 60 * 60)
    