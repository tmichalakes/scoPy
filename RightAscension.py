from astropy.coordinates import get_sun
from astropy.time import Time
import astropy.units as UNITS
from datetime import datetime
from astropy.coordinates import Angle

def calculate_out_vector_angle(date_time: datetime) -> float:
    """
    Calculates the angle (in degrees) of the OUT vector (Sun-Earth line) for a given datetime.
    The angle is measured as the Sun's right ascension (RA), pointing 180 degrees opposite the Sun.
    :param date_time: The date and time for which to calculate the OUT vector angle
    :type date_time: datetime
    :return: The OUT vector angle in degrees
    :rtype: float
    """
    t = Time(date_time)
    sun = get_sun(t)
    # Use the Sun's right ascension, add 180 to point the opposite direction, normalize to [0, 360)
    angle_deg = (sun.ra.deg + 180) % 360
    return angle_deg

def angle_between_zenith_and_out_solar(date_time: datetime) -> float:
    """
    Computes the angle (in degrees) between the zenith and the out vector using the offset from local solar midnight,
    scaled by the length of a sidereal day. Positive if before solar midnight, negative if after.
    :param date_time: The date and time for calculation (timezone-aware, timezone is assumed to be the locale!)
    :return: Angle in degrees
    """
    # Length of a sidereal day in seconds
    SIDEREAL_DAY_SEC = 86164.0905

    # Use the timezone from the input datetime
    tzinfo = date_time.tzinfo
    # Local solar midnight in the same tz as input
    local_midnight = datetime.combine(date_time.date(), datetime.min.time(), tzinfo=tzinfo)
    # Compute offset in seconds from local solar midnight
    offset_sec = (date_time - local_midnight).total_seconds()
    # Wrap to [-SIDEREAL_DAY_SEC/2, SIDEREAL_DAY_SEC/2]
    if offset_sec > SIDEREAL_DAY_SEC / 2:
        offset_sec -= SIDEREAL_DAY_SEC
    elif offset_sec < -SIDEREAL_DAY_SEC / 2:
        offset_sec += SIDEREAL_DAY_SEC

    angle = offset_sec * (360.0 / SIDEREAL_DAY_SEC)

    return angle

def angle_between_object_and_out(date_time: datetime, object_ra_deg: str) -> float:
    """
    Computes the angle (in degrees) between an object's right ascension and the OUT vector angle for a given datetime.
    :param date_time: The date and time for calculation (timezone-aware, UTC recommended)
    :param object_ra_str: The object's right ascension as a string (e.g., '13h4m12s', '202.5d')
    :return: Angle in degrees (object RA - OUT vector), normalized to [-180, 180]
    """
    object_ra_deg = Angle(object_ra_deg).deg
    out_angle_deg = calculate_out_vector_angle(date_time)
    diff = ((object_ra_deg - out_angle_deg + 180) % 360) - 180
    return diff

def angle_between_object_and_zenith(date_time: datetime, object_ra_str: str) -> float:
    """
    Computes the angle (in degrees) between an object's right ascension and the zenith (local sidereal time) for a given datetime and longitude.
    :param date_time: The date and time for calculation (timezone-aware, you must use local time!)
    :param object_ra_str: The object's right ascension as a string (e.g., '13h30m', '202.5d')
    :return: Angle in degrees (object RA - zenith), normalized to [-180, 180]
    """
    time_to_midnight_angle = angle_between_zenith_and_out_solar(date_time)
    print(f"Time to midnight angle: {time_to_midnight_angle:.2f}°")
    object_ra_deg = angle_between_object_and_out(date_time, object_ra_str)
    print(f"Object RA degrees: {object_ra_deg:.2f}°")
    diff = ((object_ra_deg - time_to_midnight_angle + 180) % 360) - 180
    print(f"Angle between object and zenith: {diff:.2f}°")

    return diff