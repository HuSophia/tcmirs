# AutoNetCDF

During my Research and Development internship at NOAA, I developed **AutoNetCDF**, a software tool that significantly improved the efficiency of information retrieval and data mining tasks for NOAA engineers and scientists. AutoNetCDF automates the process of creating a comprehensive NetCDF file by merging data from the International Best Track Archive for Climate Stewardship (IBTrACS) and NOAA MIRS satellite data. This tool generates a detailed dataset for the lifecycle of a specified hurricane, streamlining data preparation and allowing researchers to focus more on analysis and insights.

The primary functions of **AutoNetCDF** are to:
- Extract relevant hurricane data from IBTrACs based on storm name and year
- Identify and process corresponding NOAA MIRS satellite data that aligns with the storm's path
- Merge these datasets into a single comprehensive NetCDF file for further analysis and visualization

## Instructions
**1. Set Directory path**
- Update the 'dir_path' variable (line 48) with the correct path to your local directory containing MIRS data files
**2. Testing/Production**
- If you are testing or running a production version, adjust lines 71 and 72 accordingly:
  - **Testing**: Leave the lines as they are to process a limited number of points in the storm's lifecycle
  - **Production**: Comment out lines 71 and 72 to process the entire lifecycle of the storm

### Output 
The script generates a NetCDF file named according to the specified storm and year (e.g. 'IDA_2021_all_data.nc') with the combined IBTrACs and MIRS data. 

### Notes
- Make sure the MIRS data directory path is correctly specified to avoid **FileNotFound** error.
- The script processes IBTrACS data from 'ibtracs.ALL.list.v04r00.csv' and matches it with the NOAA MIRS data format.
- The satellite data is filtered to include only relevant portions that intersect with the hurricane's path.


