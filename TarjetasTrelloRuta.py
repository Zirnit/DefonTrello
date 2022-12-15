import requests
import HeadersKeys as HK

# Lista idList de Trello board "Facturas"
facturas_idList = "633eff57f7f87403c403b734" # Facturas generadas
chof1_idList = "633eff5fbfa3aa01e0bea7af" # Byron
chof2_idList = "633eff63eca5ab01ecb63c23" # Paulo
mons_idList = "633eff6610e0c402d71e23d9" # Monsalve
chof_otro_idList = "633eff69fdf9b70135d3504e" # Otros conductores
listo_idList = "633eff6d86d9c801cce0f63e" # Pedidos entregados

# Etiquetas de Trello board "Facturas"
etiqueta_Monsalve = "6340611b61a1b1037f317ff4"
etiqueta_chof1 = "6340612e7185cb002419d7a2"
etiqueta_chof2 = "634061382a7d6f02e84bd353"
etiqueta_chof_otros = "63406141a4859a0397ffea4b"
etiqueta_Playa = "63407b296d9b0901ab0596a9"
etiqueta_Santiago = "6345b9aaa55a4402dd5dde39"

# Create Trello card
def post_trello(nombre, detalle, fecha, direccion, comuna, coordenada="", idLabels="", idList=facturas_idList):
    trelloCard = "https://api.trello.com/1/cards" # Dirección API
    TrelloQS = {
    "key":HK.Tkey,
    "token":HK.Ttoken,
    "idList":idList,    # Lista de factura en Trello
    "name":nombre,      # Nombre de la tarjeta
    "desc":detalle,     # Descripción de la tarjeta
    "pos":"top",        # Posición en la cual se crea la tarjeta (top, bottom, or a positive float)
    "start": fecha,     # Fecha de "comienzo" de la tarjeta  
    #"due": fecha,       # Fecha de "caducidad" de la tarjeta
    #"address": direccion,
    #"locationName": comuna,
    "coordinates":coordenada,
    "idLabels":idLabels} 
    requests.request("POST", trelloCard, headers=HK.trelloHeaders, params=TrelloQS)

# Para obtener las ID de las tarjetas de Trello
def lista_tarjetas_trello():
    tarjetasTrelloURL = "https://api.trello.com/1/boards/633eff43035b6f00bd6ef083/cards" # filter Valid Values: all, closed, none, open, visible.
    IDtarjetasTrello = {}
    requestTarjetasTrello = requests.request(
    "GET",
    tarjetasTrelloURL,
    headers=HK.trelloHeaders,
    params=HK.trelloQuery
    ).json()
    for i in requestTarjetasTrello:
        espacio = i["name"].index(" ")
        IDtarjetasTrello[i["name"][:espacio]] = i["id"]
    return IDtarjetasTrello

# Modificar tarjeta Trello
def mod_trello(cardID, closed, idList=facturas_idList, idLabel="False"):
    trelloCard = f"https://api.trello.com/1/cards/{cardID}" # Dirección API
    querystring = {
    "key":HK.Tkey,
    "token":HK.Ttoken,
    "closed": closed,
    "idList": idList,
    "idLabels": idLabel}
    requests.put(trelloCard, headers=HK.trelloHeaders, params=querystring)
