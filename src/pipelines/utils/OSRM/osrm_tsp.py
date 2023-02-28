"""
Generate OSRM tsp routes.
"""
import logging

import numpy as np
import pandas as pd
import requests
from shapely.geometry import LineString

logger = logging.getLogger(__name__)


def solve_single_tsp(
    route: pd.DataFrame,
    lon_col: str = "longitude",
    lat_col: str = "latitude",
    osrm_port: str = "http://router.project-osrm.org",
) -> dict:
    if osrm_port[-1] == "/":
        osrm_port = osrm_port[:-1]
    coordinates = ";".join(route[[lon_col, lat_col]].astype(str).agg(",".join, axis=1))
    request = f"{osrm_port}/trip/v1/driving/{coordinates}?roundtrip=false&source=first&destination=last&steps=true&annotations=true&overview=full&geometries=geojson"
    with requests.get(request) as req:
        results = req.json()
    return results


def assign_route_sequence_info_to_route(results: dict) -> np.array:
    if (
        "message" in results
        and results["message"] == "Number of coordinates needs to be at least two."
    ):
        logger.warning("There should be more than one stop per route.")
        waypoints = []
    else:
        route_sequence = pd.DataFrame(results["waypoints"])
        n_trip = route_sequence["trips_index"].nunique()
        if n_trip > 1:
            logging.warning(
                f"There are {n_trip} trips present. There were route segments that could not be linked."
            )
        waypoints = route_sequence["waypoint_index"].values
    return waypoints


def extract_travel_leg_duration_distance(results):
    legs_info = pd.DataFrame(results["trips"][0]["legs"])[["duration", "distance"]]
    duration_seconds = np.insert(legs_info["duration"].values, 0, 0)
    distance_km = np.insert((legs_info["distance"] / 1000).values, 0, 0)
    return {
        "duration_seconds": duration_seconds,
        "distance_km": distance_km,
    }


def extract_travel_leg_geometry(results):
    legs = results["trips"][0]["legs"]
    for i, leg in enumerate(legs):
        leg["__id"] = i
    leg_steps = pd.json_normalize(legs, record_path="steps", meta="__id")
    leg_steps = (
        leg_steps.groupby("__id")
        .agg(geometry=("geometry.coordinates", "sum"))
        .reset_index()
    )
    geometry = np.insert(leg_steps["geometry"].apply(LineString).values, 0, np.nan)
    return geometry


