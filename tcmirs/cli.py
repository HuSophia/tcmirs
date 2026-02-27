"""
cli.py
------
Command-line entry point. Reproduces the behaviour of the original script
and serves as an example of how to use the package programmatically.

Usage
-----
    python -m hurricane_mirs.cli --name IDA --year 2021

Or after ``pip install -e .``:
    hurricane-mirs --name IDA --year 2021
"""

from __future__ import annotations

import argparse
import xarray as xr

from .ibtracs import get_storm_track
from .mirs import find_mirs_files, load_and_merge_mirs
from .output import build_output_dataset, write_output


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Build a netCDF file from IBTrACS + MIRS data for a named TC."
    )
    parser.add_argument("--name", required=True, help="Storm name (uppercase), e.g. IDA")
    parser.add_argument("--year", required=True, type=int, help="Storm year, e.g. 2021")
    parser.add_argument(
        "--mirs-dir",
        default="/Users/sophiahu/Documents/MIRS_DATA/",
        help="Directory containing MIRS .nc files",
    )
    parser.add_argument(
        "--ibt-nc",
        default="IBTrACS.ALL.v04r00.nc",
        help="Path to IBTrACS .nc file",
    )
    parser.add_argument(
        "--ibt-csv",
        default="ibtracs.ALL.list.v04r00.csv",
        help="Path to IBTrACS CSV file",
    )
    parser.add_argument(
        "--output",
        default=None,
        help="Output filename (default: <NAME>_<YEAR>_all_data.nc)",
    )
    parser.add_argument(
        "--test-indices",
        nargs="+",
        type=int,
        default=None,
        metavar="IDX",
        help="Only process these track row indices (e.g. --test-indices 42 43)",
    )
    parser.add_argument(
        "--filter-missing-wmo",
        action=argparse.BooleanOptionalAction,
        default=True,
        help="Drop rows with missing WMO wind/pressure (disable for 2021)",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    storm_name = args.name.upper()
    output_file = args.output or f"{storm_name}_{args.year}_all_data.nc"

    # 2021 IBTrACS data has blank WMO fields; skip that filter
    filter_wmo = args.filter_missing_wmo and args.year != 2021

    print(f"Loading IBTrACS track for {storm_name} ({args.year})...")
    track = get_storm_track(
        name=storm_name,
        year=args.year,
        ibtracs_csv=args.ibt_csv,
        filter_missing_wmo=filter_wmo,
    )
    print(f"  {len(track)} track points loaded.")

    print("Finding matching MIRS granules...")
    img_files, snd_files = find_mirs_files(
        track=track,
        mirs_dir=args.mirs_dir,
        track_indices=args.test_indices,
    )
    print(f"  IMG files: {len(img_files)}  SND files: {len(snd_files)}")

    print("Loading and merging MIRS data...")
    ds_img, ds_snd = load_and_merge_mirs(img_files, snd_files, args.mirs_dir)

    print("Building output dataset...")
    ds_ibt = xr.open_dataset(args.ibt_nc)
    ds_out = build_output_dataset(ds_img, ds_snd, ds_ibt, storm_name, args.year)

    write_output(ds_out, output_file)


if __name__ == "__main__":
    main()