# AutoNetCDF

During my Research and Development internship at NOAA, I developed **AutoNetCDF**, a software tool that significantly improved the efficiency of information retrieval and data mining tasks for NOAA engineers and scientists. AutoNetCDF automates the process of creating a comprehensive NetCDF file by merging data from the International Best Track Archive for Climate Stewardship (IBTrACS) and NOAA MIRS satellite data. This tool generates a detailed dataset for the lifecycle of a specified hurricane, streamlining data preparation and allowing researchers to focus more on analysis and insights.

The primary functions of **AutoNetCDF** are to:
- Extract relevant hurricane data from IBTrACs based on storm name and year
- Identify and process corresponding NOAA MIRS satellite data that aligns with the storm's path
- Merge these datasets into a single comprehensive NetCDF file for further analysis and visualization

## Instructions
**1. Set Directory path**
- Update the `'dir_path'` variable (line 48) with the correct path to your local directory containing MIRS data files.
  
**2.Specify User Input** 
- **Storm Name**: Set the `'storm_name'` variable to the name of the hurricane you want to analyze (e.g., `'IDA'`).
- **Year**: Set the `'storm_year'` variable to the year in which the storm occurred (e.g. `'2021'`).
  
**3. Testing/Production Configuration**
- If you are testing or running a production version, adjust lines 71 and 72 accordingly:
  - **Testing**: Leave the lines as they are to process a limited number of data points in the storm's lifecycle (e.g., points 42 and 43 for `'IDA'`). This speeds up execution and allows you to quickly debug and verify the functionality with a smaller dataset. 
  - **Production**: Comment out lines 71 and 72 to process the entire lifecycle of the storm. This ensures all relevant data points are included in the final output, providing a comprehensive dataset for analysis.

**4. Run the Script**
- Execute the script to generate a NetCDF file with the combined IBTrACs and MIRS data. The output file will be named according to the specified storm and year (e.g. `'IDA_2021_all_data.nc'`) 

### Notes
- Make sure the MIRS data directory path is correctly specified to avoid **FileNotFound** error.
- The script processes IBTrACS data from `'ibtracs.ALL.list.v04r00.csv'` and matches it with the NOAA MIRS data format.
- The satellite data is filtered to include only relevant portions that intersect with the hurricane's path.


