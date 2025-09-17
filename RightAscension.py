from datetime import datetime, timezone, timedelta

EQUINOX_MONTH = 3
EQUINOX_DAY = 21
ONE_DAY = timedelta(days=1)
MST_OFFSET_HOURS = -7.0

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

    # Gets the current offset in degrees between
    # TZ-midnight and solar midnight
    def GetCurrentSolarOffsetDegrees(self, longitude: float, timezoneOffset: float) -> float:
        tz = timezone(timezoneOffset)
        currentTime = datetime.now(tz)
        tomorrow = currentTime + ONE_DAY

        totalSeconds = (tomorrow - currentTime).total_seconds()

        midnight = datetime(currentTime.year, currentTime.month, currentTime.day, 0, 0, 0)
        if(currentTime.hour > 12):
            midnight += ONE_DAY
    
        timeToMidnight = midnight - currentTime
        solarTimeOffset = self.CurrentLocalSolarOffsetSeconds(longitude, timezoneOffset)

        return (timeToMidnight - solarTimeOffset) * (360.0 / totalSeconds)

    # gets the difference in seconds between
    # the local time (based on time zone) and the solar time
    # based on longitude
    def CurrentLocalSolarOffsetSeconds(self, longitude: float, timezoneOffset: float) -> float:
        currentTime = datetime.now(timezone.utc)
        tomorrow = currentTime + ONE_DAY

        totalSeconds = (tomorrow - currentTime).total_seconds()

        timezone_seconds = (timezoneOffset / 24.0) * totalSeconds
        solar_seconds = (longitude / 360.0) * totalSeconds

        return timezone_seconds - solar_seconds