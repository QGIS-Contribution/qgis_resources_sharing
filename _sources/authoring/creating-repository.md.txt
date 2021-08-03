# Creating a repository

## Preparing the Repository

In order for the tools to parse the repository correctly, the repository must have a certain structure. This is what you need to do:

1. Go to [this page](repository-structure) to get information about the expected structure.
2. Create correct metadata for the repository (consult [this page](creating-metadata)).
3. When you have prepared your repository, you can check if the repository is all good by trying it using the file system handler.

In the plugin, go to the `Settings` tab and add a new repository pointing to the root of the repository in your local file system. The repository URL looks like this:

- Linux: `file:///home/pointing/to/repository_root`
- Windows: `file://C:/home/pointing/to/repository_root`

----

## Where can you share it?

These are the options for sharing: on Github, GitLab, Bitbucket (they need to be public repositories), Gogs (_Go Git Service_), local file system (if you want to share the collections with your colleagues on the network), or in your own server with the HTTP(S) protocol.

### Github, GitLab and Bitbucket

There is nothing complicated here if you are already familiar with git.

After preparing the repository on your local machine, you can make it into a git repository as usual.
In general, you can do:

```bash
cd <repository root>
git init
git add .
git commit -m "Created a cool repository for cool users."
git remote add origin <remote repository URL>
git push origin master
```

Note that you currently need to use the `master` branch for your repository.

### Local File System

This is even simpler.

After preparing the repository, you can use it right away.

In the `Settings` tab, you add a repository with URL pointing to the repository root in your local machine (absolute path, example: `file:/home/user/QGIS-collections/mycollection`).

It's as simple as that.

If there is a problem with metadata or other issues when adding the
repository, you will be told.

### Your Own Server

This option could be useful in some cases, e.g. if you want to make private collections available for your customers.

There are some additional requirements that you need to be aware of if you choose this option:

- The URL structure of the repository. If your repository URL is `http://www.mydomain.com/qgisrepository/`, you must make the metadata available on: `http://www.mydomain.com/qgisrepository/metadata.ini`
- Each collection must be zipped. The zip file of a collection must be named `<name of collection>.zip`, and the zip shall combine the subdirectories of the collection (one or more of `checklists`, `expressions`, `image`, `models`, `processing`, `rscripts`, `svg` and `symbol`), in addition to a `preview` subdirectory for preview images.

For example, if you have a collection named `test_collection`, the collection must be present as: `http://www.mydomain.com/qgisrepository/collections/test_collection.zip`, and the structure of this zip file must be (only include directories that contain resources you would like to share):

```txt
test_collection.zip
├── checklists
├── expressions
├── image
├── models
├── preview
├── processing
├── rscripts
├── svg
├── symbol
```

- Preview images that illustrates the collection should be included. If you define preview images for collection `test_collection` in metadata (`preview=preview/prev1.png,prev2.png`), you have to place these preview images in the zip-file in a separate directory. `preview` is the recommended name for that directory.

An example server directory setup for the repository `myfirstrepository` with one collection (`test_collection`) that contains resources to share in a lot of resource categories:

```ascii
      qgisrepository
      ├── metadata.ini
      └── collections
          └── test_collection.zip
              ├── checlists
              |   ├── checklist1.json
              |   ├── ...
              |   └── lastchecklist.json
              ├── expressions
              |   ├── expressions1.json
              |   ├── ...
              |   └── lastexpressions.json
              ├── image
              |   ├── image1.png
              |   ├── ...
              |   └── lastimage.png
              ├── models
              |   ├── firstmodel.model3
              |   ├── ...
              |   └── testmodel.model3
              ├── preview
              |   ├── prev1.png
              |   └── prev2.png
              ├── processing
              |   ├── firstscript.py
              |   ├── ...
              |   └── testscript.py
              ├── rscripts
              |   ├── firstRscript.rsx
              |   └──firstRscript.rsx.help
              |   ├── ...
              |   ├── testRscript.rsx
              |   └── testRscript.rsx.help
              ├── style
              |   ├── firstlayerstyle.qml
              |   ├── ...
              |   └── testlayerstyle.qml
              ├── svg
              |   ├── firstmodel.model3
              |   ├── ...
              |   └── testmodel.model3
              └── symbol
                  ├── firststyle.xml
                  ├── ...
                  └── teststyle.xml

```

The repository URL to be used when adding the repository (in the _QGIS Resource Sharing_ plugin): `http://www.mydomain.com/qgisrepository/`.

You can also use authentication for this repository.

Users can configure authentication details in the plugin, so that they will be able to fetch the repository and the collections inside.
