# DSC 510
# Week 12
# Programming Assignment Week 12
# Author: Kimberly Cable
# 03/05/2022

from configparser import ConfigParser
import os
import sys
from ApiServicesClass import ApiServices
from ColorsClass import Colors
import formatWeather


def getApiKey():
    '''
    Gets the API key from config file

    Expects config file = "secrets.ini"
        [openweather]
        api_key = <OPEN-WEATHER-API-KEY>

    args:
        None

    returns:
        apiKey (str): OpenWeatherMap API Key
    '''
    # Open and read the config file
    config = ConfigParser()
    config.read(os.path.join(sys.path[0], "secrets.ini"))

    apiKey = config["openweather"]["api_key"]

    # return the API Key
    return apiKey


def convertUnits(units):
    '''
    Sets up unit of measure depending on user's input

    args:
        units (str): Unit of measure
            Expects: 'C' - metric
                     'F' - Farenheit
                     'K' - Kelvin (default)
    '''
    # Builds to base url with temperature units of measure
    if units == "C":
        parmUnits = "metric"
    elif units == "F":
        parmUnits = "imperial"
    else:
        parmUnits = ""

    return parmUnits


def buildBaseUrl(option, optionValue, units):
    '''
    Builds the Weather URL for OpenWeatherMap API

    Payload: OpenWeatherMap API parameters
        Parameters:
            City Name = "q": [{city name}
              or
            Zip Code = "zip": {zip code}

            API Key = "appid": {API Key}
            Units of Measure: "units": {units}

    args:
        option (str): Get weather by city or zip code
            Expects 'zip' or 'city' default 'city'
        optionValue (str): either zip code or city
        units (str): whether to display temperature in Kelvin,
                Farenheit, or Celcius
            Expects: 'K', 'F', or 'C'

    returns:
        payload (str): OpenWeatherMap API url payload
    '''
    # Initialize variables
    payload = {}

    # Check if by zip or city
    if option == "zip":
        payload["zip"] = optionValue
    else:
        payload["q"] = optionValue

    # Temperature units of measure
    parmUnits = convertUnits(units)
    payload["units"] = parmUnits

    # API Key
    apiKey = getApiKey()
    payload["appid"] = apiKey

    return payload


def buildOneCallUrl(baseWeatherData, units):
    '''
    Formats the OneCall OpenWeatherMap API parameters
        Payload:
            Latitude: "lat": {latitude}
            Longitude: "lon": {longitude}
            API Key: "appid": {API Key}
            Units of Measure: "units": {units}
    args:
        oneCallData (json): json data from weather API call
        units (str): Temperature unit of measure
            expects: 'C' - Metric
                     'F' - Farenheit
                     'K' - Kelvin (default)

    returns:
        payload (str): OpenWeatherMap API url parameters
        cityName (str): City name
    '''
    # Initialize variables
    payload = {}

    latitude = baseWeatherData["coord"]["lat"]
    longitude = baseWeatherData["coord"]["lon"]
    cityName = baseWeatherData["name"]

    payload["lat"] = {latitude}
    payload["lon"] = {longitude}

    # Temperature units of measure
    parmUnits = convertUnits(units)
    payload["units"] = parmUnits

    # API Key
    apiKey = getApiKey()
    payload["appid"] = apiKey

    return payload, cityName


def callWeatherApi(option, optionValue, units):
    '''
    Calls the OpenWeatherMap Api

    args:
        option (str): Get weather by city or zip code
            Expects 'zip' or 'city' default 'city'
        optionValue (str): either zip code or city
        units (str): whether to display temperature in Kelvin,
                Farenheit, or Celcius
            Expects: 'K', 'F', or 'C'

    returns:
        None
    '''
    # Constants
    BASE_WEATHER_API_URL = "https://api.openweathermap.org/data/2.5/weather"
    ONE_CALL_API_URL = "http://api.openweathermap.org/data/2.5/onecall"

    # Build the Weather URL
    baseParameters = buildBaseUrl(option, optionValue, units)

    # Call OpenWeatherMap API
    baseWeatherAPI = ApiServices()
    baseWeatherAPI.setBaseUrl(BASE_WEATHER_API_URL)
    baseWeatherAPI.setPayload(baseParameters)
    baseWeatherData = baseWeatherAPI.callApi()

    # If successful, build OneCall URL and print weather
    if "Error" in baseWeatherData:
        errorMsg = baseWeatherData["Error"]
        print(f"\n{Colors.RED}{errorMsg}{Colors.RESET}")
    else:
        oneCallParameters, cityName = buildOneCallUrl(baseWeatherData, units)

        oneCallWeatherAPI = ApiServices()
        oneCallWeatherAPI.setBaseUrl(ONE_CALL_API_URL)
        oneCallWeatherAPI.setPayload(oneCallParameters)
        weatherData = oneCallWeatherAPI.callApi()

        if "Error" in weatherData:
            errorMsg = weatherData['Error']
            print(f"\n{Colors.RED}{errorMsg}{Colors.RESET}")
        else:
            formatWeather.printData(weatherData, units, cityName)
