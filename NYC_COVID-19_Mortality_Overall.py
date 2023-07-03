# COVID-19 Overall Mortality Rates in New York City
# Author: Emily Colby
# Date: May-24-2023
# Description: This script calculates and analyzes overall COVID-19 mortality rates in New York City (NYC) by borough and citywide; data is retrieved from:
# 1. The NYC Department of Health and Mental Hygiene coronavirus-data GitHub repository
# 2. The NYC Department of City Planning 2020 census data

import pandas as pd
import matplotlib as plt
import numpy as np

deaths_by_day = pd.read_csv(
    "/Users/emily/code/NYC_COVID_project/deaths-by-day.csv"
)  # NYC mortality data
nyc_census = pd.read_csv(
    "/Users/emily/code/NYC_COVID_project/nyc_decennialcensusdata_2010_2020_change-core-geographies.csv"
)  # NYC census data

# Clean/wrangle nyc mortality data (lines 20-42)
# Remove irrelevant columns from mortality dataframe
deaths_by_day = deaths_by_day.loc[:, ~deaths_by_day.columns.str.endswith("7DAY_AVG")]
deaths_by_day.drop("INCOMPLETE", axis=1, inplace=True)

# Create an array called "total_deaths" that takes the deaths_by_day dataframe and sums total deaths in each column (i.e., total deaths per borough)
total_deaths = deaths_by_day.iloc[:, 1:].sum()

# Create a new dataframe from "total_deaths" that consists of rows with total deaths for each borough
total_deaths_df = pd.DataFrame(
    total_deaths,
    index=[
        "MN_DEATH_COUNT",
        "BX_DEATH_COUNT",
        "BK_DEATH_COUNT",
        "QN_DEATH_COUNT",
        "SI_DEATH_COUNT",
    ],
)

total_deaths_df = total_deaths_df.rename(columns={0: "Death count"})

# Sum deaths in all borourghs and store this value in a variable called, "CITYWIDE_DEATH_COUNT" (we will need to use this variable later when we combine mortality and census data)
CITYWIDE_DEATH_COUNT = total_deaths_df.sum()

# Clean/wrangle nyc census data (lines 45-68)
# Rename census dataframe columns to something more descriptive and remove irrelevant columns
nyc_census = nyc_census.rename(
    columns={"Unnamed: 2": "Borough", "2020 Data": "2020 Total Population"}
)
nyc_census = nyc_census.drop(columns=["Unnamed: 1", "Geography"])
columns_to_keep = ["Borough", "2020 Total Population"]
nyc_census = nyc_census[columns_to_keep]

# We just need the total population for each borough; thus, we can reduce the census dataframe by several rows:
# Removing row index [0:4] as it contains column sub-titles and that we do not need & citywide total population, which we'll calculate later on our own
# Removing row index [9:] as it contains population data for geographic units more granular than borough (e.g., community districts), rendering this data unnecessary for the analysis
rows_to_drop = nyc_census.index[0:4].append(nyc_census.index[9:])
nyc_census = nyc_census.drop(rows_to_drop, axis=0)

# We also need to ensure population numbers are classed as integers
nyc_census["2020 Total Population"] = nyc_census["2020 Total Population"].str.replace(
    ",", ""
)
nyc_census["2020 Total Population"] = nyc_census["2020 Total Population"].astype(int)

# Create a total NYC population variable and create a new row in our census dataframe to place this value
total_NYC_pop = nyc_census["2020 Total Population"].sum()
new_pop_row = {"Borough": "Citywide", "2020 Total Population": total_NYC_pop}
nyc_census = nyc_census.append(new_pop_row, ignore_index=True)

# Combine mortality and census data into a single dataframe (lines xx-xx)
# Make a copy of nyc_census dataframe and store death counts from our total_deaths_df in a variable called "column_to_insert"; as the variable name suggests, we'll insert it into the death_census_data_combined dataframe
death_census_data_combined = nyc_census.copy()
column_to_insert = total_deaths_df["Death count"]  # .astype(np.float64)
insert_position = 1

# Reset the index of column_to_insert (this is done because there is a mismatched number of rows b/t the mortality and census dataframes)
column_to_insert = column_to_insert.reset_index(drop=True)


death_census_data_combined.insert(
    insert_position, "COVID-19 Death Count", column_to_insert
)
sum_deaths = column_to_insert.sum()

# Update the value of the sixth row in the "COVID Death Count" column
death_census_data_combined.at[5, "COVID-19 Death Count"] = sum_deaths

# Add a column to the "death_census_data_combined" dataframe that calculates the mortality rate in each borough and citywide
death_census_data_combined["Mortality Rate (per 1,000 population)"] = (
    death_census_data_combined["COVID-19 Death Count"]
    / death_census_data_combined["2020 Total Population"]
    * 1000
)
print(death_census_data_combined)
