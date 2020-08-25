from sweref99.transverse_mercator import TransverseMercator
from sweref99.ellipsoids import GRS80

# https://www.lantmateriet.se/globalassets/kartor-och-geografisk-information/gps-och-geodetisk-matning/info_blad-2.pdf
projection_parameters = {
    "SWEREF_99_TM": (GRS80, 15.000, 0.9996, 0, 500000),
    "SWEREF_99_12_00": (GRS80, 12.000, 1, 0, 150000),
    "SWEREF_99_13_30": (GRS80, 13.500, 1, 0, 150000),
    "SWEREF_99_15_00": (GRS80, 15.000, 1, 0, 150000),
    "SWEREF_99_16_30": (GRS80, 16.500, 1, 0, 150000),
    "SWEREF_99_18_00": (GRS80, 18.000, 1, 0, 150000),
    "SWEREF_99_14_15": (GRS80, 14.250, 1, 0, 150000),
    "SWEREF_99_15_45": (GRS80, 15.750, 1, 0, 150000),
    "SWEREF_99_17_15": (GRS80, 17.250, 1, 0, 150000),
    "SWEREF_99_18_45": (GRS80, 18.750, 1, 0, 150000),
    "SWEREF_99_20_15": (GRS80, 20.250, 1, 0, 150000),
    "SWEREF_99_21_45": (GRS80, 21.750, 1, 0, 150000),
    "SWEREF_99_23_15": (GRS80, 23.250, 1, 0, 150000)
}


def make_transverse_mercator(projection="SWEREF_99_TM"):
    ellipsoid, λ0, k0, fn, fe = projection_parameters[projection]
    return TransverseMercator(ellipsoid.semi_major_axis, ellipsoid.flattening, λ0, k0, fn, fe)
