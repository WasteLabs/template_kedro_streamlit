"""
Retrieve and return OSRM table info. See https://project-osrm.org/docs/v5.24.0/api/#table-service
"""

from pprint import pprint
from typing import List, Tuple, Union

import numpy as np
import pandas as pd
import requests

PORT_TYPE_MAPPING_DEFAULT = "http://router.project-osrm.org"
PORT_TYPE_MAPPING_DEFAULT_STOP_LIMIT = 100


def get_time_dist_matrix(
    data: pd.DataFrame,
    endpoint: str = None,
    lon_col: str = "longitude",
    lat_col: str = "latitude",
    timeout: float = 120,
    slow_down: float = 1,
) -> Tuple[np.ndarray, np.ndarray]:
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

    if endpoint is None:
        if data.shape[0] > PORT_TYPE_MAPPING_DEFAULT_STOP_LIMIT:
            raise ValueError(
                f"Cannot do more than {PORT_TYPE_MAPPING_DEFAULT_STOP_LIMIT} points with default port"
            )
        endpoint = PORT_TYPE_MAPPING_DEFAULT

    table_end_point = f"{endpoint}/table/v1/driving/"
    url = _construct_url_using_coordinates(data, table_end_point)
    api_response = _send_get_request(url)
    time_matrix = _get_time_matrix(api_response, slow_down)
    distance_matrix = _get_distance_matrix(api_response)

    return time_matrix, distance_matrix


def get_interstops_time_distance(
    time_matrix: np.ndarray,
    distance_matix: np.ndarray,
) -> Tuple[List[int], List[int]]:
    """
    Function extracts from matrices spatial & time distance between each stops
    Args:
    time_matrix: OSRM time distance matrix
    distance_matrix: OSRM distance matrix
    Returns:
    time distance: stop_time[i] - stop_time[i-1]
    spatial distance: stop_distance[i] - stop_distance[i-1]
    """

    def _get_stopwise_measures(matrix: np.ndarray):
        return [0] + list(np.diag(matrix, k=1))

    travel_time = _get_stopwise_measures(time_matrix)
    travel_dist = _get_stopwise_measures(distance_matix)

    return travel_time, travel_dist


if __name__ == "__main__":
    stop_test = pd.read_csv(
        "data/testing/force_assign_milti_job_route_payload_unassigned_stops_df_test.csv"
    )
    (time_output, distance_output) = get_time_dist_matrix(stop_test.iloc[:10])
    pprint(time_output)
    pprint(distance_output)
    (time_consec, distance_consec) = get_interstops_time_distance(
        time_output, distance_output
    )
    pprint(time_consec)
    pprint(distance_consec)
