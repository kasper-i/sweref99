import unittest
from sweref99.transverse_mercator import TransverseMercator
from sweref99 import projections


class TransverseMercatorTest(unittest.TestCase):
    def setUp(self):
        self.tm = TransverseMercator(6378137.0000, 1 / 298.257222101, 13.58547, 1.000002540000, -6226307.8640, 84182.8790)

    def test_geodetic_to_grid(self):
        x, y = self.tm.geodetic_to_grid(66.000, 24.000)
        self.assertAlmostEqual(x, 1135809.4138, places=4)
        self.assertAlmostEqual(y, 555304.0166, places=4)

    def test_grid_to_geodetic(self):
        lat, lon = self.tm.grid_to_geodetic(1135809.413803, 555304.016555)
        self.assertAlmostEqual(lat, 66.000, places=4)
        self.assertAlmostEqual(lon, 24.000, places=4)


class Sweref99Test(unittest.TestCase):
    def setUp(self):
        self.tm = projections.make_transverse_mercator("SWEREF_99_TM")

    def test_geodetic_to_grid(self):
        x, y = self.tm.geodetic_to_grid(66.000, 24.000)
        self.assertAlmostEqual(x, 7349217.67, places=2)
        self.assertAlmostEqual(y, 907351.98, places=2)

    def test_grid_to_geodetic(self):
        lat, lon = self.tm.grid_to_geodetic(1135809.413803, 555304.016555)
        self.assertAlmostEqual(lat, 10.2745317, places=6)
        self.assertAlmostEqual(lon, 15.5050428, places=6)


if __name__ == '__main__':
    unittest.main()
