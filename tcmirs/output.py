"""
output.py
---------
Functions for assembling the final merged dataset and writing to netCDF.
"""

from __future__ import annotations

import xarray as xr


def build_output_dataset(
    ds_img: xr.Dataset,
    ds_snd: xr.Dataset,
    ds_ibt: xr.Dataset,
    storm_name: str,
    storm_year: int,
) -> xr.Dataset:
    """
    Merge MIRS IMG, MIRS SND, and IBTrACS datasets and attach global attributes.

    Parameters
    ----------
    ds_img:
        Filtered MIRS IMG dataset.
    ds_snd:
        Filtered MIRS SND dataset.
    ds_ibt:
        Full IBTrACS xarray Dataset (the ``.nc`` file, not the CSV).
    storm_name:
        Storm name in uppercase, e.g. ``"IDA"``.
    storm_year:
        Four-digit year of the storm.

    Returns
    -------
    xr.Dataset
        Merged dataset with TC metadata attributes attached.
    """
    storm_name_bytes = bytes(storm_name, "UTF-8")
    ds_storm = ds_ibt.where(ds_ibt.name == storm_name_bytes, drop=True)
    ds_storm = ds_storm.where(ds_storm.season == float(storm_year), drop=True)

    ds_merged = xr.merge([ds_img, ds_snd, ds_storm])

    ds_merged.attrs["TC_name"] = storm_name
    ds_merged.attrs["TC_time_start"] = bytes.decode(ds_storm["iso_time"][:, 0].item())
    ds_merged.attrs["TC_minimum_lat"] = round(float(ds_storm["lat"].min()), 2)
    ds_merged.attrs["TC_minimum_lon"] = round(float(ds_storm["lon"].min()), 2)
    ds_merged.attrs["TC_maximum_lat"] = round(float(ds_storm["lat"].max()), 2)
    ds_merged.attrs["TC_maximum_lon"] = round(float(ds_storm["lon"].max()), 2)

    return ds_merged


def write_output(ds: xr.Dataset, output_path: str) -> None:
    """
    Write a dataset to a netCDF file.

    Parameters
    ----------
    ds:
        Dataset to write.
    output_path:
        Full path for the output ``.nc`` file.
    """
    ds.to_netcdf(output_path)
    print(f"Output written to: {output_path}")