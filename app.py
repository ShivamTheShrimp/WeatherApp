import requests
import sys

def unitConverter(k):
    f_unrounded = (int(k)-273.15) * 1.8 + 32
    f = round(f_unrounded)
    return f
def getCords():
    city = input("What city would you like to get the weather for?: ")
    state = input("What state is that in?: ")
    # city = "Fremont"
    # state = "California"
    current_weather_check = input("Would you like current weather(y/n)?: ")
    daily_weather_check = input("Would you like daily weather(y/n)?: ")
    # current_weather_check = "n"
    # daily_weather_check = "y"

    if current_weather_check.lower() == "y" or current_weather_check.lower() == "n":
        if current_weather_check == "y":
            check_curr = True
        else:
            check_curr = False
    else:
        print("Not valid input")
        sys.exit()
    
    if daily_weather_check.lower() == "y" or daily_weather_check.lower() == "n":
        if daily_weather_check == "y":
            check_daily = True
        else:
            check_daily = False
    else:
        print("Not valid input")
        sys.exit()
    
    url = f"http://api.openweathermap.org/geo/1.0/direct?q={city}&limit=5&appid=dbe91dc852df30fc113a73c5947a7480"
    response = requests.get(url)

    if response.status_code == 200:
        cord_data = response.json()

        location = next((item for item in cord_data if item.get("state") == state), None)

        if location:
            lat, lon = location["lat"], location["lon"]
            return lat, lon, city, state, check_curr,check_daily
        else:
            print(f"No matching location found for {state}.")
            sys.exit()
    else:
        print("Failed to fetch data.")
        sys.exit()

def getCurrentWeather(lat,lon,city,state):
    url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid=dbe91dc852df30fc113a73c5947a7480"
    response = requests.get(url)

    if response.status_code == 200:
        cwd = response.json() #cwd means current weather data
        cwd_main = cwd["main"]
        cwd_temp_kelvin = cwd_main["temp"]
        # cwd_temp_unrounded = (int(cwd_temp_kelvin) - 273.15) * 1.8 + 32
        # cwd_temp = round(cwd_temp_unrounded,2)
        cwd_temp = unitConverter(int(cwd_temp_kelvin))
        
        print(f"The current temperature in {city}, {state} is {cwd_temp}°F")
    else:
        print("Error fetching data")
        sys.exit()


def getDailyWeather(lat,lon,city,state):
    print(lat, lon)
    # url = f"https://api.openweathermap.org/data/2.5/forecast?lat={lat}&{lon}=20&units=imperialc&appid=dbe91dc852df30fc113a73c5947a7480"
    url = f"https://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&units=imperialc&cnt=16&appid=dbe91dc852df30fc113a73c5947a7480"
    
    response = requests.get(url)

    if response.status_code == 200:
        dwd = response.json() #daily weather date
        
        dwd_lst = dwd["list"]
        for i in range(0,15): ##change 15 when we increase count to cnt-1
            dwd_1 = dwd_lst[i]
            date_1 = dwd_1['dt_txt']
            b = date_1.split('-')
            year = b[0]
            month = b[1]
            c = date_1.split()
            day = b[2]
            d = day.split()
            day = d[0]
            time = d[1]
            dwd_main = dwd_1['main']
            dwd_temp_kelvin = dwd_main['temp']
            dwd_temp = unitConverter(int(dwd_temp_kelvin))
            


            #time
            if i == 0 or i == 8:
                time = "3am"
            if i == 1 or i == 9:
                time = "6am"
            if i == 2 or i == 10:
                time = "9am"
            if i == 3 or i == 11:
                time = "12pm"
            if i == 7 or i == 15:
                time = "12am"
            
            if i == 4 or i == 12:
                time = "3pm"
            if i == 5 or i == 13:
                time = "6pm"
            if i == 6 or i == 14:
                time = "9pm"


            #month

            months = {'01':'January','02':'February','03':'March','04':'April','05':'May','06':'June','07':'July','08':'August','09':'September','10':'October','11':'November','12':'December'}
            month = months[month]

            #days
            st = ['01','21','31']
            nd = ['02','22']
            rd = ['03','23']

            if day in st:
                day = day +"st"
            elif day in nd:
                day = day+"nd"
            elif day in rd:
                day = day+"rd"
            else:
                day = day+"th"
            
            
            print(f"{month},{day},{year},{time} the temperature is {dwd_temp}°F")
            
        

        
    else:
        print("Error fetching data")
        sys.exit()






lat,lon,city,state,check_curr,check_daily = getCords()
if check_curr == True:
    getCurrentWeather(lat,lon,city,state)
if check_daily == True:
    getDailyWeather(lat,lon,city,state)

