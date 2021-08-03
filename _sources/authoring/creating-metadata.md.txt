# Creating metadata

In the root of the repository, there has to be a metadata file describing the repository and its collections.

## General

The metadata file (`metadata.ini`) must have a `general` section with this information:

| Name | Status | Description |
| :--- | :----: | :---------- |
| collection | Required | Comma separated list of collection names (these have to match the directory names of the collections) |

## Collection

For each collection, metadata are needed. The section must be named by the name defined in the general section.

This is the contents of the collection section:

| Name | Status | Description |
| :--- | :----: | :---------- |
| Version | Optional | The version of the collection, default is 1.0 |

Add a collection with checklists
| author | Required | Author's name |
| description | Required | Additional information about the collection |
| email | Optional | Author's email |
| license | Optional | The license of the collection e.g GNU GPL |
| license_file | Optional | License file (path relative to the collection root) |
| name | Required | The name of the collection |
|version|
| preview | Optional | Comma separated list of preview images (paths relative to the collection root) |
| qgis_minimum_version | Optional | Minimum QGIS version. If not specified, the minimum version will be 2.0 |
| qgis_maximum_version | Optional | Maximum QGIS version. If not specified, the maxium version will be 3.99 |
| tags | Required | Comma separated list of tags |

This is an example of the `metadata.ini` file:

```ini
[general]
collections=osm_spatialite_googlemaps,flowmap

[osm_spatialite_googlemaps]
name=OSM Spatialite Googlemaps
author=Anita Graser
email=anitagraser@gmx.at
tags=osm,spatialite,google maps,roads
description=The collection contains a complete resources to create a coherent map that looks similar to the old Google Maps style from OSM data in a SpatiaLite database
preview=preview/osm_spatialite_googlemaps.png, preview/osm_spatialite_googlemaps_lines.png
qgis_minimum_version=2.0
qgis_maximum_version=3.99

[flowmap]
name=Flowmap
author=Anita Graser
email=anitagraser@gmx.at
tags=flows, arrows
description=The collection contains styles for flow maps
preview=preview/preview.png
qgis_minimum_version=2.0
qgis_maximum_version=3.99
```
