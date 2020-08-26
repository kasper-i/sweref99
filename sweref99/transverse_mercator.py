import math


class TransverseMercator(object):
    """
    Transverse Mercator (Gauss Conformal Projection) map projection.
    https://www.lantmateriet.se/globalassets/kartor-och-geografisk-information/gps-och-geodetisk-matning/gauss_conformal_projection.pdf

    All geodetic coordinates are expressed in degrees and grid coordinates in meters.

    Args:
        semi_major_axis::int
            Semi-major axis of the ellipsoid
        flattening::int
            Flattening of the ellipsoid
        central_meridian::float
            Longitude of the central meridian
        scale_factor::float
            Scale factor along the central meridian
        false_northing::int
            False northing
        false_easting::int
            False easting
    """

    def __init__(self,
                 semi_major_axis,
                 flattening,
                 central_meridian,
                 scale_factor,
                 false_northing,
                 false_easting):

        self.λ0 = math.radians(central_meridian)
        self.k0 = scale_factor
        self.fn = false_northing
        self.fe = false_easting

        self.a = semi_major_axis
        self.f = flattening

        self.e2 = self.f * (2 - self.f)
        self.e4 = self.e2 ** 2
        self.e6 = self.e2 ** 3
        self.e8 = self.e2 ** 4

        self.n = self.f / (2 - self.f)
        self.n2 = self.n ** 2
        self.n3 = self.n ** 3
        self.n4 = self.n ** 4

        self.â = (self.a / (1 + self.n)) * (1 + 0.25 * self.n2 + (1 / 64) * self.n4)

        self.A_star = (self.e2 + self.e4 + self.e6 + self.e8)
        self.B_star = (-1 / 6) * (7 * self.e4 + 17 * self.e6 + 30 * self.e8)
        self.C_star = (1 / 120) * (224 * self.e6 + 889 * self.e8)
        self.D_star = (-1 / 1260) * (4279 * self.e8)

        self.δ1 = 0.5 * self.n - (2 / 3) * self.n2 + (37 / 96) * self.n3 - (1 / 360) * self.n4
        self.δ2 = (1 / 48) * self.n2 + (1 / 15) * self.n3 - (437 / 1440) * self.n4
        self.δ3 = (17 / 480) * self.n3 - (37 / 840) * self.n4
        self.δ4 = (4397 / 161280) * self.n4

        self.A = self.e2
        self.B = (1 / 6) * (5 * self.e4 - self.e6)
        self.C = (1 / 120) * (104 * self.e6 - 45 * self.e8)
        self.D = (1 / 1260) * (1237 * self.e8)

        self.β1 = 0.5 * self.n - (2 / 3) * self.n2 + (5 / 16) * self.n3 + (41 / 180) * self.n4
        self.β2 = (13 / 48) * self.n2 - (3 / 5) * self.n3 + (557 / 1440) * self.n4
        self.β3 = (61 / 240) * self.n3 - (103 / 140) * self.n4
        self.β4 = (49561 / 161280) * self.n4

    def grid_to_geodetic(self, northing, easting):
        """Convert from grid coordinates to geodetic coordinates.

        Args:
            northing::int
                Northing
            easting::int
                Easting

        Returns:
            latitude::int
                Latitude
            longitude::int
                Longitude
        """

        ξ = (northing - self.fn) / (self.k0 * self.â)
        η = (easting - self.fe) / (self.k0 * self.â)

        ξ_prim = ξ -\
                 self.δ1 * math.sin(2 * ξ) * math.cosh(2 * η) -\
                 self.δ2 * math.sin(4 * ξ) * math.cosh(4 * η) -\
                 self.δ3 * math.sin(6 * ξ) * math.cosh(6 * η) -\
                 self.δ4 * math.sin(8 * ξ) * math.cosh(8 * η)

        η_prim = η -\
                 self.δ1 * math.cos(2 * ξ) * math.sinh(2 * η) -\
                 self.δ2 * math.cos(4 * ξ) * math.sinh(4 * η) -\
                 self.δ3 * math.cos(6 * ξ) * math.sinh(6 * η) -\
                 self.δ4 * math.cos(8 * ξ) * math.sinh(8 * η)

        φ_star = math.asin(math.sin(ξ_prim) / math.cosh(η_prim))
        δλ = math.atan(math.sinh(η_prim) / math.cos(ξ_prim))

        λ = self.λ0 + δλ
        φ = φ_star + math.sin(φ_star) * math.cos(φ_star) * (self.A_star +
                                                            self.B_star * math.sin(φ_star) ** 2 +
                                                            self.C_star * math.sin(φ_star) ** 4 +
                                                            self.D_star * math.sin(φ_star) ** 6)

        return math.degrees(φ), math.degrees(λ)

    def geodetic_to_grid(self, latitude, longitude):
        """Convert from geodetic coordinates to grid coordinates.

        Args:
            latitude::int
                Latitude
            longitude::int
                Longitude

        Returns:
            x::int
                Northing
            y::int
                Easting
        """

        φ = math.radians(latitude)
        λ = math.radians(longitude)

        φ_star = φ - math.sin(φ) * math.cos(φ) * (self.A +
                                                  self.B * math.sin(φ) ** 2 +
                                                  self.C * math.sin(φ) ** 4 +
                                                  self.D * math.sin(φ) ** 6)

        δλ = λ - self.λ0
        ξ_prim = math.atan(math.tan(φ_star) / math.cos(δλ))
        η_prim = math.atanh(math.cos(φ_star) * math.sin(δλ))

        x = self.k0 * self.â * (ξ_prim +
                                self.β1 * math.sin(2 * ξ_prim) * math.cosh(2 * η_prim) +
                                self.β2 * math.sin(4 * ξ_prim) * math.cosh(4 * η_prim) +
                                self.β3 * math.sin(6 * ξ_prim) * math.cosh(6 * η_prim) +
                                self.β4 * math.sin(8 * ξ_prim) * math.cosh(8 * η_prim)) + self.fn

        y = self.k0 * self.â * (η_prim +
                                self.β1 * math.cos(2 * ξ_prim) * math.sinh(2 * η_prim) +
                                self.β2 * math.cos(4 * ξ_prim) * math.sinh(4 * η_prim) +
                                self.β3 * math.cos(6 * ξ_prim) * math.sinh(6 * η_prim) +
                                self.β4 * math.cos(8 * ξ_prim) * math.sinh(8 * η_prim)) + self.fe

        return x, y
