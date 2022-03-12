# DSC 510
# Week 12
# Programming Assignment Week 12
# Author: Kimberly Cable
# 03/05/2022

import requests
import sys


class ApiServices:
    """
    ApiServices Class

    args:
        None

    returns:
        None
    """

    def __init__(self):
        self.baseUrl = ""
        self.payload = ""

    def setBaseUrl(self, baseUrl):
        '''
        Set Base url

        args:
            None

        returns:
            None
        '''
        self.baseUrl = baseUrl

    def setPayload(self, payload):
        '''
        Set payload

        args:
            None

        returns:
            None
        '''
        self.payload = payload

    def callApi(self):
        '''
        Calls OpenWeatherApp to retrieve json data
        Exits if exception found
        Prints message if API cannot find zip code or city

        args:
            option (str): Get weather by city or zip code
                Expects 'zip' or 'city' default 'city'
            optionValue (str): either zip code or city
            units (str): whether to display temperature in Kelvin,
                    Farenheit, or Celcius
                Expects: 'K', 'F', or 'C'

        returns:
            prettyData: json data
            error (str): error message
        '''
        # Initialize Variables
        headers = {}

        # Call API, exit out if exception raised
        try:
            response = requests.request(
                "GET", self.baseUrl, headers=headers, params=self.payload
            )
        except requests.exceptions.HTTPError:
            print("We can't seem to locate the weather satellite.")
            print("Please try again later")
            sys.exit()
        except requests.exceptions.RequestException:
            print("Seems the weather satelites are currently down.")
            print("Please try again later")
            sys.exit()

        # Load data into json and return weather data
        # otherwise print error and exit
        if response.status_code == requests.codes.ok:
            parsedData = response.json()
            return parsedData
        else:
            return {
                "Error": "Sorry, we couldnt find your city! Please re-enter"
            }
