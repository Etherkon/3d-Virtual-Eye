# For getting weather information from Google

import pywapi
import cigi_support_methods as support

# Conversion rate
mph2ms_rate = 0.44704

# Gets current conditions
conditions = pywapi.get_weather_from_google( "weather=tampere,finland" )
wind_directions = {
        "N" : 360,
        "NE": 45,
        "E" : 90,
        "SE": 135,
        "S" : 180,
        "SW": 225,
        "W" : 270,
        "NW": 315
    }

#print conditions

#Test printing
print conditions['current_conditions']['condition']
#set_weather(...)
print conditions['current_conditions']['wind_condition']

# Method to get latest weather forecasts
def set_to_current_conditions():
    print "Setting current weather conditions"
    conditions = pywapi.get_weather_from_google( "weather=tampere,finland" )
    wind = conditions['current_conditions']['wind_condition'].split()
    # Wind: X at x mph
    support.set_wind( float(wind[3]) * mph2ms_rate, wind_directions.get((wind[1])))
    # Humidity: X%
    support.set_humidity( float( conditions['current_conditions']['humidity'].split()[1][:-1]))
    support.set_temperature( float( conditions['current_conditions']['temp_c']) )
    # Set weather based on current condition
    setweather( conditions['current_conditions']['condition'] )

def set_to_tomorrow_forecast():
    pass

# Sets weather to given condition
def setweather( condition ):
    if condition == "now":
        set_to_current_conditions()
    # Implemented weather conditions
    elif condition.lower() == "sunny" or condition.lower() == "clear":
        support.set_weather("clear")
    # Translate to something common
    elif condition.lower() == "partly sunny" or condition.lower() == "mostly sunny" or condition.lower() == "partly cloudy" or condition.lower() == "mostly cloudy":
        support.set_weather("cloudy")
    else:
        support.set_weather("overcast")


# All the conditions given by Google
#Summer:
#weather.coverage = 0
#    Sunny
#    Clear

#weather.coverage = 50
# Partly Sunny   
#  Mostly Sunny
#   Partly Cloudy
#   Mostly Cloudy

#weather.coverage = 100
##    Scattered Thunderstorms
##    Showers
##    Scattered Showers
##    Rain and Snow
##    Overcast
##    Light Snow
##    Chance of Rain
##    Chance of Storm
##    Rain
##    Cloudy
##    Mist
##    Storm
##    Thunderstorm
##    Chance of TStorm
##    Dust
##    Light Rain
##    Hail


#winter:
##    Freezing Drizzle
##    Chance of Snow
##    Sleet
##    Snow
##    Icy
##    Snow Showers
##    Flurries

# weather.visibity
# weather.groundfog
#    Fog
#    Smoke
#    Haze
