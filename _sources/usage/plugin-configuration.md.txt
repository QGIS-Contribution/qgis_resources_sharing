# Plugin configuration

## Local collections directory

The location (in the local file system) of the directory that contains the installed collections is configurable in settings: `localCollectionDir` under `[ResourceSharing]`.

You can change this in the GUI by going to the _Advanced_ tab of the _Options_ dialog (_Settings-> Options..._).

After you have promised to be careful, you can make your changes.

You can also change it by editing the QGIS3.ini file that is located under QGIS in the user QGIS folder (`/.local/share/QGIS/QGIS3/profiles/default/QGIS` on Ubuntu, `C:\Users\<user>\AppData\Roaming\QGIS\QGIS3\profiles\default\QGIS` on Windows).

For versions up to and including 0.9.0, the default location was `~/QGIS/Resource Sharing`, and the location could not be changed.

Since version 0.10.0, the default location is `<QGIS Home>/resource_sharing/collections`, but the user can specify an alternative location using the `localCollectionDir` setting as explained above.

If the specified alternative location does not exist in the file system, the plugin will try to create it.

Changing the location in settings will not move the already installed collections, so if they are not moved (manually) to the new location, they will have to be installed again.

If you upgrade from a pre-0.10.0 version of the plugin, meaning that `~/QGIS/Resource Sharing` is present in your file system, that directory will be used (and recorded in your QGIS `localCollectionDir` settings) until the location is changed by modifying the `localCollectionDir` settings.
