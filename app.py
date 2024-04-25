import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


crime_df = pd.read_csv('data.csv')


crime_df = pd.read_csv('data.csv')

st.title("Crime Data Dashboard")

st.subheader("Raw Data")
st.write(crime_df.head())





crimes = ['Rape', 'Kidnapping and Abduction', 'Dowry Deaths',
          'Assault on women with intent to outrage her modesty',
          'Insult to modesty of Women', 'Cruelty by Husband or his Relatives',
          'Importation of Girls']

north_india = ['Jammu & Kashmir', 'Punjab', 'Himachal Pradesh', 'Haryana', 'Uttarakhand', 'Uttar Pradesh', 'Chandigarh']
east_india = ['Bihar', 'Odisha', 'Jharkhand', 'West Bengal']
south_india = ['Andhra Pradesh', 'Karnataka', 'Kerala' ,'Tamil Nadu', 'Telangana']
west_india = ['Rajasthan' , 'Gujarat', 'Goa','Maharashtra','Goa']
central_india = ['Madhya Pradesh', 'Chhattisgarh']
north_east_india = ['Assam', 'Sikkim', 'Nagaland', 'Meghalaya', 'Manipur', 'Mizoram', 'Tripura', 'Arunachal Pradesh']
ut_india = ['A & N ISLANDS', 'Delhi', 'LAKSHADWEEP', 'PUDUCHERRY', 'A&N Islands', 'Daman & Diu', 'Delhi Ut', 'Lakshadweep',
       'Puducherry', 'D & N Haveli', 'DAMAN & DIU', 'D&N Haveli', 'A & N Islands']
def get_zonal_names(row):
    if row['STATE/UT'].title().strip() in north_india:
        val = 'North Zone'
    elif row['STATE/UT'].title().strip()  in south_india:
        val = 'South Zone'
    elif row['STATE/UT'].title().strip()  in east_india:
        val = 'East Zone'
    elif row['STATE/UT'].title().strip()  in west_india:
        val = 'West Zone'
    elif row['STATE/UT'].title().strip()  in central_india:
        val = 'Central Zone'
    elif row['STATE/UT'].title().strip()  in north_east_india:
        val = 'NE Zone'
    elif row['STATE/UT'].title().strip()  in ut_india:
        val = 'Union Terr'
    else:
        val = 'No Value'
    return val
crime_df['Zones'] = crime_df.apply(get_zonal_names, axis=1)
crime_df['Zones'].unique()

def plot_line_chart(df, x_col, y_col, hue_col, title, xlabel, ylabel):
    st.subheader(title)
    fig, ax = plt.subplots(figsize=(15, 8))
    sns.lineplot(x=x_col, y=y_col, hue=hue_col, data=df, palette='viridis', ci=None)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)
    plt.legend()
    st.pyplot(fig)

def plot_bar_chart(df, x_col, y_col, title, xlabel, ylabel):
    st.subheader(title)
    fig, ax = plt.subplots(figsize=(15, 8))
    sns.barplot(x=x_col, y=y_col, data=df, palette='muted', errwidth=0)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title, fontdict={'fontsize': 15})
    plt.xticks(rotation=45, ha='right')
    st.pyplot(fig)

def display_top_states(df, n=5):
    st.write(df.head(n))



rape_df = pd.DataFrame()
kidnap_df = pd.DataFrame()

if 'Zones' in crime_df.columns:
    rape_df = crime_df.groupby(by=['Year', 'STATE/UT', 'Zones'])['Rape'].sum().reset_index().sort_values(crimes[0], ascending=False)
    kidnap_df = crime_df.groupby(by=['Year', 'STATE/UT', 'Zones'])['Kidnapping and Abduction'].sum().reset_index().sort_values(crimes[1], ascending=False)
