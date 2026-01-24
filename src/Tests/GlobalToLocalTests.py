import unittest
import numpy as np

class TestGlobalToLocal(unittest.TestCase):
    def test_angle_between_radians(self):
        from Astromath.GlobalToLocal import AngleBetweenRadians

        # 0 degrees (same vector)
        a = np.array([1, 0, 0])
        b = np.array([1, 0, 0])
        self.assertAlmostEqual(AngleBetweenRadians(a, b), 0.0)

        # 90 degrees
        a = np.array([1, 0, 0])
        b = np.array([0, 1, 0])
        self.assertAlmostEqual(AngleBetweenRadians(a, b), np.pi / 2)

        # 180 degrees (opposite vectors)
        a = np.array([1, 0, 0])
        b = np.array([-1, 0, 0])
        self.assertAlmostEqual(AngleBetweenRadians(a, b), np.pi)

        # Arbitrary angle (60 degrees)
        a = np.array([1, 0, 0])
        b = np.array([0.5, np.sqrt(3)/2, 0])
        self.assertAlmostEqual(AngleBetweenRadians(a, b), np.pi/3)

    def test_spherical_to_cartesian_cardinals(self):
        from Astromath.GlobalToLocal import SphericalToCartesian, UP, EAST, NORTH
        
        # Origin
        np.testing.assert_array_almost_equal(
            SphericalToCartesian(0, 0, 0),
            np.zeros(3)
        )
        # North (z axis): phi=0
        np.testing.assert_array_almost_equal(
            SphericalToCartesian(1, 0, 0),
            NORTH
        )
        # Up (x axis): phi=90, theta=0
        np.testing.assert_array_almost_equal(
            SphericalToCartesian(1, 0, 90),
            UP
        )
        # East (y axis): phi=90, theta=90
        np.testing.assert_array_almost_equal(
            SphericalToCartesian(1, 90, 90),
            EAST
        )

        # Weird numbers
        result = SphericalToCartesian(1, 45, 45)
        expected = np.array([0.5, 0.5, 0.707107])
        np.testing.assert_array_almost_equal(result, expected, decimal=6)

        result = SphericalToCartesian(5, 135, 120)
        expected = np.array([-3.061862, 3.061862, -2.5])
        np.testing.assert_array_almost_equal(result, expected, decimal=6)

        result = SphericalToCartesian(13.9, 241.9, 39.1)
        expected = np.array([-4.129076, -7.733071, 10.787045])
        np.testing.assert_array_almost_equal(result, expected, decimal=6)

if __name__ == '__main__':
    unittest.main()
