#!/usr/bin/env python
# coding: utf-8

# # WeatherPy
# ----
# 
# ### Analysis
# * As expected, the weather becomes significantly warmer as one approaches the equator (0 Deg. Latitude). More interestingly, however, is the fact that the southern hemisphere tends to be warmer this time of year than the northern hemisphere. This may be due to the tilt of the earth.
# * There is no strong relationship between latitude and cloudiness. However, it is interesting to see that a strong band of cities sits at 0, 80, and 100% cloudiness.
# * There is no strong relationship between latitude and wind speed. However, in northern hemispheres there is a flurry of cities with over 20 mph of wind.
# 
# ---
# 

# In[1]:


# Dependencies and Setup
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import requests
import time
from pprint import pprint
# Import API key
from config import api_key

# Incorporated citipy to determine city based on latitude and longitude
from citipy import citipy

# Output File (CSV)
random_weather_data_file = "./Resources/weather_random_cities.csv"
weatherapi_data_file = "./Resources/API_random_cities.csv"

# Range of latitudes and longitudes
lat_range = (-90, 90)
lng_range = (-180, 180)
print(lng_range)
print(lat_range)


# ## Generate Cities List

# In[2]:


# List for holding lat_lngs and cities
lat_lngs = []
cities = []

# Create a set of random lat and lng combinations
lats = np.random.uniform(low=-90.000, high=90.000, size=1500)
lngs = np.random.uniform(low=-180.000, high=180.000, size=1500)
lat_lngs = zip(lats, lngs)

# Identify nearest city for each lat, lng combination
for lat_lng in lat_lngs:
    city = citipy.nearest_city(lat_lng[0], lat_lng[1]).city_name
    
    # If the city is unique, then add it to a our cities list
    if city not in cities:
        cities.append(city)

# Print the city count to confirm sufficient count
print(len(cities))


# ### Perform API Calls
# * Perform a weather check on each city using a series of successive API calls.
# * Include a print log of each city as it'sbeing processed (with the city number and city name).

# In[3]:


URLs = []
City = []
Cloudiness = []
Country = []
Date = []
Humidity = []
Lat = []
Lng = []
Max_Temp = []
Wind_Speed = []
WPy = {}
url = "http://api.openweathermap.org/data/2.5/weather?"
units = "imperial"


# In[4]:


for city in cities:
    query_url = f'{url}&APPID={api_key}&q={city}&units={units}'
    URLs.append(query_url)
    print(query_url)
    weather_response = requests.get(query_url)
    weather_json = weather_response.json()
    try:
        city = weather_json["name"]
        City.append(city)
        max_temp = weather_json["main"]["temp_max"]
        Max_Temp.append(max_temp)
        country = weather_json["sys"]["country"]
        Country.append(country)
        date = weather_json["dt"]
        Date.append(date)
        humidity = weather_json["main"]["humidity"]
        Humidity.append(humidity)
        lat = weather_json["coord"]["lat"]
        Lat.append(lat)
        lng = weather_json["coord"]["lon"]
        Lng.append(lng)
        cloudiness = weather_json["clouds"]["all"]
        Cloudiness.append(cloudiness)
        wind_speed = weather_json["wind"]["speed"]
        Wind_Speed.append(wind_speed)
    except KeyError:
        print(f"{city} doesn't exist in the list.")  


# ### Convert Raw Data to DataFrame
# * Export the city data into a .csv.
# * Display the DataFrame

# In[6]:


WPy = {"City": City , "Cloudiness": Cloudiness, "Country": Country , "Date": Date , "Humidity": Humidity,       "Lat": Lat, "Lng": Lng, "Max Temp": Max_Temp, "Wind Speed": Wind_Speed}
weather_df = pd.DataFrame(WPy)
weather_df.head()


# In[7]:


weather_df.to_csv(random_weather_data_file, index=False)


# In[8]:


weatherapi_dict = {"Weather API URL": URLs}
weatherapi_df = pd.DataFrame(weatherapi_dict)
weatherapi_df.to_csv(weatherapi_data_file, index=False)
weatherapi_df.head()


# ### Plotting the Data
# * Use proper labeling of the plots using plot titles (including date of analysis) and axes labels.
# * Save the plotted figures as .pngs.

# #### Latitude vs. Temperature Plot

# In[13]:


plt.scatter(x=Lat, y=Max_Temp,marker="o", c = "blue",edgecolor="black")
plt.title(f"City Latitude vs Max Temperature Plot (01/05/17)")
plt.xlabel("Latitude")
plt.ylabel(f"Max Temperature(F)")
plt.savefig('LatvsMaxTemp.png')
plt.grid()


# #### Latitude vs. Humidity Plot

# In[14]:


plt.scatter(x=Lat, y=Humidity,marker="o", c = "blue",edgecolor="black")
plt.title(f"City Latitude vs Humidity Plot (01/05/17)")
plt.xlabel("Latitude")
plt.ylabel(f'Humidity(%)')
plt.savefig('LatvsHumidity.png')
plt.grid()


# #### Latitude vs. Cloudiness Plot

# In[15]:


plt.scatter(x=Lat, y=Cloudiness,marker="o", c = "blue",edgecolor="black")
plt.title(f"City Latitude vs Cloudiness Plot (01/05/17)")
plt.xlabel("Latitude")
plt.ylabel(f'Cloudiness(%)')
plt.savefig('LatvsCloudiness.png')
plt.grid()


# #### Latitude vs. Wind Speed Plot

# In[16]:


plt.scatter(x=Lat, y=Wind_Speed,marker="o", c = "blue",edgecolor="black")
plt.title(f"City Latitude vs Wind Speed Plot (01/05/17)")
plt.xlabel("Latitude")
plt.ylabel(f'Wind Speed(mph)')
plt.savefig('LatvsWindSpeed.png')
plt.grid()


# In[ ]:




