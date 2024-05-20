import requests
import json
import streamlit as st
import pandas as pd

# Getting astronaut data
astronaut_url = "http://api.open-notify.org/astros.json"
astro_response = requests.get(url=astronaut_url)
astro_json = astro_response.text
astro_data = json.loads(astro_json)
count = astro_data['number']
names = [name['name'] for name in astro_data['people']]

# Getting ISS location data
location_url = "http://api.open-notify.org/iss-now.json"
location_response = requests.get(url=location_url)
location_json = location_response.text
location_data = json.loads(location_json)

# Transformations for use in map
location_dataframe = pd.DataFrame(location_data)
location_dataframe = location_dataframe.drop(columns=['message'])
transposed_dataframe = location_dataframe.T
transposed_dataframe = transposed_dataframe.drop(transposed_dataframe.index[0])
transposed_dataframe['latitude'] = transposed_dataframe['latitude'].astype(float)
transposed_dataframe['longitude'] = transposed_dataframe['longitude'].astype(float)

# Streamlit app
st.title('International Space Station: Live')
st.subheader('Current Location')
st.map(transposed_dataframe, zoom=2, size=20, color='#0044ff')
st.caption('Current Coordinates')
st.caption(f"Latitude: {transposed_dataframe['latitude'][0]}")
st.caption(f"Longitude: {transposed_dataframe['longitude'][0]}")
st.subheader('People in Space')
st.write(f'Number of people in space right now: {count}')
st.write('People in space:')
st.markdown("- " + "\n- ".join(names))
st.markdown('Note: The number of people in space changes frequently due to crew rotations and visiting spacecraft.')