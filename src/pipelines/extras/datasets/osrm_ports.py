from kedro.io import AbstractDataSet


class OsrmPorts(AbstractDataSet[str, None]):
    def __init__(self, credentials: str):
        """Creates a new instance of ImageDataSet to load / save image data for given filepath.

        Args:
            filepath: The location of the image file to load / save data.
        """
        self._credentials = credentials

    def _load(self) -> str:
        """Load OSRM access ports."""
        return self._credentials

    def _save(self) -> None:
        raise NotImplementedError("Saving is not supported for OSRM access ports")
        return None

    def _describe(self):
        return None