class OsrmTspRoutes:
    """Calculate tsp routes using osrm project api.

    Args:
        assigned_stops_df: data-frame with assigned stops per `route_id` to sequence.
        depot_df: data-frame with info on the depot where routes start and end at
        stops_limit: limit on how many stops can be sequenced, set at 100 with global OSRM API
        osrm_port: port for the osrm calls, default is "http://router.project-osrm.org", just no "/" at the end.

    Examples:

        Generate tsp sequences for 100 random stops, randomly assigned to one of 4 vehicles.

        '''python
        np.random.seed(10)
        lon = -0.5 + np.random.rand(100)
        lat = -0.5 + np.random.rand(100)
        route_id = np.random.randint(0, 5, 100)
        random_lonlat_stops = pd.DataFrame(
            {
                "longitude": lon,
                "latitude": lat,
                "route_id": route_id,
                "activity_type": ["PIKCUP"] * 100,
            }
        )
        stops = random_lonlat_stops.iloc[1:]
        depot = random_lonlat_stops.iloc[:1]
        osrm_tsp = OsrmTspRoutes(stops, depot)
        tsp_routes = osrm_tsp.generate_all_tsp_routes()
        print(tsp_routes)
        print(tsp_routes["route_id"].value_counts())
        '''
    """

    _assigned_stops_df: pd.DataFrame
    _depot_stop_df: pd.DataFrame
    _stops_limit: int
    _tsp_routes: pd.DataFrame
    _osrm_port: str

    def __init__(
        self,
        assigned_stops_df: pd.DataFrame,
        depot_df: pd.DataFrame,
        stops_limit: int = 100,
        osrm_port: str = "http://router.project-osrm.org",
    ):
        self._assigned_stops_df = assigned_stops_df.copy()
        self._depot_stop_df = depot_df.copy()
        self._stops_limit = stops_limit
        self._osrm_port = osrm_port

    def extract_first_depot(self):
        n_depots = self._depot_stop_df.shape[0]
        if n_depots > 1:
            logger.warning(
                f"There are {n_depots} depots specified, only the first one is returned."
            )
            self._depot_stop_df = self._depot_stop_df.iloc[:1]

    def _generate_depot_stops_dataframe(
        self, route_stops: pd.DataFrame
    ) -> pd.DataFrame:
        route_id = route_stops["route_id"].unique()
        if route_id.shape[0] > 1:
            logging.warning(
                "Multiple routes specified, not sure how to allocated `route_id` now, so will use first."
            )
        depot_id = route_stops["depot_id"].unique()
        if route_id.shape[0] > 1:
            logging.warning(
                "Multiple depots specified, not sure how to allocated `depot_id` now, so will use first."
            )
        depot_id = depot_id[0]
        route_id = route_id[0]
        route_depot = self._depot_stop_df.loc[
            self._depot_stop_df["depot_id"] == depot_id
        ]
        if route_depot.shape[0] == 0:
            logger.warning(
                f"No depot found for depot_id {depot_id}, will use first depot in data-frame."
            )
        depot_start_df = route_depot.assign(
            activity_type="START_AT_DEPOT", route_id=route_id
        )
        depot_end_df = route_depot.assign(
            activity_type="RETURN_TO_DEPOT", route_id=route_id
        )
        route_stops = route_stops.assign(activity_type="PICKUP")
        full_route = pd.concat([depot_start_df, route_stops, depot_end_df])
        return full_route

    def generate_tsp_route(self, route: pd.DataFrame, route_id=None) -> pd.DataFrame:
        """Calculate TSP sequence for single route

        Args:
            route: routes to sequence, with lat-lon coordinates and `"route_id"`.
            route_id: id over which routes can be filtered.

        Returns:
            route data-frame with `"route_sequence"` column based on the TSP routes.
        """
        if route_id is not None:
            route = route.loc[route["route_id"] == route_id]
        else:
            route_id = route["route_id"].unique()[0]
        route = self._generate_depot_stops_dataframe(route)
        if route.shape[0] <= 1:
            logger.warning(
                f"Route has {route.shape[0]} <= 1 stops, so skipping sequence generation."
            )
            return route
        n_stops = route.shape[0]
        logger.info(
            f"Generating route sequence for `route_id` {route_id} with {n_stops} stops."
        )

        if route.shape[0] > self._stops_limit:
            logger.warning(
                f"Route has {route.shape[0]} > {self._stops_limit} stops which may result in OSRM errors."
            )

        results = solve_single_tsp(route, osrm_port=self._osrm_port)
        tsp_sequence = assign_route_sequence_info_to_route(results)
        tsp_route = (
            route.assign(route_sequence=tsp_sequence)
            .sort_values("route_sequence")
            .assign()
        )
        duration_distance = extract_travel_leg_duration_distance(results)
        paths = extract_travel_leg_geometry(results)

        tsp_route = tsp_route.assign(
            duration_seconds=duration_distance["duration_seconds"],
            distance_km=duration_distance["distance_km"],
            geometry=paths,
        )

        return tsp_route

    def generate_all_tsp_routes(self) -> pd.DataFrame:
        """Generate TSP sequences for all routes."""
        self._tsp_routes = (
            self._assigned_stops_df.groupby(["route_id"])
            .apply(self.generate_tsp_route)
            .reset_index(drop=True)
        )
        return self._tsp_routes


if __name__ == "__main__":
    np.random.seed(10)
    lon = -0.5 + np.random.rand(100)
    lat = -0.5 + np.random.rand(100)
    route_id = np.random.randint(0, 5, 100)
    random_lonlat_stops = pd.DataFrame(
        {
            "longitude": lon,
            "latitude": lat,
            "route_id": route_id,
            "activity_type": ["PICKUP"] * 100,
        }
    )
    stops = random_lonlat_stops.iloc[1:]
    depot = random_lonlat_stops.iloc[:1]
    osrm_tsp = OsrmTspRoutes(stops, depot)
    tsp_routes = osrm_tsp.generate_all_tsp_routes()
    print(tsp_routes)
    print(tsp_routes["route_id"].value_counts())
