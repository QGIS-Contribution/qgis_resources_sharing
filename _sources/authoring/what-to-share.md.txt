# What to share

A repository contains collections to be shared.

A collection is a set of resources that belong together.

Either because they can be used to create a coherent map design or do a specific task, or because they form a natural group.

The items that supported by the QGIS Resource Sharing plugin are (plugin version in parenthesis):

| Item | Folder | Notes |
| :--- | :----- | :---- |
| Raster images | image | Image files that can be used as *Raster image markers* and *Raster image fills*. Can be referenced from symbols and styles. |
| SVGs | svg | SVG files that can be used as *SVG markers* and *SVG fills*. Can be referenced from symbols and styles. |
| Symbols | symbol | XML files that can contain marker, line and fill symbols and also colorramps, textformattings (0. 14) and labelsettings (0.14). |
| Layer styles | style | QML files. |
| Expressions (0.15) | expressions | JSON files with user expressions (QGIS 3.12 and later). |
| Processing scripts | processing | Python processing scripts. |
| Models (0.10) | models | Models for the *Graphical modeler*. |
| R scripts (0.9) | rscripts | *Processing R Provider* plugin **R scripts**. |
| Checklists (0.16) | checklists | Checklist files for the [QGIS Dataset QA Workbench] plugin. |

Note that you can include other QGIS resources in the repository (composer templates, project files, ...) as well.

They will be available in the collection directory, but the plugin will not do anything with them.

[QGIS Dataset QA Workbench]: https://github.com/kartoza/qgis_dataset_qa_workbench
