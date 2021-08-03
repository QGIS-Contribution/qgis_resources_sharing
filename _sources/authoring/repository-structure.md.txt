# Repository structure

In order for the plugin to be able to read the repository correctly, the repository must have a specific structure.

Generally the structure looks like this:

    Repository root
    ├── README (encouraged)
    ├── metadata.ini (required)
    └── collections
        ├── [Collection1 register id] (the id string used in "collections" in metadata.ini)
        │   ├── checklists (optional, containing checklist definition JSON files)
        │   ├── expressions (optional, containing JSON files with QGIS Expressions)
        │   ├── image (optional, containing all kinds of image files)
        │   ├── models (optional, containing Processing models)
        │   ├── preview (encouraged, containing previews for the collection, referenced in metadata.ini)
        │   ├── processing (optional, containing Python Processing scripts)
        │   ├── rscripts (optional, containing R scripts)
        │   ├── style (optional, containing QML files - QGIS Layer style)
        │   ├── svg (optional, containing SVG files)
        │   ├── symbol (optional, containing symbol definition XML files)
        │   └── license file (encouraged)
        │
        ├── [Collection2 register id] (the id string used in "collections" in metadata.ini)
        │   ├── checklists (optional, containing checklist definition JSON files)
        │   ├── expressions (optional, containing JSON files with QGIS Expressions)
        │   ├── image (optional, containing all kinds of image files)
        │   ├── models (optional, containing Processing models)
        │   ├── preview (encouraged, containing previews for the collection, referenced in metadata.ini)
        │   ├── processing (optional, containing Python Processing scripts)
        │   ├── rscripts (optional, containing R scripts)
        │   ├── style (optional, containing QML files - QGIS Layer style)
        │   ├── svg (optional, containing SVG files)
        │   ├── symbol (optional, containing symbol definition XML files)
        │   └── license file (encouraged)
        │
        ├── ...
        ├── ...
        │
        └── [CollectionN register id] (the id string used in "collections" in metadata.ini)
            ├── checklists (optional, containing checklist definition JSON files)
            ├── expressions (optional, containing JSON files with QGIS Expressions)
            ├── image (optional, containing all kinds of image files)
            ├── models (optional, containing Processing models)
            ├── processing (optional, containing Python Processing scripts)
            ├── rscripts (optional, containing R scripts)
            ├── style (optional, containing QML files - QGIS Layer style)
            ├── svg (optional, containing SVG files)
            ├── symbol (optional, containing symbol definition XML files)
            └── license file (encouraged)

If the _QGIS Resource Sharing plugin_ shall be able to make the
resources available to QGIS users in a convenient way, you have
to place them where the plugin expects to find them:

- Layer style (QML) files belong in the **_style_** directory.
- Processing models belong in the **_models_** directory.
- Processing (Python) scripts belong in the **_processing_**
  directory.
- R script (for use with the Processing R plugin) belong in in the
  **_rscripts_** directory.

- Symbol XML files belong in the **_symbol_** directory.
  Symbol images are expected to be in the **_image_** directory and
  symbol SVGs are expected to be in the **_svg_** directory.

- SVGs belong in the **_svg_** directory.

- Images belong in the **_image_** directory.

- Expression JSON files belong in the **_expressions_** directory.

- Data QA Workbench checklist JSON files belong in the
  **_checklists_** directory.

Check the [QGIS Resources Repository](https://github.com/QGIS/QGIS-Resources) and [this test repository](https://github.com/QGIS-Contribution/QGIS_Test-Resources) for GitHub repository examples.
