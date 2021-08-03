# Publishing your repository

When everything is done, and you have published the repository somewhere, you can add the repository in the
_QGIS Resource Sharing_ plugin in QGIS.

You may wonder if you can have your repository included as a default repository that will be shown to all QGIS users without them
needing to add the repository manually.

Well, yes, that may be possible.

To offer your repository as a default repository, fork the [QGIS official resource repository](https://github.com/qgis/QGIS-Resources), update the [`directory.csv`](https://github.com/qgis/QGIS-Resources/blob/master/directory.csv) file and make a pull request to the upstream project.

If your offer is accepted, and the pull request merged, your repository will be listed among the "approved" repositories and its
collections will be available to everyone through the _Resource Sharing_ plugin the next time they start QGIS and the _Resource Sharing_ plugin.
