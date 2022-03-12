# DSC 510
# Week 12
# Programming Assignment Week 12
# Author: Kimberly Cable
# 03/05/2022


from datetime import datetime
from ColorsClass import Colors


def windDegreeToText(degree):
    '''
    Converts degrees to a direction

    args:
        degree (int): wind degrees

    returns:
        direction (str): direction of wind
    '''
    if degree > 337.5:
        direction = "N"
    if degree > 292.5:
        direction = "NW"
    if degree > 247.5:
        direction = "W"
    if degree > 202.5:
        direction = "SW"
    if degree > 157.5:
        direction = "S"
    if degree > 122.5:
        direction = "SE"
    if degree > 67.5:
        direction = "E"
    if degree > 22.5:
        direction = "NE"
    else:
        direction = "N"

    return direction


def weatherDescription(weatherId):
    '''
    Changes the color of the weather description based on the id
    and adds an emoji

    args:
        weatherId (int): Weather id

    returns:
        weatherParm (tuple): weather symbol and color
    '''
    # Initialize Variables
    # Weather Condition codes from OpenWeatherMap API
    THUNDERSTORM = range(200, 300)
    DRIZZLE = range(300, 400)
    RAIN = range(500, 600)
    SNOW = range(600, 700)
    ATMOSPHERE = range(700, 800)
    CLEAR = range(800, 801)
    CLOUDY = range(801, 900)

    if weatherId in THUNDERSTORM:
        weatherParm = ("\U000026C8", Colors.RED)
    elif weatherId in DRIZZLE:
        weatherParm = ("\U0001F327", Colors.LIGHTBLUE)
    elif weatherId in RAIN:
        weatherParm = ("\U0001F327", Colors.CYAN)
    elif weatherId in SNOW:
        weatherParm = ("\U00002744", Colors.LIGHTWHITE)
    elif weatherId in ATMOSPHERE:
        weatherParm = ("\U0001F32B", Colors.DARKGRAY)
    elif weatherId in CLEAR:
        weatherParm = ("\U0001F31E", Colors.YELLOW)
    elif weatherId in CLOUDY:
        weatherParm = ("\U00002601", Colors.LIGHTGRAY)
    else:
        weatherParm = ("", Colors.RESET)

    return weatherParm


def getWeekDay(index):
    '''
    Get day of the week from date index

    args:
        index (int): Day of week index

    returns:
        weekDay (str): Day of the week
    '''
    if index == 0:
        weekDay = "Monday"
    elif index == 1:
        weekDay = "Tuesday"
    elif index == 2:
        weekDay = "Wednesday"
    elif index == 3:
        weekDay = "Thursday"
    elif index == 4:
        weekDay = "Friday"
    elif index == 5:
        weekDay = "Saturday"
    else:
        weekDay = "Sunday"

    return weekDay


def getTimeZone(utcDate, offset):
    '''
    Calculates the Local Date/Time from the UTC Date/Time

    args:
        utcDate (int): UTC date from OpenWeather App
        offset (int): Timezone Offset from OpenWeather App

    returns:
        utcDateInt (int): Local Date/Time
    '''
    localUTCDate = utcDate + offset
    utcDateInt = datetime.utcfromtimestamp(localUTCDate)

    return utcDateInt


def convertDate(utcDate, offset):
    '''
    Convert UTC Date to MM/DD/YYYY format and get day of week

    args:
        utcDate (int): UTC date
        offset (int): Timezone offset from API

    returns:
        localDate (str): MM/DD/YYYY format date
        dayOfWeek (str): Day of the Week
    '''
    localDateInt = getTimeZone(utcDate, offset)

    localDate = datetime.strftime(localDateInt, "%m/%d")
    dayOfWeek = getWeekDay(datetime.date(localDateInt).weekday())

    return localDate, dayOfWeek


