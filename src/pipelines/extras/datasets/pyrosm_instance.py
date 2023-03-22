from kedro.io import AbstractDataSet
from pyrosm import OSM


class PyrosmInstance(AbstractDataSet[OSM, None]):
    def __init__(self, filepath: str, credentials: str | None = None):
        """Creates a new instance of ImageDataSet to load / save image data for given filepath.

        Args:
            filepath: The location of the image file to load / save data.
        """
        self._credentials = credentials
        self._filepath = filepath

    def _load(self) -> OSM:
        """Load geocoder."""
        return OSM(self._filepath)

    def _save(self) -> None:
        raise NotImplementedError("Saving is not supported for OSM")
        return None

    def _describe(self):
        return None
