from geopy.geocoders import GoogleV3
from kedro.io import AbstractDataSet


class GmapsGeocoder(AbstractDataSet[GoogleV3, None]):
    def __init__(self, credentials: str):
        """Creates a new instance of ImageDataSet to load / save image data for given filepath.

        Args:
            filepath: The location of the image file to load / save data.
        """
        self._credentials = credentials

    def _load(self) -> GoogleV3:
        """Load geocoder."""
        return GoogleV3(api_key=self._credentials)

    def _save(self) -> None:
        raise NotImplementedError("Saving is not supported for GmapsGeocoder")
        return None

    def _describe(self):
        return None