st.title("Rape Cases")
if not rape_df.empty:
    st.subheader("Rape Cases Over Time")
    fig, ax = plt.subplots(figsize=(10, 6))
    for zone in rape_df['Zones'].unique():
        zone_data = rape_df[rape_df['Zones'] == zone]
        sns.lineplot(x=zone_data['Year'], y=zone_data['Rape'], ci=None, label=zone, ax=ax)

    plt.xlabel('Years')
    plt.ylabel('# Rape Cases')
    plt.title('Rape Cases in Different Zones Over Time')
    plt.legend()
    st.pyplot(fig)

    st.subheader('Zone-Wise Rape Cases Registered ')
    fig, ax = plt.subplots(figsize=(15, 10))
    order = rape_df.groupby('Zones')['Rape'].sum().sort_values(ascending=False).index
    color_palette = 'viridis'
    sns.barplot(x='Zones', y='Rape', data=rape_df, order=order, errwidth=0, ax=ax, palette=color_palette)
    plt.xticks(rotation=45, ha='right')
    plt.ylabel('# Rape Cases')
    plt.title('Zone-Wise Rape Cases Registered', fontdict={'fontsize': 15})
    st.pyplot(fig)

    st.subheader('States with Rape Cases Registered')
    selected_zones = ['Central Zone', 'East Zone']
    rape_st_df = rape_df[rape_df['Zones'].isin(selected_zones)]
    rape_st_df = rape_st_df.groupby(by='STATE/UT')['Rape'].sum().reset_index().sort_values('Rape', ascending=False)
    color_palette = 'muted'
    fig, ax = plt.subplots(figsize=(15, 10))
    sns.barplot(x='STATE/UT', y='Rape', data=rape_st_df, errwidth=0, palette=color_palette)
    plt.xticks(rotation=45, ha='right')
    plt.ylabel('# Rape Cases')
    plt.title('States with Rape Cases Registered', fontdict={'fontsize': 15})
    st.pyplot(fig)
    

kidnap_df = crime_df.groupby(by=['Year', 'STATE/UT', 'Zones'])['Kidnapping and Abduction'].sum().reset_index().sort_values(crimes[1], ascending=False)

st.title("Kidnapping and Abduction Cases")

st.subheader("Kidnapping and Abduction Cases Over Time")
fig, axes = plt.subplots(figsize=(20, 15), nrows=len(kidnap_df['Zones'].unique()), ncols=1)

for count, zone in enumerate(kidnap_df['Zones'].unique()):
    ax = axes[count]
    zone_data = kidnap_df[kidnap_df['Zones'] == zone]
    sns.lineplot(x=zone_data['Year'], y=zone_data['Kidnapping and Abduction'], ci=None, ax=ax)
    ax.set_xlabel('Years')
    ax.set_ylabel('# Cases')
    ax.set_title(zone)

plt.subplots_adjust(hspace=0.9)

st.pyplot(fig)

st.subheader('Zone-Wise Kidnapping/Abduction Cases Registered ')
fig, ax = plt.subplots(figsize=(15, 10))
order = kidnap_df.groupby('Zones')['Kidnapping and Abduction'].sum().sort_values(ascending=False).index
color_palette = 'muted'
sns.barplot(x='Zones', y='Kidnapping and Abduction', data=kidnap_df, order=order, errwidth=0, ax=ax, palette=color_palette)
ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha='right')
ax.set_ylabel('# Kidnapping/Abduction Cases')
ax.set_title('Zone-Wise Kidnapping/Abduction Cases Registered', fontdict={'fontsize': 15})


st.pyplot(fig)


st.subheader('States with Kidnapping and Abduction Cases Registered ')
selected_zones_kidnap = ['East Zone', 'West Zone']
kidnap_st_df = kidnap_df[kidnap_df['Zones'].isin(selected_zones_kidnap)]
kidnap_st_df = kidnap_st_df.groupby(by='STATE/UT')['Kidnapping and Abduction'].sum().reset_index().sort_values('Kidnapping and Abduction', ascending=False)
color_palette_kidnap = 'pastel'
fig, ax = plt.subplots(figsize=(15, 10))
sns.barplot(x='STATE/UT', y='Kidnapping and Abduction', data=kidnap_st_df, errwidth=0, palette=color_palette_kidnap)
ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha='right')
ax.set_ylabel('# Kidnapping and Abduction Cases')
ax.set_title('States with Kidnapping and Abduction Cases Registered', fontdict={'fontsize': 15})

st.pyplot(fig)




dowry_df = crime_df.groupby(by=['Year', 'STATE/UT', 'Zones'])['Dowry Deaths'].sum().reset_index().sort_values('Dowry Deaths', ascending=False)


st.title("Dowry Deaths Cases ")

st.subheader("Dowry Deaths Cases Over Time")
fig, axes = plt.subplots(figsize=(20, 15), nrows=len(dowry_df['Zones'].unique()), ncols=1)

for count, zone in enumerate(dowry_df['Zones'].unique()):
    ax = axes[count]
    zone_data = dowry_df[dowry_df['Zones'] == zone]
    sns.lineplot(x=zone_data['Year'], y=zone_data['Dowry Deaths'], ci=None, ax=ax)
    ax.set_xlabel('Years')
    ax.set_ylabel('# Cases')
    ax.set_title(zone)


plt.subplots_adjust(hspace=0.9)


st.pyplot(fig)


