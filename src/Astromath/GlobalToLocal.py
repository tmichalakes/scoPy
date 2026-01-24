import numpy as np

# Library to convert Right Ascension and Declination to given coordinates given Latitude, Right Ascension, And Declination
# All Coordinate systems are defined in terms of the orthonormal basis x=up, y=east, z=north where up is directly towards the zenith,
# East is a heading of 90 degrees, and north is a heading defined by 0.0 degrees. This composes a basis following right-hand
# rule for 3 dimensional coordinate systems.

UP = np.array([1.0, 0.0, 0.0]) #x
EAST = np.array([0.0, 1, 0.0]) #y
NORTH = np.array([0.0, 0.0, 1]) #z

DEGREES_PER_RADIAN = 180.0 / np.pi
RADIANS_PER_DEGREE = np.pi / 180.0

# Given a right ascension (in degrees from the zenith) and a declination (in degrees), returns 
# a vector within the ambient basis.
def SphericalToCartesian(rho: float, theta: float, phi: float) -> np.ndarray:
    """
    Converts spherical coordinates to Cartesian coordinates in the ambient basis, using standard mathematical conventions.

    Standard convention:
    - theta (azimuthal): angle in degrees from the positive x-axis in the x-y plane, in [0, 360].
    - phi (polar): angle in degrees from the positive z-axis down to the x-y plane, in [0, 180].

    :param rho: Radius or magnitude
    :type rho: float
    :param theta: Azimuthal angle in degrees, measured from the positive x-axis in the x-y plane, must be in the range [0, 360].
    :type theta: float
    :param phi: Polar angle in degrees, measured from the positive z-axis, must be in the range [0, 180].
    :type phi: float
    :return: Returns a 1-D ndarray of shape (3,) representing the Cartesian coordinates.
    :rtype: ndarray[_AnyShape, dtype[Any]]
    """
    if theta < 0 or theta > 360:
        raise ValueError("Theta (azimuthal) degrees must be between 0 and 360")
    if phi < 0 or phi > 180:
        raise ValueError("Phi (polar) degrees must be between 0 and 180")

    theta_radians = theta * RADIANS_PER_DEGREE
    phi_radians = phi * RADIANS_PER_DEGREE

    # Standard convention:
    # x = rho * sin(phi) * cos(theta)
    # y = rho * sin(phi) * sin(theta)
    # z = rho * cos(phi)
    up = np.sin(phi_radians) * np.cos(theta_radians)
    east = np.sin(phi_radians) * np.sin(theta_radians)
    north = np.cos(phi_radians)

    return rho * (up * UP + east * EAST + north * NORTH)

# GetBasis for local right ascension
def GetBasisForLocalRightAscension(azimuthalAngle: float) -> float:
    """
    Docstring for GetBasisForLocalRightAscension
    
    :param azimuthalAngle: Description
    :type azimuthalAngle: float
    :return: Description
    :rtype: float
    """
    if azimuthalAngle < -180 or azimuthalAngle > 180:
        raise ValueError("Right Ascension Angle must be between -180 and 180")
    
    ra_radians = azimuthalAngle * RADIANS_PER_DEGREE
    upLocal = np.cos(ra_radians) * UP + np.sin(ra_radians) * EAST
    eastLocal = -1 * np.sin(ra_radians) * UP + np.cos(ra_radians) * EAST
    northLocal = NORTH

    return (upLocal, eastLocal, northLocal)

# Given a latitude in degrees (negative means south), return a basis for local coordinates
# such that up describes straight up from that latitude, north describes directly towards the northern
# horizon. 
def GetBasisForLatitude(latitude: float) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    if latitude < -90 or latitude > 90:
        raise ValueError("Latitude must be between -90 and 90")

    # Euler rotational matrix about the east axis - a latitude change is a tilt 
    lat_radians = latitude * RADIANS_PER_DEGREE

    upLocal = np.cos(lat_radians) * UP + np.sin(lat_radians) * NORTH
    eastLocal = EAST
    northLocal = -1 * np.sin(lat_radians) * UP + np.cos(lat_radians) * NORTH
    
    return (upLocal, eastLocal, northLocal)

# Provided a vector and a basis of orthonormal vectors, converts the vector to the coordinate system defined by the matrix
def BasisChange(vector: np.ndarray, *basis_vectors: np.ndarray) -> np.ndarray:
    """
    Given an ambient vector `vector` and a variable list of basis vectors (each a 1-D array length 3),
    return the coordinates of `vector` in that basis. Basis vectors are interpreted as rows, so
    result = A @ vector where A[i,:] = basis_vector_i. Returns a 1-D ndarray of shape (3,) (or (n,) when
    n basis vectors provided).
    """
    if vector is None:
        raise ValueError("You must provide a vector")

    if not basis_vectors:
        raise ValueError("You must provide at least one basis vector")

    # Ensure vector is a 1-D ndarray
    vec = np.asarray(vector).reshape(-1,)

    # Stack basis vectors as rows (each row is a basis vector expressed in ambient coords)
    try:
        A = np.vstack([np.asarray(b).reshape(-1,) for b in basis_vectors])
    except Exception as e:
        raise ValueError("Basis vectors must be array-like and match vector length") from e

    if A.shape[1] != vec.shape[0]:
        raise ValueError(f"Basis vectors length ({A.shape[1]}) must match vector length ({vec.shape[0]})")

    # Compute coordinates; result is a 1-D ndarray of length equal to number of basis vectors
    coords = A @ vec
    return coords

# Given a local vector and a local basis, gives the heading unit vector in the east-north plane
def GetHeadingVector(localVector: np.ndarray, localBasis: tuple[np.ndarray, np.ndarray, np.ndarray]) -> np.ndarray:
    localEast = localBasis[1]
    localNorth = localBasis[2]

    heading: np.ndarray = localVector.dot(localEast) * localEast + localVector.dot(localNorth) * localNorth
    mag_heading = np.linalg.norm(heading)

    # if the magnitude is 0.0, this implies local vector is parallel to the up vector
    # this is an edge case I'll have to consider. 
    if(mag_heading == 0.0):
        return np.array([0.0,0.0,0.0])
    
    # return a unit vector
    return heading * (1.0 / mag_heading)

# Given two vectors returns the angle between them in radians
def AngleBetweenRadians(a: np.ndarray, b: np.ndarray) -> float:
    """
    Calculates the angle in radians between two vectors a and b.    
    :type a: np.ndarray
    :type b: np.ndarray
    :return: The angle in radians between vectors a and b
    :rtype: float
    """
    dot = np.dot(a, b)

    mag_a = np.linalg.norm(a)
    mag_b = np.linalg.norm(b)

    if(mag_a * mag_b == 0.0):
        raise ValueError("One or more vectors ")

    cosine = np.clip(dot / (mag_a * mag_b), -1.0, 1.0)

    return np.arccos(cosine)

# Given a heading in the east-north plane, returns the angle between the heading vector and the north vector.
def GetHeadingAngleDegrees(heading: np.ndarray) -> float:
    return AngleBetweenRadians(heading, NORTH) * DEGREES_PER_RADIAN

# Given a vector, returns the angle between that vector and the up vector
def GetInclinationAngleDegrees(vector: np.ndarray) -> float:
    return AngleBetweenRadians(vector, UP) * DEGREES_PER_RADIAN
    
        