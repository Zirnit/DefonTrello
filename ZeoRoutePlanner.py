import requests
import HeadersKeys as HK

def ingresa_punto(direccion, comuna, latitude, longitude, glosa, fecha, nombreCliente):
    address = direccion + ", " + comuna
    stop = {
        "address": address,
        "latitude": latitude,
        "longitude": longitude,
        "notes": glosa,
        "optimize_status": "normal",
        "stop_duration": 10,
        "stop_date": fecha,
        "parcel_count": 1,
        "arrive_start": "now",
        "arrive_end": "anytime",
        "earliest": 0,
        "latest": 0,
        "driver_id": "",
        "stop_type": "delivery",
        "customer_name": nombreCliente,
        "customer_mobile_number": "",
        "customer_email": ""
    }
    url="https://zeorouteplanner.com/api/v5/route_stop"
    querystring = {
    "api_key":HK.zoeRP,
    "stops":[stop]
    }
    requests.request("POST", url, json=querystring).json()

#print(ingresa_punto())