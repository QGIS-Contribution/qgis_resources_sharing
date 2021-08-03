# Documentation

This documentation website is generated using Sphinx and deployed on [GitHub pages](https://pages.github.com/) using GitHub Actions.

To work on the documentation, install the related requirements:

```bash
python -m pip install -U -r requirements/documentation.txt
```

## Write

The documentation is divided into 3 categories. To update a particular page, find the markdown file in the related folder:

- for end-users: `docs/usage`
- for collections authors: `docs/authoring`
- for developers: `docs/development`

Put images in the `assets` directory.

```{tip}
To see live rendering of your documentation, you can run: `sphinx-autobuild -b html docs docs/_build/html`.
```

After you make changes to the documentation, please make a PR.

## Write documentation using live render

```bash
sphinx-autobuild -b html docs/ docs/_build
```

Open <http://localhost:8000> in a web browser to see the HTML render updated when a file is saved.

## Build

```bash
# build it
sphinx-build -b html docs docs/_build/html
```

Open `docs/_build/index.html` in a web browser.

## Deploy

Documentation website is hosted on GitHub Pages. Deployment takes advantage of [`ghp-import` library](https://pypi.org/project/ghp-import/). It's automatically triggered on CI but it's still possible to deploy it manually:

```bash
ghp-import --force --no-jekyll --push docs/_build/html
```

Files are uploaded to the branch `gh-pages` of the repository: <https://github.com/QGIS-Contribution/QGIS-ResourceSharing/tree/gh-pages>.
