from weather import weather
import requests


class currentLoc:
    def getGeoLocationData():
        ipAddress = currentLoc.getIPAddress()

        if ipAddress is None:
            return None, None

        weatherURL = "https://weatherapi-com.p.rapidapi.com/current.json"

        querystring = {"q": ipAddress}

        headers = {
            "X-RapidAPI-Key": "a740b2b326msh0bfa143902fde7fp16deb3jsnff739d0370b6",
            "X-RapidAPI-Host": "weatherapi-com.p.rapidapi.com",
        }

        try:
            response = requests.get(
                weatherURL, headers=headers, params=querystring, timeout=3
            )

            if response.status_code != 200:
                print(
                    "Status:",
                    response.status_code,
                    "Problem encountered with WeatherAPI. Exiting.",
                )
                return None, None

            return (
                response.json()["current"]["temp_c"],
                response.json()["current"]["precip_mm"],
            )

        except requests.exceptions.RequestException as error:
            print("Error with WeatherAPI:", error, "Exiting")
            return None, None

    def getIPAddress():
        try:
            response = requests.get("https://ipinfo.io", timeout=3)

            if response.status_code != 200:
                print(
                    "Warning Status:",
                    response.status_code,
                    " Problem encountered with IP Info, Moving to IP-API",
                )

                ipAddress = currentLoc.getIPAddressBackup()
            else:
                ipAddress = response.json()["ip"]

            return ipAddress

        except requests.exceptions.RequestException as error:
            print("Error with IP Info:", error, "Moving to IP-API")
            return currentLoc.getIPAddressBackup()

    def getIPAddressBackup():
        try:
            ipURL = "http://ip-api.com/json/"

            response = requests.get(ipURL)

            if response.status_code != 200:
                print(
                    "Status:",
                    response.status_code,
                    "Problem encountered with IP-API. Exiting",
                )
                return None

            ip = response.json()["query"]

            return ip

        except requests.exceptions.RequestException as error:
            print("Error with IP-API:", error, "Exiting")
            return None

    def printMessage(temperature, precipitation):
        if weather.isCold(temperature):
            print("It is cold so you should wear warm clothing.")
        else:
            print("It is warm so you should wear light clothing.")

        if weather.isRainy(precipitation):
            print("It is currently raining so you do need an umbrella.\n")
        else:
            print("It is not raining so you don't need an umbrella.\n")