st.subheader('Zone-Wise Dowry Deaths Cases Registered')
fig, ax = plt.subplots(figsize=(15, 10))
order = dowry_df.groupby('Zones')['Dowry Deaths'].sum().sort_values(ascending=False).index
color_palette = 'pastel'
sns.barplot(x='Zones', y='Dowry Deaths', data=dowry_df, order=order, errwidth=0, ax=ax, palette=color_palette)
ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha='right')
ax.set_ylabel('# Dowry Deaths Cases')
ax.set_title('Zone-Wise Dowry Deaths Cases Registered', fontdict={'fontsize': 15})


st.pyplot(fig)


st.subheader('States with Dowry Deaths Cases Registered ')
selected_zones_dowry = ['East Zone', 'Central Zone']
dowry_st_df = dowry_df[dowry_df['Zones'].isin(selected_zones_dowry)]
dowry_st_df = dowry_st_df.groupby(by='STATE/UT')['Dowry Deaths'].sum().reset_index().sort_values('Dowry Deaths', ascending=False)
color_palette_dowry = 'pastel'
fig, ax = plt.subplots(figsize=(15, 10))
sns.barplot(x='STATE/UT', y='Dowry Deaths', data=dowry_st_df, errwidth=0, palette=color_palette_dowry)
ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha='right')
ax.set_ylabel('# Dowry Deaths Cases')
ax.set_title('States with Dowry Deaths Cases Registered', fontdict={'fontsize': 15})


st.pyplot(fig)


assault_df = crime_df.groupby(by=['Year', 'STATE/UT', 'Zones'])['Assault on women with intent to outrage her modesty'].sum().reset_index().sort_values('Assault on women with intent to outrage her modesty', ascending=False)


st.title("Assault Cases")

st.subheader('States with Dowry Deaths Cases Registered ')
selected_zones_dowry = ['East Zone', 'Central Zone']
dowry_st_df = dowry_df[dowry_df['Zones'].isin(selected_zones_dowry)]
dowry_st_df = dowry_st_df.groupby(by='STATE/UT')['Dowry Deaths'].sum().reset_index().sort_values('Dowry Deaths', ascending=False)
color_palette_dowry = 'pastel'
fig, ax = plt.subplots(figsize=(15, 10))
sns.barplot(x='STATE/UT', y='Dowry Deaths', data=dowry_st_df, errwidth=0, palette=color_palette_dowry)
ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha='right')
ax.set_ylabel('# Dowry Deaths Cases')
ax.set_title('States with Dowry Deaths Cases Registered', fontdict={'fontsize': 15})

st.pyplot(fig)


st.subheader('Zone-Wise Assault on Women Cases Registered ')
fig, ax = plt.subplots(figsize=(15, 10))
color_palette_assault = 'viridis'
sns.lineplot(x='Year', y='Assault on women with intent to outrage her modesty', hue='Zones',
             data=assault_df, palette=color_palette_assault)
ax.set_ylabel('# Assault Cases')
ax.set_title('Zone-Wise Assault on Women Cases Registered', fontdict={'fontsize': 15})

st.pyplot(fig)

st.subheader('States with Assault on Women Cases Registered ')
selected_zones_assault = ['Central Zone', 'South Zone']
assault_st_df = assault_df[assault_df['Zones'].isin(selected_zones_assault)]
assault_st_df = assault_st_df.groupby(by='STATE/UT')['Assault on women with intent to outrage her modesty'].sum().reset_index().sort_values('Assault on women with intent to outrage her modesty', ascending=False)
color_palette_assault = 'Set2'
fig, ax = plt.subplots(figsize=(15, 10))
sns.barplot(x='STATE/UT', y='Assault on women with intent to outrage her modesty', data=assault_st_df, errwidth=0, palette=color_palette_assault)
ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha='right')
ax.set_ylabel('# Assault on Women Cases')
ax.set_title('States with Assault on Women Cases Registered', fontdict={'fontsize': 15})

st.pyplot(fig)


insult_df = crime_df.groupby(by=['Year', 'STATE/UT', 'Zones'])['Insult to modesty of Women'].sum().reset_index().sort_values('Insult to modesty of Women', ascending=False)

st.title("Insult to Modesty Cases ")

st.subheader('Zone-Wise Insult to modesty of Women Cases Registered ')
fig, ax = plt.subplots(figsize=(15, 10))
color_palette_insult = 'pastel'
sns.lineplot(x='Year', y='Insult to modesty of Women', hue='Zones', data=insult_df, palette=color_palette_insult)
ax.set_xticks(insult_df['Year'].unique())
ax.set_ylabel('# Insult to modesty of Women Cases')
ax.set_title('Zone-Wise Insult to modesty of Women Cases Registered', fontdict={'fontsize': 15})
ax.legend(title='Zones')

