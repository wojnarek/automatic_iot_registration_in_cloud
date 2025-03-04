import time
import board
import adafruit_dht

dht_device = adafruit_dht.DHT11(board.D4)

previous_temperature = None
previous_humidity = None

def get_sensor_data():
    global previous_temperature, previous_humidity
    try:
        
        temperature = dht_device.temperature
        humidity = dht_device.humidity


        if temperature is not None and humidity is not None:
            previous_temperature = temperature
            previous_humidity = humidity
            return temperature, humidity
        else:
           
            if previous_temperature is not None and previous_humidity is not None:
                return previous_temperature, previous_humidity
            else:
              
                return None, None

    except RuntimeError as e:
       
        print(f"Failed to read data: {e}")
        if previous_temperature is not None and previous_humidity is not None:
            return previous_temperature, previous_humidity
        else:
            
            return None, None

if __name__ == "__main__":
    
    while True:
        t, h = get_sensor_data()
        if t is not None and h is not None:
            print(f"Temperature: {t}°C  Humidity: {h}%")
        else:
            print("No data from sensor")
        time.sleep(2)