def convertTime(utcDate, offset):
    '''
    Converts UTC Date/Time to Local Time

    args:
        utcDate (int): UTC date
        offset (int): Timezone offset from API

    returns:
        localTime (str): Local time
    '''
    localDateInt = getTimeZone(utcDate, offset)

    localTime = datetime.strftime(localDateInt, "%I:%M %p")

    return localTime


def moonPhase(phase):
    '''
    Converts API decimal moon pase to readable format

    args:
        phase (int): decimal moon phase

    returns:
        moonPhase (tuple): {emoji, text}
    '''
    if phase == 0 or phase == 1:
        moonPhase = ("\U0001F311", "New Moon")
    elif phase > 0 and phase < 0.25:
        moonPhase = ("\U0001F312", "Waxing Cresent")
    elif phase == 0.25:
        moonPhase = ("\U0001F313", "First Quarter")
    elif phase > 0.25 and phase < 0.50:
        moonPhase = ("\U0001F314", "Waxing Gibous")
    elif phase == 0.51:
        moonPhase = ("\U0001F315", "Full Moon")
    elif phase > 0.51 and phase < 0.75:
        moonPhase = ("\U0001F316", "Waning Gibous")
    elif phase == 0.75:
        moonPhase = ("\U0001F317", "Last Quarter")
    elif phase > 0.75 and phase < 1:
        moonPhase = ("\U0001F318", "Waning Cresent")

    return moonPhase


def formatForecastPrint(weatherData, units):
    '''
    Formats and Prints the Forecast

    args:
        weatherData (json): Weather data from API
        units (str): temperature unit of measure

    returns:
        None
    '''
    for day in range(len(weatherData["daily"])):
        # Convert date to local date
        localDate, dayOfWeek = convertDate(
            int(weatherData["daily"][day]["dt"]),
            int(weatherData["timezone_offset"])
        )

        # Variables from weatherData
        weatherId = weatherData["daily"][day]["weather"][0]["id"]
        description = weatherData["daily"][day]["weather"][0]["description"]
        temperature = round(weatherData["daily"][day]["temp"]["day"])
        feelsLike = round(weatherData["daily"][day]["feels_like"]["day"])
        minTemp = round(weatherData["daily"][day]["temp"]["min"])
        maxTemp = round(weatherData["daily"][day]["temp"]["max"])

        windSpeed = weatherData["daily"][day]["wind_speed"]

        if units == "F":
            windUnits = "m/h"
        else:
            windUnits = "m/s"

        windDirection = windDegreeToText(
            weatherData["daily"][day]["wind_deg"]
        )
        humidity = weatherData["daily"][day]["humidity"]
        clouds = weatherData["daily"][day]["clouds"]
        precipitation = weatherData["daily"][day]["pop"]
        sunset = convertTime(
            weatherData["daily"][day]["sunset"],
            int(weatherData["timezone_offset"])
        )
        sunrise = convertTime(
            weatherData["daily"][day]["sunrise"],
            int(weatherData["timezone_offset"])
        )
        moonPhaseIcon, moonPhaseTxt = moonPhase(
            weatherData["daily"][day]["moon_phase"]
        )
        weatherSymbol, color = weatherDescription(weatherId)

        # Format and Print Weather
        print(f"{'':3}", end="")
        print(f"\n{Colors.BLUE}{dayOfWeek}: {localDate}{Colors.RESET}")

        print(color)
        print(f"{'':3}", end="")
        print(f"{weatherSymbol:3} {temperature}°{units}")
        print(f"{'':3}", end="")
        print(f"feels like {feelsLike}°{units}. {description.capitalize()}")
        print(Colors.RESET)

        print(f"{'':3}", end="")
        line1 = f"{Colors.BOLD}Min Temp: {Colors.RESET}{minTemp}°{units}"
        print(f"{line1:<30}", end=" ")
        print(f"{Colors.BOLD}Max Temp: {Colors.RESET}{maxTemp}°{units}")

        print(f"{'':3}", end="")
        line2 = f"{Colors.BOLD}Wind: {Colors.RESET}"
        line2 += f"{windSpeed} {windUnits} {windDirection}"
        print(f"{line2:<30}", end=" ")
        print(f"{Colors.BOLD}Humidity: {Colors.RESET}{humidity}%.")

        print(f"{'':3}", end="")
        line3 = f"{Colors.BOLD}Clouds: {Colors.RESET}{clouds}%"
        print(f"{line3:<30}", end=" ")
        print(f"{Colors.BOLD}Precipitation: {Colors.RESET}{precipitation}%")

        print(f"{'':3}", end="")
        line4 = f"{Colors.BOLD}Sunrise: {Colors.RESET}{sunrise}"
        print(f"{line4:<30}", end=" ")
        print(f"{Colors.BOLD}Sunset: {Colors.RESET}{sunset}")

        print(f"{'':3}", end="")
        print(f"{Colors.BOLD}Moon: {Colors.RESET}", end="")
        print(f"{moonPhaseIcon:3} {moonPhaseTxt}")


