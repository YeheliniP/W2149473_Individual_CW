import pandas as pd
import numpy as np
# Loading the dataset 
asap = pd.read_csv('asap-hotspots-monthly.csv')
print(asap.head())
# EDA
print(asap.shape)
print(asap.info())
print(asap.describe(include="all"))
print(asap.head())
#count of missing values 
print(asap.isnull())
print(asap.isnull().sum()) #count of missing values 
asap['date'] = pd.to_datetime(asap['date']) #converting the date column to datetime format
asap_cleaned = asap.dropna(subset=['ISO3']) #removing the rows with null values
print(asap_cleaned.isnull().sum())
asap_cleaned.to_csv('asap-cleaned.csv', index=False)


