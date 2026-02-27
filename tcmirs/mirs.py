"""
mirs.py
-------
Functions for identifying and loading MIRS satellite granule files that
overlap a tropical cyclone track in space and time.
"""

from __future__ import annotations

import os

import pandas as pd
import pytz
import xarray as xr
from shapely import wkt
from shapely.geometry import Point

from .config import TIME_WINDOW_HOURS, IMG_VARS_TO_REMOVE, SND_VARS_TO_KEEP


def _granule_overlaps_track_point(
    ds: xr.Dataset,
    lat: float,
    lon_180: float,
    t_behind: "pd.Timestamp",
    t_ahead: "pd.Timestamp",
    require_east_of_dateline: bool = True,
) -> bool:
    """
    Return True if a MIRS granule's time window and spatial footprint
    contain the given track point.

    Parameters
    ----------
    ds:
        Open MIRS xarray Dataset.
    lat, lon_180:
        Storm centre coordinates (longitude in -180/180 range).
    t_behind, t_ahead:
        UTC-aware timestamps defining the acceptable time window.
    require_east_of_dateline:
        If ``True`` (default), skip granules whose first FOV longitude is
        >= 0, which filters out wrap-around granules for Atlantic storms.
        Set to ``False`` for storms that cross the dateline.
    """
    start = pd.to_datetime(ds.attrs["time_coverage_start"])
    end = pd.to_datetime(ds.attrs["time_coverage_end"])

    if not (t_behind <= start and t_ahead >= end):
        return False

    if require_east_of_dateline:
        if ds.attrs["geospatial_first_scanline_first_fov_lon"] >= 0:
            return False

    polygon_val = wkt.loads(ds.attrs["geospatial_bounds"])
    point = Point(float(lon_180), float(lat))
    return point.within(polygon_val)


def find_mirs_files(
    track: pd.DataFrame,
    mirs_dir: str,
    time_window_hours: int = TIME_WINDOW_HOURS,
    require_east_of_dateline: bool = True,
    track_indices: list[int] | None = None,
) -> tuple[list[str], list[str]]:
    """
    Identify MIRS IMG and SND granule files that overlap the storm track.

    Parameters
    ----------
    track:
        DataFrame returned by :func:`ibtracs.get_storm_track`.
    mirs_dir:
        Directory containing MIRS ``.nc`` files.
    time_window_hours:
        Hours either side of each track point to accept a granule.
    require_east_of_dateline:
        Passed through to :func:`_granule_overlaps_track_point`.
    track_indices:
        If provided, only process these row indices of ``track``.
        Useful for testing without looping the full lifecycle.

    Returns
    -------
    tuple[list[str], list[str]]
        ``(img_files, snd_files)`` — sorted lists of matching filenames.
    """
    mirs_files = os.listdir(mirs_dir)
    indices = track_indices if track_indices is not None else range(len(track))
    matched: set[str] = set()

    for ipt in indices:
        t_val = track["ISO_TIME"].iloc[ipt]
        lat_val = track["LAT"].iloc[ipt]
        lon_val = track["LON_180"].iloc[ipt]

        print(f"  Checking track point {ipt}: {t_val}")

        t_ahead = pytz.utc.localize(t_val + pd.to_timedelta(time_window_hours, unit="h"))
        t_behind = pytz.utc.localize(t_val - pd.to_timedelta(time_window_hours, unit="h"))

        for fname in mirs_files:
            if not fname.endswith(".nc"):
                continue
            fpath = os.path.join(mirs_dir, fname)
            ds = xr.open_dataset(fpath)
            if _granule_overlaps_track_point(
                ds, lat_val, lon_val, t_behind, t_ahead, require_east_of_dateline
            ):
                matched.add(fname)
            ds.close()

    img_files = sorted(f for f in matched if f.startswith("NPR-MIRS-IMG"))
    snd_files = sorted(f for f in matched if f.startswith("NPR-MIRS-SND"))
    return img_files, snd_files


def load_and_merge_mirs(
    img_files: list[str],
    snd_files: list[str],
    mirs_dir: str,
    snd_vars_to_keep: list[str] = SND_VARS_TO_KEEP,
    img_vars_to_remove: list[str] = IMG_VARS_TO_REMOVE,
) -> tuple[xr.Dataset, xr.Dataset]:
    """
    Load and concatenate MIRS IMG and SND granules, applying variable filters.

    Parameters
    ----------
    img_files, snd_files:
        Filenames (not full paths) returned by :func:`find_mirs_files`.
    mirs_dir:
        Directory containing MIRS files.
    snd_vars_to_keep:
        Variables to retain from SND datasets.
    img_vars_to_remove:
        Variables to drop from IMG datasets.

    Returns
    -------
    tuple[xr.Dataset, xr.Dataset]
        ``(ds_img, ds_snd)`` merged datasets ready for output.

    Raises
    ------
    ValueError
        If either file list is empty.
    """
    if not img_files:
        raise ValueError("No MIRS IMG files provided.")
    if not snd_files:
        raise ValueError("No MIRS SND files provided.")

    ds_img_list = [xr.open_dataset(os.path.join(mirs_dir, f)) for f in img_files]
    ds_img = xr.concat(ds_img_list, dim="Scanline").drop_vars(
        img_vars_to_remove, errors="ignore"
    )

    ds_snd_list = [xr.open_dataset(os.path.join(mirs_dir, f)) for f in snd_files]
    ds_snd = xr.concat(ds_snd_list, dim="Scanline")[snd_vars_to_keep]

    return ds_img, ds_snd