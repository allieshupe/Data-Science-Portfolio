# DSC 510
# Week 10
# Course Project
# Author Allie Shupe
# 8/12/2023

import requests


# get the zip code or city from the user
def city_zipcode():
    searchType = input('If searching by zip code enter "zipcode"; '
                       'if searching by city enter "city": ')
    searchType = searchType.lower()
    while searchType != "zipcode" and searchType != "city":
        searchType = str(input('Invalid input. '
                               'If searching by zip code enter "zipcode"; '
                               'if searching by city, enter "city": '))
    if searchType == "zipcode":
        areaSearch = input('Please enter the zipcode: ')
    else:
        areaSearch = input('Please enter the city in the format '
                           '"City,State Abbreviation": ').lower()
    return searchType, areaSearch


# get the weather data from OpenWeatherMap
def getWeather(lat, lon, apikey, url):
    try:
        fullURL = url + 'weather?lat=' + lat + '&lon=' + lon + '&appid=' + apikey
        weather = requests.request("GET", fullURL)
    except requests.exceptions.ConnectionError:
        print('There is an error with your network connection.')
    else:
        weather = weather.json()
        mainWeather = weather['main']
        temperature = mainWeather["temp"]
        feelsLike = mainWeather["feels_like"]
        tempMin = mainWeather["temp_min"]
        tempMax = mainWeather["temp_max"]
        pressure = mainWeather["pressure"]
        humidity = mainWeather["humidity"]
        cloudWeather = weather["clouds"]
        clouds = cloudWeather["all"]
        description = weather['weather'][0]['description']
    return temperature, feelsLike, tempMin, tempMax, pressure, humidity, clouds, description


# Get the latitude and longitude for the city/zip code being searched
def getLatLon(searchType, areaSearch, geoURL, apikey):
    error = ''
    lat = 0
    lon = 0
    city = ''
    state = ''
    if searchType == "city":
        try:
            fullURL = geoURL + "direct?q=" + areaSearch + ",US&appid=" + apikey
            coords = requests.request("GET", fullURL)
            coords = coords.json()
        except requests.exceptions.ConnectionError:
            print('There is an error with your network connection.')
        else:
            try:
                lat = str(coords[0]['lat'])
                lon = str(coords[0]['lon'])
                city = coords[0]['name']
                state = coords[0]['state']
                print('The connection to the web service was successful.')
            except IndexError:
                error = 'invalid input.'
                print('Error: '+error)
    else:
        try:
            fullURL = geoURL + "zip?zip=" + areaSearch + ",US&appid=" + apikey
            coords = requests.request("GET", fullURL)
            coords = coords.json()
        except requests.exceptions.ConnectionError:
            print('There is an error with your network connection.')
        else:
            try:
                lat = str(coords['lat'])
                lon = str(coords['lon'])
                city = coords['name']
                state = coords['country']
                print('The connection to the web service was successful.')
            except KeyError:
                error = coords['message']
                print('Error: ' + error)
    return lat, lon, city, error, state


# Convert temperature to desired units
def tempConversion(temp, units):
    units = units.lower()
    if units == "kelvin":
        temp = temp
    elif units == "celsius":
        temp = temp - 273.15
    else:
        temp = (temp - 273.15) * (9 / 5) + 32
    return temp


# print the output
def pretty_print(Dict, city, state):
    print(f"Today's weather in {city}, {state}:")
    print(f'__________________________________')
    for key, value in Dict.items():
        formatting = ('{: <20}{: <}'.format(key, value))
        print(f'{formatting}')


def main():
    print('Welcome. This program will display weather data for any given US city.')

    # enter API Key
    apikey = ''
    weatherURL = 'https://api.openweathermap.org/data/2.5/'
    geoURL = 'https://api.openweathermap.org/geo/1.0/'

    # start while loop
    cont = "y"
    while cont == "y":
        # get weather data from the api
        searchType, areaSearch = city_zipcode()
        lat, lon, city, error, state = getLatLon(searchType, areaSearch, geoURL, apikey)

        # only continue if no errors were thrown
        if error == '':
            temperature, feelsLike, tempMin, tempMax, pressure, humidity, clouds, description \
                = getWeather(lat, lon, apikey, weatherURL)

            # ask user which unit of measurement they would prefer
            units = input('Enter "Kelvin", "Celsius", or "Fahrenheit" for temperature units: ')
            while units.lower() != "kelvin" and units.lower() != "celsius" and \
                    units.lower() != "fahrenheit":
                units = input('Invalid input. Please enter "Kelvin", "Celsius", '
                              'or "Fahrenheit" for temperature units: ')

            # convert the temperatures to the desired units and add units
            unitFormat = u'\N{DEGREE SIGN}' + units[0].upper()
            temperature = str(round(tempConversion(temperature, units), 2)) + unitFormat
            feelsLike = str(round(tempConversion(feelsLike, units), 2)) + unitFormat
            tempMin = str(round(tempConversion(tempMin, units), 2)) + unitFormat
            tempMax = str(round(tempConversion(tempMax, units), 2)) + unitFormat

            # add measurement units to pressure, humidity and clouds
            pressure = str(round(pressure, 2)) + ' KPa'
            humidity = str(humidity) + '%'
            clouds = str(clouds) + '%'

            # create a dictionary to store all weather values
            weatherDict = {"Temperature": temperature,
                           "Feels Like": feelsLike,
                           "Temperature Min": tempMin,
                           "Temperature Max": tempMax,
                           "Pressure": pressure,
                           "Humidity": humidity,
                           "Cloud Coverage": clouds,
                           "Description": description
                           }

            pretty_print(weatherDict, city, state)

            # ask if user would like to look up another city
            cont = input('Enter "y" if you would like to lookup another city, "n" to exit.').lower()
            while cont != 'y' and cont != 'n':
                cont = input('Invalid input. Enter "y" if you would like to lookup another '
                             'city, "n" to exit.')

    # print thank you message
    print('Thank you for using this program.')


# call to main()
if __name__ == "__main__":
    main()
