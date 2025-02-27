import csv
import logging
import pickle

from qgis.core import QgsSettings
from qgis.PyQt.QtCore import QObject, QTemporaryFile

from qgis_resource_sharing import config
from qgis_resource_sharing.__about__ import __title__
from qgis_resource_sharing.collection_manager import CollectionManager
from qgis_resource_sharing.config import CollectionStatus
from qgis_resource_sharing.exception import MetadataError
from qgis_resource_sharing.network_manager import NetworkManager
from qgis_resource_sharing.repository_handler import BaseRepositoryHandler
from qgis_resource_sharing.utilities import (
    local_collection_path,
    repo_settings_group,
    repositories_cache_path,
)

LOGGER = logging.getLogger(__title__)


class RepositoryManager(QObject):
    """Class to handle repositories."""

    DIRECTORY_URL = (
        "https://raw.githubusercontent.com/qgis/QGIS-Resources/master/directory.csv"
    )

    def __init__(self):
        """Constructor.

        ..note:
        - Directories is a list of repositories. It is stored in the
        settings. The data structure of directories:
        self._directories = {
            'QGIS Official Repository': {
                'url': 'git@github.com:anitagraser/QGIS-style-repo-dummy.git',
                'auth_cfg': '0193jkad'
             }
        }

        - Repositories is a dictionary of repositories with all their
        collections. The data structure of repositories:
        self._repositories = {
            repo_name: [{
                'register_name': collection,
                'author': author,
                'author_email': email,
                'repository_url': self.url,
                'status': CollectionStatus.NOT_INSTALLED,
                'name': parser.get(collection, 'name'),
                'tags': parser.get(collection, 'tags'),
                'description': parser.get(collection, 'description'),
                'qgis_min_version': '2.0',
                'qgis_max_version': '2.99'
                'preview': ['preview/image1.png', 'preview/image2.png']
            },
            .... //other collections from this repository
            ],
            ... //other repository
        }
        """
        QObject.__init__(self)
        # Online directories from the DIRECTORY_URL
        self._online_directories = {}
        # Registered directories
        self._directories = {}
        # Registered repositories
        self._repositories = {}
        # Collection manager instance to deal with collections
        self._collections_manager = CollectionManager()
        # Load repositories from cache
        self.load_repositories()
        # Fetch online directories
        self.fetch_online_directories()
        # Load directory of repositories from settings
        self.load_directories()

    @property
    def directories(self):
        """Directories contains all the repositories (name and URL)
        registered in setting.

        :returns: Dictionary of repositories registered
        :rtype: dict
        """
        return self._directories

    def fetch_online_directories(self):
        """Fetch online directory of repositories."""
        downloader = NetworkManager(self.DIRECTORY_URL)
        status, _ = downloader.fetch()
        if status:
            directory_file = QTemporaryFile()
            if directory_file.open():
                directory_file.write(downloader.content)
                directory_file.close()
            with open(directory_file.fileName()) as csv_file:
                reader = csv.DictReader(csv_file, fieldnames=("name", "url"))
                for row in reader:
                    repName = row["name"]
                    repUrl = row["url"]
                    # Check name and URL for None before stripping and adding
                    if repName is not None and repUrl is not None:
                        self._online_directories[row["name"]] = repUrl.strip()
                    else:
                        if repName is None:
                            # No name
                            LOGGER.warning("Missing name for repository" " - not added")
                        else:
                            # No URL
                            LOGGER.warning(
                                "Missing URL for repository"
                                + str(row["name"])
                                + " - not added"
                            )
            # Save to settings
            settings = QgsSettings()
            settings.beginGroup(repo_settings_group())
            settings.setValue("online_directories", self._online_directories)
            settings.endGroup()
        else:
            # Use settings
            settings = QgsSettings()
            settings.beginGroup(repo_settings_group())
            self._online_directories = settings.value("online_directories", {})
            settings.endGroup()

    def load_directories(self):
        """Update the repository directory."""
        self._directories = {}
        settings = QgsSettings()
        settings.beginGroup(repo_settings_group())
        # Loop through the repositories from the official directory
        for online_dir_name in self._online_directories:
            # Check if the repository is already present
            repo_present = False
            for repo_name in settings.childGroups():
                url = settings.value(repo_name + "/url", "", type=str)
                if url == self._online_directories[online_dir_name]:
                    repo_present = True
                    break
                if online_dir_name == repo_name:
                    repo_present = True
                    nameWarn = (
                        "The repository " + repo_name + " is masking "
                        "an official repository with the same name"
                    )
                    LOGGER.warning(nameWarn)
                    break
            if not repo_present:
                try:
                    self.add_directory(
                        online_dir_name, self._online_directories[online_dir_name]
                    )
                except Exception as exc:
                    LOGGER.error(
                        f"Error occured adding '{online_dir_name}' repository. Trace: {exc}"
                    )
                    continue

        for repo_name in settings.childGroups():
            self._directories[repo_name] = {}
            url = settings.value(repo_name + "/url", "", type=str)
            self._directories[repo_name]["url"] = url
            auth_cfg = settings.value(repo_name + "/auth_cfg", "", type=str).strip()
            self._directories[repo_name]["auth_cfg"] = auth_cfg
        settings.endGroup()

    def add_directory(self, repo_name, url, auth_cfg=None):
        """Add a directory to settings and add the collections from that repo.

        :param repo_name: The name of the repository
        :type repo_name: str

        :param url: The URL of the repository
        :type url: str
        """
        repo_handler = BaseRepositoryHandler.get_handler(url)
        if repo_handler is None:
            LOGGER.warning("There is no handler available for URL '" + str(url) + "'!")
        if auth_cfg:
            repo_handler.auth_cfg = auth_cfg
        # Fetch metadata
        status, fetcherror = repo_handler.fetch_metadata()
        if status:
            # Parse metadata
            try:
                collections = repo_handler.parse_metadata()
            except MetadataError as me:
                metadata_warning = (
                    "Error parsing metadata for " + str(repo_name) + ":\n" + str(me)
                )
                LOGGER.warning(metadata_warning)
                return False, metadata_warning
            # Add the repository and its collections
            self._repositories[repo_name] = collections
            self.rebuild_collections()
            # Add to QgsSettings
            settings = QgsSettings()
            settings.beginGroup(repo_settings_group())
            settings.setValue(repo_name + "/url", url)
            if auth_cfg:
                settings.setValue(repo_name + "/auth_cfg", auth_cfg)
            settings.endGroup()
            # Serialize repositories every time we successfully added a repo
            self.serialize_repositories()
        return status, fetcherror

    def edit_directory(
        self, old_repo_name, new_repo_name, old_url, new_url, new_auth_cfg
    ):
        """Edit the directory of repositories and update the
        collections.
        Also used to reload repositories (old == new for url and repo_name)

        :param old_repo_name: The old name of the repository
        :type old_repo_name: str
        :param new_repo_name: The new name of the repository
        :type new_repo_name: str
        :param old_url: The old URL of the repository
        :type old_url: str
        :param new_url: The new URL of the repository
        :type new_url: str
        :param new_auth_cfg: The auth config id.
        :type new_auth_cfg: str
        :return: (status, error)
        :rtype: (boolean, string)
        """
        old_collections = self._repositories.get(old_repo_name, [])
        if (old_repo_name != new_repo_name) and (old_url == new_url):
            # Renaming a repository (same URL)
            for old_collection in old_collections:
                coll_id = self._collections_manager.get_collection_id(
                    old_collection["register_name"], old_collection["repository_url"]
                )
                old_path = local_collection_path(coll_id)
                # Update the repository name for this collection
                config.COLLECTIONS[coll_id]["repository_name"] = new_repo_name
                new_path = local_collection_path(coll_id)
                # If the repository is renamed (same URL), the directories
                # of its collections should be renamed accordingly (so that
                # they remain accessible)
                if old_path.exists():
                    old_path.rename(new_path)
            new_collections = old_collections
            status = True
            fetcherror = ""
        else:
            # old_repo_name == new_repo_name and old_url == new_url
            # or new_url != old_url
            # Fetch the metadata (metadata.ini) from the new url
            repo_handler = BaseRepositoryHandler.get_handler(new_url)
            if repo_handler is None:
                repo_warning = "No handler for URL '" + str(new_url) + "'!"
                LOGGER.warning(repo_warning)
                return (False, repo_warning)
            if new_auth_cfg:
                repo_handler.auth_cfg = new_auth_cfg
            status, fetcherror = repo_handler.fetch_metadata()
            if status:
                # Parse metadata
                try:
                    new_collections = repo_handler.parse_metadata()
                except MetadataError as me:
                    metadata_warning = (
                        "Error parsing metadata for "
                        + str(new_repo_name)
                        + ":\n"
                        + str(me)
                    )
                    LOGGER.warning(metadata_warning)
                    return (False, metadata_warning)
                    # raise MetadataError(metadata_warning)
                # Get all the installed collections from the old repository
                installed_old_collections = []
                for old_collection in old_collections:
                    if old_collection["status"] == CollectionStatus.INSTALLED:
                        installed_old_collections.append(old_collection)
                # Handling installed collections
                # An old collection that is present in the new location
                # (URL) is identified by its register name.
                # Cases for installed collections:
                # 1. Old collection exists in the new, same URL: use the new
                # one, else: update the status to INSTALLED
                # 2. Old collection exists in the new, different URL: keep them
                # both (add the old one). Because they should be treated as
                # different collections
                # 3. Old collection doesn't exist in the new, same URL: keep
                # the old collection
                # 4. Old collection doesn't exist in the new, different URL:
                # same as 3
                for installed_collection in installed_old_collections:
                    reg_name = installed_collection["register_name"]
                    is_present = False
                    for n_coll in new_collections:
                        # Look for collections that are already present
                        if n_coll["register_name"] == reg_name:
                            # Already present
                            is_present = True
                            if old_url == new_url:
                                # Set the status to installed
                                n_coll["status"] = CollectionStatus.INSTALLED
                                # Keep the collection statistics
                                for key in installed_collection.keys():
                                    if key in [
                                        "models",
                                        "processing",
                                        "rscripts",
                                        "style",
                                        "svg",
                                        "symbol",
                                        "expressions",
                                    ]:
                                        n_coll[key] = installed_collection[key]
                            else:
                                # Different repository URLs, so append
                                new_collections.append(installed_collection)
                            break
                    if not is_present:
                        new_collections.append(installed_collection)
        # Remove the old repository and add the new one
        self._repositories.pop(old_repo_name, None)
        self._repositories[new_repo_name] = new_collections
        self.rebuild_collections()
        # Update QgsSettings
        settings = QgsSettings()
        settings.beginGroup(repo_settings_group())
        settings.remove(old_repo_name)
        settings.setValue(new_repo_name + "/url", new_url)
        settings.setValue(new_repo_name + "/auth_cfg", new_auth_cfg)
        settings.endGroup()
        # Serialize repositories every time we successfully edited repo
        self.serialize_repositories()
        return status, fetcherror

    def remove_directory(self, repo_name):
        """Remove a directory and all its collections.

        :param repo_name: The old name of the repository
        :type repo_name: str
        """
        self._repositories.pop(repo_name, None)
        self.rebuild_collections()
        # Remove repository from QgsSettings
        settings = QgsSettings()
        settings.beginGroup(repo_settings_group())
        settings.remove(repo_name)
        settings.endGroup()
        # Serialize repositories
        self.serialize_repositories()

    def reload_directory(self, repo_name, url, auth_cfg):
        """Re-fetch the directory and update the collections registry.

        :param repo_name: The name of the repository
        :type repo_name: str

        :param url: The URL of the repository
        :type url: str
        """
        # We are basically editing a directory (same repo name and url)
        status, editerror = self.edit_directory(
            repo_name, repo_name, url, url, auth_cfg
        )
        return status, editerror

    def rebuild_collections(self):
        """Rebuild the collections for all the repositories."""
        config.COLLECTIONS = {}
        for repo in self._repositories.keys():
            repo_collections = self._repositories[repo]
            for collection in repo_collections:
                collection_id = self._collections_manager.get_collection_id(
                    collection["register_name"], collection["repository_url"]
                )
                collection["repository_name"] = repo
                config.COLLECTIONS[collection_id] = collection
                # Get the collection path (updating if neccessary)
                collection_path = local_collection_path(collection_id)
                # Check the file system to see if the collection exists.
                # If not, also uninstall its resources
                current_status = config.COLLECTIONS[collection_id]["status"]
                if current_status == CollectionStatus.INSTALLED:
                    if not collection_path.exists():
                        # Uninstall the collection
                        self._collections_manager.uninstall(collection_id)

    def resync_repository(self):
        """Resync from collections as opposed to rebuild_collections."""
        for repo in self._repositories.keys():
            repo_collections = self._repositories[repo]
            synced_repo_collections = []
            for collection in repo_collections:
                collection_id = self._collections_manager.get_collection_id(
                    collection["register_name"], collection["repository_url"]
                )
                synced_repo_collections.append(config.COLLECTIONS[collection_id])
            self._repositories[repo] = synced_repo_collections

    def serialize_repositories(self):
        """Save repositories to cache."""
        if not repositories_cache_path().parent.exists():
            repositories_cache_path().parent.mkdir(parents=True)
        self.resync_repository()
        with open(str(repositories_cache_path()), "wb") as f:
            pickle.dump(self._repositories, f)

    def load_repositories(self):
        """Load repositories from cache and rebuild collections."""
        repo_collections = {}
        if repositories_cache_path().exists():
            with open(str(repositories_cache_path()), "rb") as f:
                repo_collections = pickle.load(f)
        self._repositories = repo_collections
        self.rebuild_collections()
