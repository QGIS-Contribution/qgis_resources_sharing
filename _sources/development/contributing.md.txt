# Contributing

You are welcome to make a patch on GitHub by issuing pull request
[here](https://github.com/QGIS-Contribution/QGIS-ResourceSharing).

Also, if you experience problems with the plugin, or have suggestions
for improvement, you are very welcome to add issues there.

If contributing code, it would be nice if you check it with pep8
and make sure that the tests are not broken by running:

```bash
pep8 resource_sharing
nose2-3 -s test --with-coverage
```

This project uses git submodules for the test data.
To clone the project completely, do:

```bash
git clone git@github.com:QGIS-Contribution/QGIS-ResourceSharing.git <the destination directory>
cd <the destination directory>
git submodule init
git submodule update
```
