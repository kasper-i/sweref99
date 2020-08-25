# SWEREF 99 map projection

Python library for conversion between geodetic (latitude, longitude) coordinates and plane (N, E) grid coordinates.
Implements a Transverse Mercator map projection (Gauss Conformal Projection) and projection parameters for the SWEREF 99
geodetic reference system. The ellipsoid is GRS80 but other ellipsoids can easily be defined.

Since the WGS 84 datum used by GPS is almost identical to SWEREF 99 they can be used interchangeably for most
applications. More details on the relationship between WGS 84 and SWEREF 99 can be found 
[here](https://www.lantmateriet.se/sv/Kartor-och-geografisk-information/gps-geodesi-och-swepos/Referenssystem/Tredimensionella-system/SWEREF-99/).

The map projection implementation is based on the [Gauss-Krügers](https://www.lantmateriet.se/sv/Kartor-och-geografisk-information/gps-geodesi-och-swepos/Om-geodesi/Formelsamling/)
formula published by Lantmäteriet.

## Usage

```python
from sweref99 import projections

if __name__ == '__main__':
    tm = projections.make_transverse_mercator("SWEREF_99_TM")
    lat, lon = 57.705918, 11.987286

    # Geodetic to grid
    northing, easting = tm.geodetic_to_grid(lat, lon)
    print(f"{lat:.6f}° N {lon:.6f}°E : {northing:.2f} N {easting:.2f} E")

    # Grid to geodetic
    lat, lon = tm.grid_to_geodetic(northing, easting)
    print(f"{northing:.2f} N {easting:.2f} E : {lat:.6f}° N {lon:.6f}°E")
``` 

## Supported projections 

 * SWEREF_99_TM
 * SWEREF_99_12_00
 * SWEREF_99_13_30
 * SWEREF_99_15_00
 * SWEREF_99_16_30
 * SWEREF_99_18_00
 * SWEREF_99_14_15
 * SWEREF_99_15_45
 * SWEREF_99_17_15
 * SWEREF_99_18_45
 * SWEREF_99_20_15
 * SWEREF_99_21_45
 * SWEREF_99_23_15
 