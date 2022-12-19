import buildWeatherUrl
from ColorsClass import Colors


def getTempUnits():
    '''
    Get the temperature unit of measure from the user

    args:
        None

    returns:
        units (str): unit of measure
            Expects: 'F' for Fahrenheit
                     'C' for Celcius
                     'K' for Kelvin
    '''
    # Initialize variables
    IMPERIAL = "F"
    METRIC = "C"
    KELVIN = "K"

    while True:
        print("\nWould you like to view the temperature in:")
        print(f"{'':5}[F] - F for Fahrenheit ")
        print(f"{'':5}[C] - C for Celcius")
        print(f"{'':5}[K] - K to Kelvin")

        try:
            userOption = str(input().upper().strip())
        except ValueError:
            print("Sorry, that is incorrect. Please enter F, C, or K")

        if userOption == IMPERIAL:
            units = "F"
            break
        elif userOption == METRIC:
            units = "C"
            break
        elif userOption == KELVIN:
            units = "K"
            break
        else:
            print(Colors.RED)
            print("\nSorry, incorrect choice. ")
            print(Colors.RESET)

    return units


def getByZipCode():
    '''
    Gets the Zip Code from the user and prints weather

    args:
        None

    returns:
        None
    '''

    while True:
        try:
            print("\nPlease enter a U.S. zip code")
            zipCode = int(input())

            if len(str(zipCode)) == 5:
                break
            else:
                print(Colors.RED)
                print("\nSorry, your Zip Code must only 5 numbers.")
                print(Colors.RESET)
        except ValueError:
            print(Colors.RED)
            print("\nSorry, the Zip Code you entered is not correct.")
            print(Colors.RESET)

    # Get unit of measure from user
    temperatureUnits = getTempUnits()

    # print weather
    buildWeatherUrl.callWeatherApi("zip", zipCode, temperatureUnits)


def getByCity():
    '''
    Gets the City and State from the user and prints weather

    args:
        None

    returns:
        None
    '''
    while True:
        try:
            print("\nPlease enter a U.S. city")
            city = input().strip().lower()
            break
        except ValueError:
            print(Colors.RED)
            print("\nSorry, the City you entered is not correct.")
            print(Colors.RESET)

    temperatureUnits = getTempUnits()

    buildWeatherUrl.callWeatherApi("city", city, temperatureUnits)


def main():
    '''
    Gets the weather by either a zip code or city/state

    args:
        None

    returns:
        None
    '''
    # Initialize Constants
    FINISHED = "X"

    # Print Welcome
    print(Colors.BOLD)
    print("Welcome to Today's Weather Service!")
    print(Colors.RESET)

    # Ask user if want to lookup by city or zip code
    # 'X' to exit
    while True:
        print("\nWould you like to lookup by:")
        print(f"{'':5}Enter 1 for Zip Code")
        print(f"{'':5}Enter 2 for City")
        print(f"{'':5}Enter X to Quit")

        try:
            userOption = input()
            if int(userOption) == 1:
                getByZipCode()
            elif int(userOption) == 2:
                getByCity()
            else:
                print(Colors.RED)
                print("\nIncorrect choice. Please enter 1, 2, or X")
                print(Colors.RESET)
        except ValueError:
            if userOption.strip().upper() == FINISHED:
                break
            else:
                print(Colors.RED)
                print("\nIncorrect choice. Please enter 1, 2, or X")
                print(Colors.RESET)


if __name__ == "__main__":
    main()
