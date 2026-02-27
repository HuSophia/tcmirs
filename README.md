# tcmirs

Developed during an R&D internship at NOAA, **tcmirs** automates the creation of a comprehensive netCDF file by merging data from the [International Best Track Archive for Climate Stewardship (IBTrACS)](https://www.ncei.noaa.gov/products/international-best-track-archive) and NOAA MIRS satellite retrievals. Given a storm name and year, the package extracts the full hurricane lifecycle from IBTrACS, identifies MIRS satellite granules that intersect the storm's path, and merges them into a single analysis-ready netCDF file — allowing researchers to focus on analysis rather than data preparation.

## Installation

```bash
git clone https://github.com/your-username/tcmirs.git
cd tcmirs
pip install -e .
```

## Usage

**Command line**
```bash
# Full storm lifecycle
tcmirs --name IDA --year 2021 --mirs-dir /path/to/MIRS_DATA/

# Test on a subset of track points
tcmirs --name IDA --year 2021 --mirs-dir /path/to/MIRS_DATA/ --test-indices 42 43
```

**Python API**
```python
import xarray as xr
from tcmirs import get_storm_track, find_mirs_files, load_and_merge_mirs
from tcmirs import build_output_dataset, write_output

track = get_storm_track("IDA", 2021, "ibtracs.ALL.list.v04r00.csv", filter_missing_wmo=False)

img_files, snd_files = find_mirs_files(track, "/path/to/MIRS_DATA/", track_indices=[42, 43])

ds_img, ds_snd = load_and_merge_mirs(img_files, snd_files, "/path/to/MIRS_DATA/")

ds_ibt = xr.open_dataset("IBTrACS.ALL.v04r00.nc")
ds_out = build_output_dataset(ds_img, ds_snd, ds_ibt, "IDA", 2021)
write_output(ds_out, "IDA_2021_all_data.nc")
```

## Required data files

| File | Source |
|------|--------|
| `ibtracs.ALL.list.v04r00.csv` | [IBTrACS downloads](https://www.ncei.noaa.gov/data/international-best-track-archive-for-climate-stewardship-ibtracs/v04r00/access/csv/) |
| `IBTrACS.ALL.v04r00.nc` | [IBTrACS downloads](https://www.ncei.noaa.gov/data/international-best-track-archive-for-climate-stewardship-ibtracs/v04r00/access/netcdf/) |
| MIRS granules (`NPR-MIRS-IMG*`, `NPR-MIRS-SND*`) | NOAA MIRS |

## Package structure

```
tcmirs/
├── __init__.py    — public API
├── config.py      — variable lists and constants
├── ibtracs.py     — IBTrACS track loading and filtering
├── mirs.py        — MIRS granule discovery and loading
├── output.py      — dataset merging and netCDF writing
└── cli.py         — command-line entry point
```

## Notes
- MIRS granules are matched to each track point within a ±12 hour window
- For Atlantic storms, granules that wrap around the dateline are automatically excluded
- The `--test-indices` flag is recommended for verifying a new storm before processing its full lifecycle
- IBTrACS 2021 data has incomplete WMO wind/pressure fields; the `filter_missing_wmo` option handles this automatically when `year=2021`


