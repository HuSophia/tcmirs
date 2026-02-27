"""
ibtracs.py
----------
Functions for reading and filtering IBTrACS storm track data.
"""

from __future__ import annotations

import pandas as pd

from .config import IBTRACS_EXTRACT_VARS


def _lon_to_360(dlon: float) -> float:
    """Convert a longitude value from -180/180 to 0-360 degrees."""
    return (360 + (dlon % 360)) % 360


def get_storm_track(
    name: str,
    year: int,
    ibtracs_csv: str,
    filter_missing_wmo: bool = True,
    extra_vars: list[str] | None = None,
) -> pd.DataFrame:
    """
    Load IBTrACS CSV data and return track rows for a named storm in a given year.

    Parameters
    ----------
    name:
        Storm name in uppercase, e.g. ``"IDA"``.
    year:
        Four-digit calendar year of the storm, e.g. ``2021``.
    ibtracs_csv:
        Path to the IBTrACS ``*.list.v04r00.csv`` file.
    filter_missing_wmo:
        If ``True`` (default), rows with missing WMO wind or pressure are
        dropped. Set to ``False`` for years like 2021 where WMO fields may
        be blank in early data.
    extra_vars:
        Additional column names to include beyond the default set defined in
        :data:`config.IBTRACS_EXTRACT_VARS`.

    Returns
    -------
    pd.DataFrame
        Filtered track data with an extra ``LON_180`` column (original
        longitude) and ``LON`` converted to 0-360 degrees.
    """
    data = pd.read_csv(ibtracs_csv, low_memory=False)
    data = data.iloc[1:, :]  # drop units row

    year_start = pd.to_datetime(str(year))
    year_end = pd.to_datetime(str(year + 1))

    data = data[data["NAME"] == name]
    data["ISO_TIME"] = pd.to_datetime(data["ISO_TIME"])

    mask = (data["ISO_TIME"] >= year_start) & (data["ISO_TIME"] < year_end)
    data = data[mask]

    vars_to_extract = IBTRACS_EXTRACT_VARS.copy()
    if extra_vars:
        vars_to_extract += [v for v in extra_vars if v not in vars_to_extract]

    data = data[vars_to_extract]

    if filter_missing_wmo:
        data = data[data["WMO_WIND"] != " "]
        data = data[data["WMO_PRES"] != " "]

    data["LON_180"] = data["LON"]
    data["LON"] = data["LON"].astype(float).apply(_lon_to_360)

    return data