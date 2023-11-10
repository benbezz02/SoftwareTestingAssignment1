from currentLoc import currentLoc
from futureLoc import futureLoc


def main():
    runProgramme = True

    while runProgramme:
        print("WeatherWear.com")
        print("---------------")
        print("1. Recommend clothing for current location")
        print("2. Recommend clothing for future location")
        print("3. Exit")

        user_input = input("\nEnter choice: ")

        match (user_input):
            case "1":
                temperature, precipitation = currentLoc.getGeoLocationData()

                # Error has occured in function above
                if temperature is None and precipitation is None:
                    return 1

                # Printing output
                currentLoc.printMessage(temperature, precipitation)
            case "2":
                location, date = futureLoc.getFutureInfo()
                futureTemperature, futurePrecipitation = futureLoc.getFutureLocData(
                    location, date
                )

                # Error has occured in function above
                if futureTemperature is None and futurePrecipitation is None:
                    return 2

                # Printing output
                futureLoc.printMessage(
                    location, date, futureTemperature, futurePrecipitation
                )
            case "3":
                print("Exiting the programme...")

                # Exit loop
                runProgramme = False
            case _:
                # Any other input but 1, 2 or 3
                print("Invalid choice entered. Please Enter 1, 2 or 3.\n")

    # Returning 0 represents successful exit
    return 0


if __name__ == "__main__":
    main()
