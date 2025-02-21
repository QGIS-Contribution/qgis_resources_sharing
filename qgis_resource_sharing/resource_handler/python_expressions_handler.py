import logging
import shutil
from pathlib import Path

from processing.tools.system import mkdir, userFolder

from qgis_resource_sharing.resource_handler.base import BaseResourceHandler

PYTHON_EXPRESSIONS_FOLDER = "python/expressions"
PYTHON_EXPRESSIONS = (
    "python_expressions"  # Resource Sharing collection subdirectory name
)
LOGGER = logging.getLogger("QGIS Resource Sharing")


class PythonExpressionsHandler(BaseResourceHandler):
    """Handler for python expressions."""

    IS_DISABLED = False

    def __init__(self, collection_id):
        """Constructor of the base class."""
        BaseResourceHandler.__init__(self, collection_id)
        LOGGER.info("Python Expressions")

    @classmethod
    def dir_name(cls):
        LOGGER.info(f"Expressions folder")
        return PYTHON_EXPRESSIONS

    def install(self):
        """Install the models from the collection.

        Copy the python expressions (*.py) in the directory of the
        Resource Sharing collection to the user's python expressions directory.
        """
        # Return silently if the directory does not exist
        if not Path(self.resource_dir).exists():
            return

        # Handle the python expressions files located in self.resource_dir
        python_expression_files = []
        for item in Path(self.resource_dir).glob("*.py"):
            file_path = Path(self.resource_dir, item)
            python_expression_files.append(file_path)
        valid = 0
        for python_expression_file in python_expression_files:
            LOGGER.info(
                f"Processing installing files {python_expression_file.as_posix()}"
            )
            # Install the python expression file silently
            try:
                shutil.copy(python_expression_file, self.python_expressions_folder())
                valid += 1
            except OSError as e:
                LOGGER.error(
                    "Could not copy python expression '"
                    + str(python_expression_file)
                    + "':\n"
                    + str(e)
                )
        if valid > 0:
            self.refresh_python_expressions_provider()
        self.collection[PYTHON_EXPRESSIONS] = valid

    def uninstall(self):
        """Uninstall the collection's models from the processing toolbox."""
        if not Path(self.resource_dir).exists():
            return
        # Remove the model files that are present in this collection
        for item in Path(self.resource_dir).glob("*.py"):
            python_expression_path = Path(self.python_expressions_folder(), item.name)
            if python_expression_path.exists():
                python_expression_path.unlink()
        self.refresh_python_expressions_provider()

    def refresh_python_expressions_provider(self):
        # for item in Path(self.resource_dir).glob("*.py"):
        #     python_expression_path = Path(self.python_expressions_folder(), item.name)
        #     with open(python_expression_path) as file:
        #         eval(file.read())
        pass

    def default_python_expressions_folder(self):
        """Return the default location of the processing models folder."""
        folder = Path(userFolder(), "..", PYTHON_EXPRESSIONS_FOLDER)
        mkdir(str(folder))
        return str(folder)

    def python_expressions_folder(self):
        """Return the folder where processing expects to find models."""
        # Use the default location
        return self.default_python_expressions_folder()
