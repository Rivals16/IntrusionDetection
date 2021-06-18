from Information import *
import json
import time
import boltiot
import requests
import numpy as np
import math

bolt_id = "XXXXXXXXXXXXXXXXXXXx"
bolt_api = "XXXXXXXXXXXXXXXXXXXXXXXXX"

chat_id = XXXXXXXXX"
telegram_id_api = "XXXXXXXXXXXXXXXX"

def send_telegram_message(message):
    url = "https://api.telegram.org/" + telegram_id_api + "/sendMessage"
    print(url)

    response = requests.request(
        "POST",
        url=url,
        params={
            "chat_id": chat_id,
            "text": message
        }
    )

    return response


def min_max_intensity(array, k):
    c = 10 # Multiplication Factor
    variance_intensity = np.var(array)
    z = 20 * math.sqrt(variance_intensity/k)

    min_intensity = array[-1] - z
    max_intensity = array[-1] + z
    return [min_intensity, max_intensity]


if __name__ == "__main__":
    bolt_connect = boltiot.Bolt(bolt_api, bolt_id)

    current_intensity = bolt_connect.analogRead('A0')


    k_intensity = []
    k = 10
    while True:
        print('Collecting response from sensor..')
        response = bolt_connect.analogRead('A0')
        current_intensity = int(json.loads(response)['value'])
        if len(k_intensity) != 10:
            k_intensity.append(current_intensity)
        else:
            intensity_range = min_max_intensity(k_intensity,k)
            k_intensity.pop(0)
            k_intensity.append(current_intensity)
            print(current_intensity, *intensity_range)
            try:
                if current_intensity < intensity_range[0] or current_intensity > intensity_range[1]:
                    print("Intrusion Detected : ")
                    message = "Someone in The room"
                    send_telegram_message(message)
                    break

            except Exception as e:
                print("Error Occur below:")
                print(e)
        print()

        time.sleep(5)

