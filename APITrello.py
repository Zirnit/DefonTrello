import requests
import HeadersKeys as HK
from base64 import b64decode

# Lista de tableros en Trello
pedidos_idBoard = "61ce1d50882ab9559d105e43"
compras_idBoard = "6373dcefc0f5a70075826fea"
ruta_idBoard = "633eff43035b6f00bd6ef083"
test_idBoard = "638f8f736c3c63011f219d78"

# Lista idList de Trello board "Pedidos"
pendientes_idList = "61ce1d50882ab9559d105e44" #Pendientes Santiago
playa_idList = "62f67cff9ba3ce0c4ffd4be2" # Pendientes playa
monsalve_idList = "62f67d119efeba8106426433" # Pendientes Monsalve
listo_idList = "61ce1d50882ab9559d105e46"
sodexo_idList = "63728d27fb591a00e0656147"

# Lista idList de Trello board "Ruta"
facturas_idList = "633eff57f7f87403c403b734" # Facturas generadas
chof1_idList = "633eff5fbfa3aa01e0bea7af" # Byron
chof2_idList = "633eff63eca5ab01ecb63c23" # Paulo
mons_idList = "633eff6610e0c402d71e23d9" # Monsalve
chof_otro_idList = "633eff69fdf9b70135d3504e" # Otros conductores
listo_idList = "633eff6d86d9c801cce0f63e" # Pedidos entregados

# Lista idList de Trello board "Compras"
ordenes_idList = "6373dd6176f3a50ca68a4a98" # Órdenes de compra
buscar_idList = "6373e63f22f54803ee382440" # Ir a buscar
tablero_ruta_idList = "638f8fe605c6ea0069fbe69b" # Para ruta
en_ruta_idList = "6373dd6bc5df92016c7705fe" # En ruta
recibidos_idList = "6373dd910ea7d20154813028" # Recibidos

# Etiquetas de Trello board "Pedidos"
etiqueta_Playa = "62eaecd5dfd104854cc9ff3d"
etiqueta_Monsalve = "62f691943b8e600bfc3bad29"
etiqueta_Sodexo = "63728b8b472fe7012578ce78"

# Etiquetas de Trello board "Ruta"
etiqueta_Monsalve = "6340611b61a1b1037f317ff4"
etiqueta_chof1 = "6340612e7185cb002419d7a2"
etiqueta_chof2 = "634061382a7d6f02e84bd353"
etiqueta_chof_otros = "63406141a4859a0397ffea4b"
etiqueta_Playa = "63407b296d9b0901ab0596a9"
etiqueta_Santiago = "6345b9aaa55a4402dd5dde39"
etiqueta_por_preparar = "6390a06d0eaba4049b16e0e0"

# Etiquetas de Trello board "Compras"
etiqueta_Buscar = "63908b900b85c702061ab85f"

# Create Trello card
def post_trello(nombre, detalle, fechaC=False, fechaV=False, coordenada=False, idLabels=False, idList=False):
    trelloCard = "https://api.trello.com/1/cards" # Dirección API
    TrelloQS = {
    "key":HK.tKey,
    "token":HK.tToken,
    "idList":idList, # Lista del pedido en Trello
    "name":nombre, # Nombre de la tarjeta
    "desc":detalle, # Descripción de la tarjeta
    "pos":"top", # Posición en la cual se crea la tarjeta (top, bottom, or a positive float)
    "start": fechaC, # Fecha de creación de la tarjeta
    "due": fechaV, # Fecha de "caducidad" de la tarjeta
    "coordinates":coordenada,
    "idLabels": idLabels} # Etiqueta de la tarjeta
    if not fechaC:
        del TrelloQS["start"]
    if not fechaV:
        del TrelloQS["due"]
    if not coordenada:
        del TrelloQS["coordinates"]
    if not idLabels:
        del TrelloQS["idLabels"]
    response = requests.request("POST", trelloCard, headers=HK.trelloHeaders, params=TrelloQS)
    return response.json()["id"]

# Para obtener las ID de las tarjetas de Trello
def lista_tarjetas_trello(board_ID):
    tarjetasTrelloURL = f"https://api.trello.com/1/boards/{board_ID}/cards" # filter Valid Values: all, closed, none, open, visible.
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
def mod_trello(cardID, closed="false", idList=False, idLabel=False):
    trelloCard = f"https://api.trello.com/1/cards/{cardID}" # Dirección API
    querystring = {"key":HK.tKey,
    "token":HK.tToken,
    "closed": closed,
    "idList": idList,
    "idLabels": idLabel
    }
    if not idList:
        del querystring["idList"]
    if not idLabel:
        del querystring["idLabels"]
    requests.put(trelloCard, headers=HK.trelloHeaders, params=querystring)

def adjunta_pedido_PDF(card_ID,file_data,file_name):
    querystring = {
    "key":HK.tKey,
    "token":HK.tToken   
    }
    PDF_data = b64decode(file_data)
    requests.post(f"https://trello.com/1/cards/{card_ID}/attachments", params=querystring, files={'file': (file_name, PDF_data, "application/pdf")})