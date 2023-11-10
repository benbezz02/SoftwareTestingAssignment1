from weather import weather
from datetime import datetime
import requests


class futureLoc:
    def getFutureInfo():
        airportCode = input("Enter a Airport IATA Code: ")

        # Valid input checker
        while len(airportCode) != 3 or not airportCode.isalpha():
            print("Invalid input detected.")
            airportCode = input("Enter a valid Airport IATA Code(e.g. MLA): ")

        # set any lowercase input to all uppercase
        airportCode = airportCode.upper()

        date = input("Enter future date(up to 10 days), in the format YYYY-MM-DD: ")
        currentDate = datetime.today()

        # Valid input checker
        while True:
            try:
                # Checking date is in format year-month-day
                date = datetime.strptime(date, "%Y-%m-%d")

                # Checking date is in the 10 day ahead range
                if 0 <= ((date - currentDate).days + 1) <= 10:
                    break
            except:
                print("Invalid input detected.")
                date = input(
                    "Enter a valid future date(up to 10 days), in the format YYYY-MM-DD(e.g. 2023-10-20): "
                )

        return airportCode, date

    def getFutureLocData(airportCode, date):
        url = "https://weatherapi-com.p.rapidapi.com/forecast.json"

        querystring = {"q": "iata:" + airportCode, "date": date}

        headers = {
            "X-RapidAPI-Key": "a740b2b326msh0bfa143902fde7fp16deb3jsnff739d0370b6",
            "X-RapidAPI-Host": "weatherapi-com.p.rapidapi.com",
        }

        try:
            response = requests.get(url, headers=headers, params=querystring)

            # Status code not equal to 200 will occur if invalid get ran
            if response.status_code != 200:
                print(
                    "Status:",
                    response.status_code,
                    "Problem encountered with WeatherAPI. Exiting.",
                )

                # Returning None, None to indicate error has occured
                return None, None

            # Return temperature and precipication from the valid recieved data
            return (
                response.json()["forecast"]["forecastday"][0]["day"]["avgtemp_c"],
                response.json()["forecast"]["forecastday"][0]["day"]["totalprecip_mm"],
            )

        # Except will occur if WeatherApi Server is down
        except requests.exceptions.RequestException as error:
            print("Error with WeatherAPI:", error, "Exiting")
            return None, None

    def printMessage(location, date, temperature, precipitation):
        print("On the " + date.strftime("%d/%m/%Y") + " at " + location + " airport: ")

        if weather.isCold(temperature):
            print("It will be cold so you should wear warm clothing.")
        else:
            print("It will be warm so you should wear light clothing.")

        if weather.isRainy(precipitation):
            print("It is likely to rain so you do need an umbrella.\n")
        else:
            print("It is likely to not rain so you don't need an umbrella.\n")
