import network 
import urequests
import utime
import ujson
from machine import Pin, I2C
from rotary_irq_rp2 import RotaryIRQ
import ssd1306
from dht import DHT11, InvalidChecksum

sensor = DHT11(Pin(0))

led_R = Pin(28, mode=Pin.OUT)
led_V = Pin(27, mode=Pin.OUT)
led_B = Pin(26, mode=Pin.OUT)


wlan = network.WLAN(network.STA_IF) # met la raspi en mode client wifi
wlan.active(True) # active le mode client wifi

ssid = 'IIM_Private'
password = 'Creatvive_Lab_2023'
wlan.connect(ssid, password) # connecte la raspi au réseau

i2c = I2C(0, sda=Pin(16), scl=Pin(17))
d = i2c.scan()

r = RotaryIRQ(
    pin_num_clk=14,
    pin_num_dt=13,
    min_val=1,
    max_val=5,
    reverse=True,
    incr=1,
    range_mode=RotaryIRQ.RANGE_BOUNDED,
    pull_up=True,
    half_step=False,
)

url = "https://api.openweathermap.org/data/2.5/weather?lat=48.90&lon=2.33&appid=a32a825225d19883c0b3eb8e44dd36a1"

api = urequests.get(url) # lance une requete sur l'url

val_old = r.value()
print("Ok")
while True:
    val_new = r.value()

    if val_old != val_new:
        led_R.off()
        led_V.off()
        led_B.off()
        val_old = val_new
        display = ssd1306.SSD1306_I2C(128, 64, i2c)
        
        if val_new == 1:
            display.text("Temperature", 0, 0,1)
            temp_Ext = "Ext : " + str(round(api.json()['main']['temp']-273, 2)) + " deg"
            temp_Int = "Int : " + str(sensor.temperature) + " deg"
            display.text(temp_Ext, 0, 16)
            display.text(temp_Int, 0, 32)
            
        elif val_new == 2:
            display.text("Weather", 0, 0,1)
            display.text(api.json()['weather'][0]['main'], 0, 16)
            
        elif val_new == 3:
            display.text("Sunrise", 0, 0,1)
            formated_time = utime.localtime(api.json()['sys']['sunrise'])
            display.text("The sun rises at", 0, 16)
            display.text('%02d:%02d' % (formated_time[3], formated_time[4]), 0, 32)
            
        elif val_new == 4:
            display.text("Sunset", 0, 0,1)
            formated_time = utime.localtime(api.json()['sys']['sunset'])
            display.text("The sun sets at", 0, 16)
            display.text('%02d:%02d' % (formated_time[3], formated_time[4]), 0, 32)
            
        elif val_new == 5:
            display.text("Bike today ?", 0, 0,1)
            temp = api.json()['main']['temp']-273
            if temp <= 8:
                led_B.on()
                display.text("It's too cold", 0, 16)
            if temp > 8 and temp < 30:
                led_V.on()
                display.text("It's perfect", 0, 16)
            if temp >= 30:
                led_R.on()
                display.text("It's too hot", 0, 16)

        display.show()













