# Dependencies upgrade workflow

This plugin has external dependencies:

- dulwich
- giturlparse
- pathvalidate

Because it's still hard to install Python 3rd party packages from an index (for example <https://pypi.org>), especially on Windows or Mac systems (or even on Linux if we want to do it properly in a virtual environment), those required packages are stored in the `ext_libs` folder.

## Upgrade workflow

Manage versions in the `requirements/embedded.txt` file, then:

```bash
python -m pip install --no-deps -U -r requirements/embedded.txt -t ext_libs
```

Note: even if `dulwich` depends on `certifi` and `urllib3`, we specifally install them since they are already included with QGIS.

## Related links

- <https://gis.stackexchange.com/questions/141320/installing-3rd-party-python-libraries-for-qgis-on-windows>
- <https://github.com/QGIS-Contribution/QGIS-ResourceSharing/issues/112>
