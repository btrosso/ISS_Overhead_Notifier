import requests
import smtplib
import time
import pytz
from datetime import datetime
from dateutil import parser


def is_overhead(my_lat, my_long, iss_lat, iss_long):
    if (my_long+5 > iss_long > my_long-5) and (my_lat+5 > iss_lat > my_lat-5):
        return True


MY_LAT = 33.244041
MY_LONG = -86.816872

response = requests.get(url="http://api.open-notify.org/iss-now.json")
response.raise_for_status()
data = response.json()

iss_latitude = float(data["iss_position"]["latitude"])
iss_longitude = float(data["iss_position"]["longitude"])

# Your position is within +5 or -5 degrees of the ISS position.
#
# if MY_LONG+5 > ISS_TEST_LONG > MY_LONG-5:
#     if MY_LAT+5 > ISS_TEST_LAT > MY_LAT-5:
#         print("look up")


def is_night():
    parameters = {
        "lat": MY_LAT,
        "lng": MY_LONG,
        "formatted": 0,
    }

    sun_response = requests.get("https://api.sunrise-sunset.org/json", params=parameters)
    sun_response.raise_for_status()
    sun_data = response.json()

    nz_zone = pytz.timezone('US/Central')
    sunrise = sun_data["results"]["sunrise"]
    sunset = sun_data["results"]["sunset"]

    converted_sunrise = datetime.strftime(parser.parse(sunrise).astimezone(nz_zone), "%I:%M:%S %p")
    sunrise_parse = converted_sunrise.split(":")
    converted_sunset = datetime.strftime(parser.parse(sunset).astimezone(nz_zone), "%I:%M:%S %p")
    sunset_parse = converted_sunset.split(":")

    time_now = datetime.strftime(datetime.now(), "%I:%M:%S %p")
    time_now_parse = time_now.split(":")

    if int(sunset_parse[0]) + 2 < int(time_now_parse[0]) or int(time_now_parse[0]) < int(sunrise_parse[0]) - 2:
        return True


while True:
    time.sleep(60)
    if is_overhead(my_lat=MY_LAT, my_long=MY_LONG, iss_lat=iss_latitude, iss_long=iss_longitude) and is_night():
        my_email = "314159brandon314159@gmail.com"
        password = "HolyMoly123!!"
        with smtplib.SMTP("smtp.gmail.com", port=587) as connection:
            connection.starttls()
            connection.login(user=my_email, password=password)
            connection.sendmail(
                from_addr=my_email,
                to_addrs="riseandgrind2020@yahoo.com",
                msg=f"Subject: ISS Notification!!\n\nGo outside and look up!\n"
                    f"The International Space Station should be visible!"
            )
