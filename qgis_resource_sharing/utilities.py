import logging
import ntpath
from pathlib import Path

from ext_libs.pathvalidate import sanitize_filename
from qgis.core import Qgis, QgsApplication, QgsSettings
from qgis.PyQt.QtCore import QDir

from qgis_resource_sharing import config
from qgis_resource_sharing.__about__ import DIR_PLUGIN_ROOT, __title__

LOGGER = logging.getLogger(__title__)

SUPPORTED_RESOURCES_MAP = {
    "svg": "SVG",
    "style": "Layer style (QML) file",
    "symbol": "Symbol (XML) file",
    "expressions": "Expression (JSON) file",
    "processing": "Processing script",
    "models": "Processing model",
    "rscripts": "R script",
    "checklists": "Dataset QA Workbench checklist",
    "python_expressions": "Python Expressions",
}


def resources_path(*args):
    """Get the absolute path to resources in the resources dir.

    :param args List of path elements e.g. ['img', 'logos', 'image.png']
    :type args: list

    :return: Absolute path to the resources folder.
    :rtype: Path
    """
    path = DIR_PLUGIN_ROOT / "resources"
    for item in args:
        path = path / item
    return path


def ui_path(*args):
    """Get the absolute path to the ui file from the UI dir.

    :param args List of path elements e.g. ['manage_repository.ui]
    :type args: list

    :return: Absolute path to the ui file.
    :rtype: Path
    """
    path = Path(__file__).parent
    path = path / "gui" / "ui"
    for item in args:
        path = path / item
    return path


def user_expressions_group():
    """Get the user expressions group."""
    return "/expressions/user"


def repo_settings_group():
    """Get the settings group for Resource Sharing Dialog."""
    return "/ResourceSharing/repository"


def resource_sharing_group():
    """Get the settings group for the local collection directories."""
    return "/ResourceSharing"


def repositories_cache_path():
    """Get the path to the repositories cache."""
    return Path(
        QgsApplication.qgisSettingsDirPath(), "resource_sharing", "repositories_cache"
    )


def local_collection_root_dir_key():
    """The QSettings key for the local collections root dir."""
    return "localCollectionDir"


def default_local_collection_root_dir():
    return Path(QgsApplication.qgisSettingsDirPath(), "resource_sharing", "collections")


def local_collection_path(id=None):
    """Get the path to the local collection dir.

    If id is not passed, it will just return the root dir of the
    collections.
    """
    settings = QgsSettings()
    settings.beginGroup(resource_sharing_group())
    if settings.contains(local_collection_root_dir_key()):
        # The path is defined in the settings - use it
        lcPath = Path(settings.value(local_collection_root_dir_key()))
    else:
        # The path is not defined in the settings
        if old_local_collection_path().exists():
            # The pre-version 0.10 directory exists - so use it
            lcPath = old_local_collection_path()
        else:
            # Use the new default directory
            lcPath = default_local_collection_root_dir()
        LOGGER.info("Setting the collection path to " + str(lcPath))
        settings.setValue(local_collection_root_dir_key(), str(lcPath))
    settings.endGroup()
    # If the directory does not exist, create it!
    if not lcPath.exists():
        LOGGER.debug("coll_mgr - creating local collection dir: " + str(lcPath))
        lcPath.mkdir(parents=True, exist_ok=True)
    path = lcPath
    if id:
        collection_name = config.COLLECTIONS[id]["name"]
        sane_name = sanitize_filename(collection_name)
        repository_name = config.COLLECTIONS[id]["repository_name"]
        sane_repo_name = sanitize_filename(repository_name)
        # Use repository name instead of hash
        dir_name = "%s (%s)" % (sane_name, sane_repo_name)
        path = lcPath / dir_name
        # Check if the "old" directory name exists
        # (should eventuall be removed)
        old_dir_name = "%s" % (id)
        old_path = lcPath / old_dir_name
        if old_path.exists():
            try:
                old_path.rename(path)
            except Exception:
                pass
    return path


def old_local_collection_path(id=None):
    """Get the path to the old local collection dir.
    (in case we would like to help the users migrate)
    If id is not passed, it will just return the root dir of the
    collections.
    """
    path = Path(QDir.homePath()) / "QGIS" / "Resource Sharing"
    if id:
        collection_name = config.COLLECTIONS[id]["name"]
        dir_name = "%s (%s)" % (collection_name, id)
        path = path / dir_name
    return path


def path_leaf(path):
    head, tail = ntpath.split(path)
    return tail or ntpath.basename(head)


def qgis_version():
    """Get the version of QGIS.

    :returns: QGIS Version where 30400 represents QGIS 3.4 etc.
    :rtype: int
    """
    version = str(Qgis.QGIS_VERSION_INT)
    version = int(version)
    return version