st.pyplot(fig)

st.subheader('States with Insult to modesty of Women Cases Registered ')
selected_zone_insult = 'South Zone'
insult_st_df = insult_df[insult_df['Zones'] == selected_zone_insult]
insult_st_df = insult_st_df.groupby(by='STATE/UT')['Insult to modesty of Women'].sum().reset_index().sort_values('Insult to modesty of Women', ascending=False)
color_palette_insult = 'Set3'
fig, ax = plt.subplots(figsize=(15, 10))
sns.barplot(x='STATE/UT', y='Insult to modesty of Women', data=insult_st_df, errwidth=0, palette=color_palette_insult)
ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha='right')
ax.set_ylabel('# Insult to modesty of Women Cases')
ax.set_title('States with Insult to modesty of Women Cases Registered', fontdict={'fontsize': 15})

st.pyplot(fig)


cruel_df = crime_df.groupby(by=['Year', 'STATE/UT', 'Zones'])['Cruelty by Husband or his Relatives'].sum().reset_index().sort_values('Cruelty by Husband or his Relatives', ascending=False)

st.title("Cruelty by Husband or his Relatives Cases")

st.subheader('Zone-Wise Cruelty by Husband or his Relatives Cases Registered ')
fig, ax = plt.subplots(figsize=(15, 10))
color_palette_cruel = 'Set2'
sns.lineplot(x='Year', y='Cruelty by Husband or his Relatives', hue='Zones', data=cruel_df, palette=color_palette_cruel)
ax.set_xticks(cruel_df['Year'].unique())
ax.set_ylabel('# Cruelty by Husband or his Relatives Cases')
ax.set_title('Zone-Wise Cruelty by Husband or his Relatives Cases Registered', fontdict={'fontsize': 15})
ax.legend(title='Zones')

st.pyplot(fig)

st.subheader('States with Cruelty by Husband or his Relatives Cases Registered ')
selected_zones_cruel = ['West Zone', 'South Zone']
cruel_st_df = cruel_df[cruel_df['Zones'].isin(selected_zones_cruel)]
cruel_st_df = cruel_st_df.groupby(by='STATE/UT')['Cruelty by Husband or his Relatives'].sum().reset_index().sort_values('Cruelty by Husband or his Relatives', ascending=False)
color_palette_cruel = 'viridis'
fig, ax = plt.subplots(figsize=(15, 10))
sns.barplot(x='STATE/UT', y='Cruelty by Husband or his Relatives', data=cruel_st_df, errwidth=0, palette=color_palette_cruel)
ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha='right')
ax.set_ylabel('# Cruelty by Husband or his Relatives Cases')
ax.set_title('States with Cruelty by Husband or his Relatives Cases Registered', fontdict={'fontsize': 15})

st.pyplot(fig)



import_df = crime_df.groupby(by=['Year', 'STATE/UT', 'Zones'])['Importation of Girls'].sum().reset_index().sort_values('Importation of Girls', ascending=False)

st.title("Importation of Girls Cases ")

st.subheader('Zone-Wise Importation of Girls Cases Registered ')
fig, ax = plt.subplots(figsize=(15, 10))
color_palette_import = 'viridis'
for zone in import_df['Zones'].unique():
    zone_data = import_df[import_df['Zones'] == zone]
    sns.lineplot(x=zone_data['Year'], y=zone_data['Importation of Girls'], ci=None, label=zone)

ax.set_xlabel('Years')
ax.set_ylabel('# Cases')
ax.set_title('Zone-Wise Importation of Girls Cases Registered', fontdict={'fontsize': 15})
ax.legend(title='Zones')

st.pyplot(fig)

st.subheader('States with Importation of Girls Cases Registered ')
selected_zone_import = 'East Zone'
import_st_df = import_df[import_df['Zones'] == selected_zone_import]
import_st_df = import_st_df.groupby(by='STATE/UT')['Importation of Girls'].sum().reset_index().sort_values('Importation of Girls', ascending=False)
color_palette_import = 'Blues'
fig, ax = plt.subplots(figsize=(15, 10))
sns.barplot(x='STATE/UT', y='Importation of Girls', data=import_st_df, errwidth=0, palette=color_palette_import)
ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha='right')
ax.set_ylabel('# Importation of Girls Cases')
ax.set_title('States with Importation of Girls Cases Registered', fontdict={'fontsize': 15})

st.pyplot(fig)



