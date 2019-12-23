from star import Star
from gpiozero.tools import random_values
from signal import pause
import requests
import schedule
import datetime

star = Star(pwm=True)
leds = star.leds

temp = 10

def get_temp():
    base_url = "https://api.darksky.net/forecast/"
    key = "211b3687d8ca6996aa8aa64713a8a2be"
    lat = "53.1457525"
    long = "-0.754067"
    payload = {"exclude": "minutely, hourly, daily, alerts, flags", "units": "uk2"}
    url = base_url + key + "/" + lat + "," + long
    r = requests.get(url, params=payload)
    data = r.json()
    global temp
    temp = float(data["currently"]["temperature"])
    
schedule.every().hour.do(get_temp)

while True:
    schedule.run_pending()
    time.sleep(1)
    
try:
    for led in leds:
        led.source_delay = temp/100
        led.source = random_values()
    pause()
except KeyboardInterrupt:
    star.off()
    star.close()