import os, requests

BASE_URL = "http://127.0.0.1:8510/v2/"


def getDevices():

    allDevices = list()

    get_devices = requests.get(BASE_URL + "elements")

    devices = get_devices.json()['elements']

    for device in devices:
        device_name = requests.get(BASE_URL + "element/" + device)

        allDevices.append("Name: " + device_name.json()['name'] + "     ItemID: " +  device)

    return allDevices