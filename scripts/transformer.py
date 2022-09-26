# Importing Dictionaries
import pandas as pd


# Reading all CSV files
crop_data = pd.read_csv('inputs/crop.csv')
spectral_data = pd.read_csv('inputs/spectral.csv')
soil_data = pd.read_csv('inputs/soil.csv')
weather_data = pd.read_csv('inputs/weather.csv')

# Number 1:

# Crop Data from 2021:
crop_data_2021 = crop_data[crop_data['year'] == 2021]

# Removing unneccary columns:

crop_data_2021_cleaned = crop_data_2021[['field_id', 'field_geometry', 'crop_type']]

# Saving CSV to outputs folder
crop_data_2021_cleaned.to_csv('outputs/crop_cleaned.csv')

# Number 2:

# Calculating NDVI:
spectral_data['NDVI'] = (spectral_data['nir'] - spectral_data['red'])/(spectral_data['nir'] + spectral_data['red'])

# Extract Year from Date
spectral_data['year'] = pd.DatetimeIndex(spectral_data['date']).year

# Grouping by column to generate pos value
spectral_data_pos = spectral_data.loc[spectral_data.groupby(['tile_id','year'])['NDVI'].idxmax()].reset_index(drop=True)

# Renaming columns / Cleaning up
spectral_data_pos_cleaned = spectral_data_pos.rename(columns={'date': 'pos_date', 'NDVI': 'pos'}) 
spectral_data_pos_cleaned = spectral_data_pos_cleaned[['tile_id', 'tile_geometry', 'pos', 'pos_date']]

# Saving CSV to outputs folder
spectral_data_pos_cleaned.to_csv('outputs/spectral_cleaned.csv')

# Number 3:

#Calculating Weighted Averaged
soil_data['HLW'] = (abs(soil_data['hzdept'] - soil_data['hzdepb']))/(soil_data['hzdepb'])
soil_data['WAC'] = soil_data['mukey'] * (soil_data['comppct']/100)

# Grouping by mukey and cokey

soil_data_grouped = soil_data.groupby(['mukey', 'cokey'], as_index=False).agg({'HLW': 'sum', 'mukey_geometry': 'first', 'om': 'first', 'cec': 'first', 'ph': 'first', 'comppct': 'first'})

# Renaming columns / Cleaning up
# I wasn't too sure what the ask for this specific question was as the output only required mukey, the geomery and the soil attributed after being asked to calculate weighted averages.
soil_data_cleaned = soil_data_grouped[['mukey', 'mukey_geometry', 'om', 'cec', 'ph']]
# Saving CSV to outputs folder
soil_data_cleaned.to_csv('outputs/soil_cleaned.csv')

# Number 4:
# Filtered for 2021
weather_data_2021 = weather_data[weather_data['year'] == 2021]
weather_data_2021['temp_mean'] = weather_data_2021['temp']
weather_data_2021['temp_min'] = weather_data_2021['temp']
weather_data_2021['temp_max'] = weather_data_2021['temp']
weather_data_grouped = weather_data_2021.groupby(['fips_code'], as_index=False).agg({'precip': 'sum', 'temp_min': 'min', 'temp_max': 'max', 'temp_mean': 'mean'})

# Saving CSV to outputs folder
weather_data_grouped.to_csv('outputs/weather_cleaned.csv')

