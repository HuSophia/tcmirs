"""
config.py
---------
Default variable lists and constants. Users can override these by passing
custom lists into the processing functions.
"""

#: Variables to retain from MIRS SND files
SND_VARS_TO_KEEP: list[str] = [
    "Player", "Plevel", "PTemp", "PVapor", "PClw", "PRain", "PGraupel"
]

#: Variables to drop from MIRS IMG files
IMG_VARS_TO_REMOVE: list[str] = [
    "Atm_type", "ChanSel", "SWP", "IWP", "Snow",
    "SWE", "SnowGS", "SIce", "SIce_MY", "SIce_FY", "SFR",
    "CldTop", "CldBase", "CldThick", "PrecipType", "RFlag", "SurfM",
    "WindSp", "WindDir", "WindU", "WindV", "Prob_SF", "quality_information",
]

#: IBTrACS columns extracted for storm track data
IBTRACS_EXTRACT_VARS: list[str] = [
    "NAME", "ISO_TIME", "WMO_WIND", "WMO_PRES", "LAT", "LON",
    "USA_R34_NE", "USA_R34_NW", "USA_R34_SE", "USA_R34_SW",
    "USA_R50_NE", "USA_R50_NW", "USA_R50_SE", "USA_R50_SW",
    "USA_R64_NE", "USA_R64_NW", "USA_R64_SE", "USA_R64_SW",
    "REUNION_R34_NE", "REUNION_R34_NW", "REUNION_R34_SE", "REUNION_R34_SW",
    "REUNION_R50_NE", "REUNION_R50_NW", "REUNION_R50_SE", "REUNION_R50_SW",
    "REUNION_R64_NE", "REUNION_R64_NW", "REUNION_R64_SE", "REUNION_R64_SW",
    "BOM_R34_NE", "BOM_R34_SE", "BOM_R34_NW", "BOM_R34_SW",
    "BOM_R50_NE", "BOM_R50_SE", "BOM_R50_NW", "BOM_R50_SW",
    "BOM_R64_NE", "BOM_R64_SE", "BOM_R64_NW", "BOM_R64_SW",
]

#: Hours either side of each track point to search for matching MIRS granules
TIME_WINDOW_HOURS: int = 12