def printData(weatherData, units, cityName):
    '''
    Formats and prints the current weather, forecast and alerts

    args:
        weatherData (json): Weather data from API
        units (str): temperature unit of measure
        cityName (str): Name of City

    returns:
        None
    '''
    # Variables from weatherData
    city = cityName
    weatherId = weatherData["current"]["weather"][0]["id"]
    description = weatherData["current"]["weather"][0]["description"]
    temperature = round(weatherData["current"]["temp"])
    feelsLike = round(weatherData["current"]["feels_like"])

    weatherSymbol, color = weatherDescription(weatherId)

    forecastLength = len(weatherData["daily"])

    if "alerts" in weatherData:
        alertEvent = weatherData["alerts"][0]["event"].upper()
        alertFrom = weatherData["alerts"][0]["sender_name"]
        alertDesc = weatherData["alerts"][0]["description"]
        # Convert UTC date to MM/DD
        alertStart, alertStartDayOfWeek = convertDate(
            int(weatherData["alerts"][0]["start"]),
            int(weatherData["timezone_offset"])
        )
        alertEnd, alertEndDayOfWeek = convertDate(
            int(weatherData["alerts"][0]["end"]),
            int(weatherData["timezone_offset"])
        )

    # Print Weather
    print(f"\n{'':-<40}")

    print(f"{Colors.BOLD}Current temperature in {city} is{Colors.RESET}")

    print(f"{'':3}", end="")
    print(color)
    print(f"{weatherSymbol:3} {temperature}°{units}")

    print(f"{'':3}", end="")
    print(f"feels like {feelsLike}°{units}. {description.capitalize()}")
    print(Colors.RESET)

    # Print alerts
    if "alerts" in weatherData:
        print(f"{'':3}", end="")
        print(f"{Colors.RED}{Colors.BOLD}ALERT: {alertEvent}{Colors.RESET}")

        print(f"{'':6}", end="")
        print(f"{Colors.RED}{Colors.BOLD}From: {Colors.RESET}", end="")
        print(f"{Colors.RED}{alertFrom}")

        print(f"{'':6}", end="")
        print(f"{Colors.RED}{Colors.BOLD}Starts: {Colors.RESET}", end="")
        line = f"{Colors.RED}{alertStartDayOfWeek}, {alertStart}{Colors.RESET}"
        print(f"{line:<26}", end=" ")
        print(f"{Colors.RED}{Colors.BOLD}Ends: {Colors.RESET}", end=" ")
        print(f"{Colors.RED}{alertEndDayOfWeek}, {alertEnd}{Colors.RESET}")

        print(f"{'':6}", end="")
        print(f"{Colors.RED}{alertDesc}{Colors.RESET}")

    # Print Forecast
    print(f"\n{Colors.BOLD}{Colors.UNDERLINE}", end="")
    print(f"{forecastLength} Day Forecast{Colors.RESET}")
    formatForecastPrint(weatherData, units)

    print(f"{'':-<40}")
