"""
Retrieve and return OSRM table info. See https://project-osrm.org/docs/v5.24.0/api/#table-service
"""

from typing import Dict, Union

import numpy as np
import pandas as pd
import requests

PORT_TYPE_MAPPING_DEFAULT_STOP_LIMIT = 1000


def get_time_dist_matrix(
    data: pd.DataFrame,
    endpoint: str = None,
    lon_col: str = "longitude",
    lat_col: str = "latitude",
    timeout: float = 120,
    slow_down: float = 1,
) -> Dict[str, np.ndarray]:
    """
    Calculate the time (seconds) and distance (meters) of the shortest-time path between all stops.
    Args:
    data: data-frame with lat-lon coordinates
    port: port to OSRM RestAPI
    lon: column name of latitude coordinate
    lat: column name of longitude coordinate
    timeout: time before time-out error occurs for API
    slow_down: factor by which to slow-down travel speed and increase duration.
    Return:
    time_matrix: short-time path time (seconds) between stops i and j.
    distance_matrix: short-time path distance (meters) between stops i and j.
    """

    def _construct_url_using_coordinates(data: pd.DataFrame, endpoint: str) -> str:
        """
        Function takes lat & lon & builds url request
        """
        coordinates = (
            data[lon_col].astype(str) + "," + data[lat_col].astype(str)
        ).tolist()
        coordinates = ";".join(coordinates)
        url = f"{endpoint}{coordinates}?annotations=distance,duration"
        return url

    def _send_get_request(url: str) -> dict:
        with requests.Session() as session:
            response_content = session.get(
                url, timeout=timeout, headers={"Connection": "close"}
            ).json()
        return response_content

    def _get_time_matrix(
        api_response: dict, slow_down: Union[float, int]
    ) -> np.ndarray:
        time_matrix = np.array(api_response["durations"]) * slow_down
        return time_matrix

    def _get_distance_matrix(api_response) -> np.ndarray:
        distance_matrix = np.array(api_response["distances"])
        return distance_matrix

    table_end_point = f"{endpoint}/table/v1/driving/"
    url = _construct_url_using_coordinates(data, table_end_point)
    api_response = _send_get_request(url)
    time_matrix = _get_time_matrix(api_response, slow_down)
    distance_matrix = _get_distance_matrix(api_response)

    return {"time_matrix": time_matrix, "distance_matrix": distance_matrix}
