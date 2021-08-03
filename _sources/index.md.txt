# QGIS Resource Sharing - Documentation

> **Description :** {{ description }}  
> **Author and contributors:** {{ author }}  
> **Plugin version:** {{ version }}  
> **QGIS minimum version:** {{ qgis_version_min }}  
> **QGIS maximum version:** {{ qgis_version_max }}  
> **Source code:** {{ repo_url }}  
> **Last documentation update:** {{ date_update }}

## Introduction

![the plugin](assets/img/app.png)

If you have ever wanted to share QGIS resources easily with your peers, this plugin comes to the rescue!

The QGIS Resource Sharing plugin allows QGIS users to share resources (symbols, layer styles, SVGs, images, expressions, processing models, processing scripts, Dataset QA checklists,  and R scripts) in repositories that other users can access.

A QGIS Resource Sharing repository could be a remote GIT repository (currently Github, Gitlab and Bitbucket public repositories are supported), local file system collections, or zipped collections on the Web.

![settings-repositories](/assets/img/repositories.png)

Collections are stored locally. By default, they are placed under the user's QGIS directory.

Git based collections are downloaded using git *clone* and updated using git *pull*, meaning that the complete repository will be stored locally, and that you can use a git client to suggest changes, keep it updated
(pull)...

The plugin lets you update the repositories through the GUI (the *Reload repositories* button in *Settings*).

The plugin was initially implemented as a Google Summer of Code project in 2016 for QGIS under the OSGeo organization by Akbar Gumbira (student), Alessandro Pasotti (mentor), Anita Graser (mentor), and with the help of Richard Duivenvoorde, Tim Sutton, and others in the QGIS community.

## Table of contents

```{toctree}
---
caption: How to use the plugin
maxdepth: 1
---
usage/installation
usage/installing-collection
usage/adding-repository
usage/plugin-configuration
usage/problems_and_solutions
```

```{toctree}
---
caption: Create your own collections
maxdepth: 1
---
authoring/what-to-share
authoring/creating-repository
authoring/repository-structure
authoring/creating-metadata
authoring/publishing-repository
authoring/repository-example
```

```{toctree}
---
caption: Contribute to the plugin
maxdepth: 1
---
development/contributing
development/environment
development/update_dependencies
development/documentation
development/release-workflow
```
