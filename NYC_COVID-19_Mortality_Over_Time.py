# COVID-19 Overall Mortality Rates in New York City
# Author: Emily Colby
# Date: May-24-2023
# Description: This script calculates and analyzes COVID-19 mortality rates in New York City (NYC) by borough and citywide; it also aims to describe the variations in mortality rate by borough through data visualization; data is retrieved from:
# 1. The NYC Department of Health and Mental Hygiene coronavirus-data GitHub repository
# 2. The NYC Department of City Planning 2020 census data

exec(open("NYC_COVID-19_Mortality_Overall.py").read())

import pandas as pd
import matplotlib as plt
import matplotlib.pyplot as plt
import numpy as np

# View Mortality Rates for each borough and citywide in a dataframe
print(death_census_data_combined)
