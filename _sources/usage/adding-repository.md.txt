# Adding a repository

The officially approved *QGIS Resource Sharing* repositories and their collections should be listed in the *Settings* tab when you have clicked the ***Reload Repositories*** button, as illustrated in the screenshot below.

![Repositories](/assets/img/repositories.png)

You can add other repositories by clicking the ```Add repository...``` button and specify a *Name* for the repository (you are free to call it whatever you like, as long as the name is unique) and its *URL* (remember to use ``https`` for github and similar repositories).

If authentication is needed to access the repository, *Add* the configuration.

![Add repository](/assets/img/settings.png)

If the repository is successfully added, you can now also see its collections in the ``All collections`` tab and install them from there.

The table below lists the types of repositories that can be added.

| Type | URL Example | Description |
| :--- | ----------- | :---------- |
| GitHub |  <https://github.com/qgis/QGIS-Resources.git> | Works only for public repositories |
| GitLab |  <https://gitlab.com/test/MyResources.git> |  Works only for public repositories |
| Bitbucket |  <https://bitbucket.org/gisuser/qgis-style-repo-useful.git> | Works only for public repositories |
| File system | file:///home/gisuser/dev/repositories/qgis_resources | Pointing to the repository root in your local file system HTTP(s) with zip collections | https://yourdomain.com/qgis/QGIS-Resources | Providing the base URL of the repository. Metadata must be available, with this URL: [base_url]/metadata.ini. The collections should be in [base_url]/collections/[collection_name].zip |

Adding a repository (and loading one or more of its collections) means that a copy of the repository will be placed in the local file system (under ``resource_sharing/repositories`` in the QGIS user directory).
