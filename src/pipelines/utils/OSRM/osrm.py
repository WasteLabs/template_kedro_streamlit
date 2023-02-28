"""
Wrapper for converting OSRM json results into pandas data-frames.
"""
import json
import logging
from copy import deepcopy
from typing import Dict, List

import geopandas as gpd
import pandas as pd
from shapely.geometry import LineString

EPSG = "EPSG:4326"


class OsrmRoutePathNormalizer:
    """Convert OSRM route and trip results into data-frames"""

    _osrm_json_results: Dict
    _route_path_type: str
    _route_path_info: dict
    _leg_info: List
    _order_sequence_flag: bool

    def __init__(
        self, osrm_json_results: Dict, route_path_type: str, order_sequence: bool = True
    ):
        self._osrm_json_results = osrm_json_results
        self._route_path_type = route_path_type
        self._check_route_path_type()
        self._order_sequence_flag = order_sequence

    def _check_route_path_type(self):
        if self._route_path_type not in self._osrm_json_results:
            raise ValueError(
                f"Route path type `{self._route_path_type}` not in supplied OSRM results."
            )
        n_entries = len(self._osrm_json_results[self._route_path_type])
        if n_entries > 1:
            logging.warning(
                "Route path object has multiple %i legs. Only first one will be processed.",
                n_entries,
            )

    def _set_route_info(self):
        route_path_info = self._osrm_json_results[self._route_path_type]
        self._route_path_info = route_path_info[0]

    def _set_route_legs(self):
        route_path_info = self._osrm_json_results[self._route_path_type]
        self._leg_info = route_path_info[0]["legs"]

    def _order_sequence(self, waypoint_info):
        if self._order_sequence_flag is True:
            waypoint_info = waypoint_info.sort_values(["route_sequence"]).reset_index(
                drop=True
            )
        return waypoint_info

    def extract_road_snap_info(self):
        """Extract info on where stops were snapped to the road,
        includes lat-lon snapping and distances."""

        def infer_waypoint_index(info: pd.DataFrame) -> pd.DataFrame:
            """Infer travel sequence of road-snap info"""
            if "waypoint_index" not in info.columns:
                info["waypoint_index"] = range(info.shape[0])
            return info

        waypoint_info = pd.DataFrame(self._osrm_json_results["waypoints"])
        waypoint_info[["road_snap_longitude", "road_snap_latitude"]] = waypoint_info[
            "location"
        ].tolist()
        waypoint_info = waypoint_info.drop(columns=["hint", "name", "location"])
        waypoint_info["original_index"] = waypoint_info.index
        waypoint_info = infer_waypoint_index(waypoint_info)
        waypoint_info = waypoint_info.rename(
            columns={
                "waypoint_index": "route_sequence",
                "distance": "road_snap_distance_m",
            }
        )
        waypoint_info = self._order_sequence(waypoint_info)
        return waypoint_info

    def extract_travel_leg_geometry(self) -> gpd.GeoSeries:
        """Extract the geometry path in WKT between all stops."""
        legs = deepcopy(self._leg_info)
        for i, leg in enumerate(legs):
            leg["__id"] = i
        leg_steps = pd.json_normalize(legs, record_path="steps", meta="__id")
        leg_steps = (
            leg_steps.groupby("__id")
            .agg(geometry=("geometry.coordinates", "sum"))
            .reset_index()
        )
        geometry = leg_steps["geometry"].apply(LineString)
        return geometry

    def extract_travel_leg_duration_distance(self) -> pd.DataFrame:
        """Extract the travel distance (km) and duration (seconds) between all stops"""
        legs_info_df = pd.DataFrame(self._leg_info)[["duration", "distance"]]
        legs_info_df["distance"] = legs_info_df["distance"] / 1000
        legs_info_df = legs_info_df.rename(
            columns={"duration": "duration_seconds", "distance": "distance_km"}
        )
        return legs_info_df

    def extract_travel_leg_info(self) -> gpd.GeoDataFrame:
        """Extract travel metrix and path info."""
        self._check_route_path_type()
        self._set_route_legs()
        leg_kpis = self.extract_travel_leg_duration_distance()
        leg_paths = self.extract_travel_leg_geometry()
        leg_info = gpd.GeoDataFrame(leg_kpis, geometry=leg_paths, crs=EPSG)
        leg_info["travel_sequence"] = range(leg_info.shape[0])
        return leg_info

    def extract_travel_summary_info(self) -> gpd.GeoDataFrame:
        """Extract route summary info, like total distance, duration and path."""
        self._check_route_path_type()
        self._set_route_info()
        route_path_info = self._route_path_info
        total_distance_km = route_path_info["distance"] / 1000
        total_duration_hours = route_path_info["duration"] / 3600
        route_path = route_path_info["geometry"]["coordinates"]
        geometry = LineString(route_path)
        route_summary = pd.DataFrame(
            [
                {
                    "total_distance_km": total_distance_km,
                    "total_travel_duration_hours": total_duration_hours,
                    "geometry": geometry,
                }
            ]
        )
        route_summary = gpd.GeoDataFrame(
            route_summary, geometry=route_summary["geometry"], crs=EPSG
        )
        return route_summary
