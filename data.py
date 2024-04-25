import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load data
crime_df = pd.read_csv('data.csv')

# Data preprocessing functions
def get_case_consistency(row):
    row = row.strip()
    row = row.upper()
    row = row.title()
    return row

def get_zonal_names(row):
    if row.title().strip() in north_india:
        val = 'North Zone'
    elif row.title().strip() in south_india:
        val = 'South Zone'
    elif row.title().strip() in east_india:
        val = 'East Zone'
    elif row.title().strip() in west_india:
        val = 'West Zone'
    elif row.title().strip() in central_india:
        val = 'Central Zone'
    elif row.title().strip() in north_east_india:
        val = 'NE Zone'
    elif row.title().strip() in ut_india:
        val = 'Union Terr'
    else:
        val = 'No Value'
    return val

# Apply preprocessing to the dataframe
crime_df['STATE/UT'] = crime_df['STATE/UT'].apply(get_case_consistency)
crime_df['Zones'] = crime_df['STATE/UT'].apply(get_zonal_names)

# Group data for Rape cases
rape_df = crime_df.groupby(by=['Year', 'STATE/UT', 'Zones'])['Rape'].sum().reset_index().sort_values('Rape', ascending=False)

# Streamlit App
st.title("Crime Data Dashboard")

# Display the raw data
st.subheader("Raw Data")
st.write(crime_df.head())

# Display line chart for Rape cases
st.subheader("Rape Cases Over Time")
plt.figure(figsize=(10, 6))
for zone in rape_df['Zones'].unique():
    zone_data = rape_df[rape_df['Zones'] == zone]
    sns.lineplot(x=zone_data['Year'], y=zone_data['Rape'], ci=None, label=zone)

plt.xlabel('Years')
plt.ylabel('# Rape Cases')
plt.title('Rape Cases in Different Zones Over Time')
plt.legend()
st.pyplot()

# You can add more visualizations for other crimes in a similar manner

# Show the app
st.show()
