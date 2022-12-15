import requests
import HeadersKeys as HK

def obtenerCoordenadas(direccion, comuna):
    url = "http://api.positionstack.com/v1/forward"
    querystring = {
        "access_key" : HK.positionstack,
        "query" : direccion+", "+comuna,
        "country" : "CL"
    }
    response = requests.request("GET", url, params=querystring).json()
    try:
        location = str(response["data"][0]["latitude"])+","+str(response["data"][0]["longitude"])
        latitude = response["data"][0]["latitude"]
        longitude = response["data"][0]["longitude"]
    except:
        location = ""
        latitude = 0
        longitude = 0
    return location, latitude, longitude

#print(obtenerCoordenadas("poeta pedro prado 1689", "quinta normal"))
