import requests
import HeadersKeys as HK
from base64 import b64decode

# Lista de tableros en Trello
pedidos_idBoard = "61ce1d50882ab9559d105e43"
compras_idBoard = "6373dcefc0f5a70075826fea"
ruta_idBoard = "633eff43035b6f00bd6ef083"
test_idBoard = "638f8f736c3c63011f219d78"

# Lista idList de Trello board "Pedidos"
pendientes_idList_pedidos = "61ce1d50882ab9559d105e44" #Pendientes Santiago
playa_idList_pedidos = "62f67cff9ba3ce0c4ffd4be2" # Pendientes playa
monsalve_idList_pedidos = "62f67d119efeba8106426433" # Pendientes Monsalve
listo_idList_pedidos = "61ce1d50882ab9559d105e46"
sodexo_idList_pedidos = "63728d27fb591a00e0656147"

# Lista idList de Trello board "Ruta"
facturas_idList_ruta = "633eff57f7f87403c403b734" # Facturas generadas
chof1_idList_ruta = "633eff5fbfa3aa01e0bea7af" # Byron
chof2_idList_ruta = "633eff63eca5ab01ecb63c23" # Paulo
mons_idList_ruta = "633eff6610e0c402d71e23d9" # Monsalve
chof_otro_idList_ruta = "633eff69fdf9b70135d3504e" # Otros conductores
listo_idList_ruta = "633eff6d86d9c801cce0f63e" # Pedidos entregados

# Lista idList de Trello board "Compras"
ordenes_idList_compras = "6373dd6176f3a50ca68a4a98" # Órdenes de compra
buscar_idList_compras = "6373e63f22f54803ee382440" # Ir a buscar
tablero_ruta_idList_compras = "638f8fe605c6ea0069fbe69b" # Para ruta
en_ruta_idList_compras = "6373dd6bc5df92016c7705fe" # En ruta
recibidos_idList_compras = "6373dd910ea7d20154813028" # Recibidos

# Lista idList de Trello board "Test"
pendiente_idList_test = "638f8f9424f8370124782689"
ruta1_idList_test = "638f8fee6e9ebb04826fff44"
ruta2_idList_test = "63909323d66522001593bfb7"
ruta3_idList_test = "6390932c383e3d0108870515"
byron_idList_test = "6390a15b03b57900362c97e4"
paulo_idList_test = "6390a15d5160fb0067ce8982"
listo_idList_test = "638f8ff2e395e50388c8ecca"
en_ruta_idList_test = "639348135e7e0d03d120e0c2"

# Etiquetas de Trello board "Pedidos"
etiqueta_Playa_pedidos = "62eaecd5dfd104854cc9ff3d"
etiqueta_Monsalve_pedidos = "62f691943b8e600bfc3bad29"
etiqueta_Sodexo_pedidos = "63728b8b472fe7012578ce78"

# Etiquetas de Trello board "Ruta"
Santiago_idLabel_ruta = "6345b9aaa55a4402dd5dde39"
Byron_idLabel_ruta = "6340612e7185cb002419d7a2"
Monsalve_idLabel_ruta = "6340611b61a1b1037f317ff4"
Paulo_idLabel_ruta = "634061382a7d6f02e84bd353"
Entregado_idLabel_ruta = "634ecaecf7bcc400fd6ae4fa"
Playa_idLabel_ruta = "63407b296d9b0901ab0596a9"
Willy_idLabel_ruta = "6352ef9c2023b00269c28b6e"
RAPID_idLabel_ruta = "63652707f9ded5025f6e9b9d"
INV_CALAMA_idLabel_ruta = "638f561bae0c440225e6298b"
TOP_FRIO_idLabel_ruta = "6357fc2b1ad93603e8e4fe49"
Ir_a_buscar_idLabel_ruta = "63934b2c4e445305242ccd3d"
KEYLOGISTICS_idLabel_ruta = "6357fd61fcb80401e6522212"
CACEM_idLabel_ruta = "637ba54a5e4fbe00b435f0d6"
Otro_idLabel_ruta = "63406141a4859a0397ffea4b"
Sodexo_idLabel_ruta = "63a1be69f60b7a011572d0e2"

# Etiquetas de Trello board "Compras"
etiqueta_Buscar_compras = "63908b900b85c702061ab85f"

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

def adjunta_PDF(card_ID,file_data,file_name):
    querystring = {
    "key":HK.tKey,
    "token":HK.tToken   
    }
    PDF_data = b64decode(file_data)
    requests.post(f"https://trello.com/1/cards/{card_ID}/attachments", params=querystring, files={'file': (file_name, PDF_data, "application/pdf")})
