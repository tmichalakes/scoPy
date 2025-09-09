import numpy as np;
# Library to convert Right Ascension and Declination to given coordinates given Latitude, Right Ascension, And Declination
# All Coordinate systems are defined in terms of the orthonormal basis x=up, y=east, z=north where up is directly towards the zenith,
# East is a heading of 90 degrees, and north is a heading defined by 0 degrees. This composes a basis following right-hand
# rule for 3 dimensional coordinate systems.

UP = np.array([1, 0, 0]) #x
EAST = np.array([0, 1, 0]) #y
NORTH = np.array([0, 0, 1]) #z

DEGREES_PER_RADIAN = 180 / np.pi
RADIANS_PER_DEGREE = np.pi / 180

# Converts a right ascension given in hours, minutes, and seconds purely to seconds.
def RASeconds(hours: float, minutes: float, seconds: float) -> float:
    return hours * 60 * 60 + minutes * 60 + seconds

# Given a right ascension provided in seconds, returns an angle from the up vector in the up-east plane
# Do not need to convert declination to degrees - it's in degrees.
def RAToTheta(seconds: float) -> float:
    # TO-DO: this and other conversions to get angles from RA and time and date. 
    return 0

# Given a right ascension (in degrees from the zenith) and a declination (in degrees), returns 
# a vector within the ambient basis.
def SphericalToCartesian(rightAscensionDegrees: float, declination: float) -> np.ndarray:
    if rightAscensionDegrees < -180 or rightAscensionDegrees > 180:
        raise ValueError("Right Ascension degrees must be between -180 and 180")
    
    if declination < -90 or declination > 90:
        raise ValueError("Declination must be between -90 and 90")

    ra_radians = rightAscensionDegrees * RADIANS_PER_DEGREE
    dec_radians = declination * RADIANS_PER_DEGREE

    up = np.cos(ra_radians) * np.cos(dec_radians)
    east = np.sin(ra_radians) * np.cos(dec_radians)
    north = np.sin(dec_radians)

    return up * UP + east * EAST + north * NORTH

# Given a latitude in degrees (negative means south), return a basis for local coordinates
# such that up describes straight up from that latitude, north describes directly towards the northern
# horizon. 
def GetBasisForLatitude(latitude: float) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    if latitude < -90 or latitude > 90:
        raise ValueError("Value must be between -90 and 90")

    # Euler rotational matrix about the east axis - a latitude change is a tilt 
    lat_radians = latitude * RADIANS_PER_DEGREE

    upLocal = np.cos(lat_radians) * UP + np.sin(lat_radians) * NORTH
    eastLocal = EAST
    northLocal = -1 * np.sin(lat_radians) * UP + np.cos(lat_radians) * NORTH
    
    return (upLocal, eastLocal, northLocal)

# Provided a vector and a basis of orthonormal vectors, converts the vector to the coordinate system defined by the matrix
def BasisChange(vector: np.ndarray, basis: tuple[np.ndarray, np.ndarray, np.ndarray]) -> np.ndarray:
    if vector is None:
        raise ValueError("You must provide a vector")
    
    if basis is None:
        raise ValueError("You must provide a basis")

    # np.matrix is "row-first" - that is, given [[1,2], [3,4]], 1,2 will be the first row of the matrix
    baseChangeMatrix = np.matrix(basis)

    return baseChangeMatrix * vector

# Given a local vector and a local basis, gives the heading vector in the east-north plane
def GetHeadingVector(localVector: np.ndarray, localBasis: tuple[np.ndarray, np.ndarray, np.ndarray]) -> np.ndarray:
    localEast = localBasis[1]
    localNorth = localBasis[2]

    heading: np.ndarray = localVector.dot(localEast) * localEast + localVector.dot(localNorth) * localNorth
    mag_heading = np.linalg.norm(heading)

    # if the magnitude is 0, this implies local vector is parallel to the up vector
    # this is an edge case I'll have to consider. 
    if(mag_heading == 0):
        return np.array([0,0,0])
    
    # return a unit vector
    return heading * (1 / mag_heading)

# Given two vectors returns the angle between them in radians
def AngleBetweenRadians(a: np.ndarray, b: np.ndarray) -> float:
    dot = np.dot(a, b)

    mag_a = np.linalg.norm(a)
    mag_b = np.linalg.norm(b)

    if(mag_a * mag_b == 0):
        raise ValueError("One or more vectors ")

    cosine = np.clip(dot / (mag_a * mag_b), -1, 1)

    return np.arccos(cosine)

def GetHeadingAngleDegrees(heading: np.ndarray) -> float:
    return AngleBetweenRadians(heading, NORTH) * DEGREES_PER_RADIAN
