import time
from datetime import datetime
from importlib import reload

import FechasRelativas as FR
import APIDefontana as PD
import APITrello as TT

registro_pedidos = {}

lista_pedidos_Cerrados = ["EFX (EN_DESPACHO_FACTURADO)", "EEX (EN_DESPACHO_EN_FACTURACION)", 
"DEX (DESPACHADO_EN_FACTURACION)", "DFX (DESPACHADO_FACTURADO)", "M (CERRADO_MANUAL)"]
lista_pedidos_Semilistos = ["EFX (EN_DESPACHO_FACTURADO)", "EEX (EN_DESPACHO_EN_FACTURACION)",
"DEX (DESPACHADO_EN_FACTURACION)"]

# Consultar pedidos en defontana
def obtenerPedidos():
    pedidosDefontana = PD.lista_pedidos()
    return pedidosDefontana

# Consultar tarjetas existentes en Trello
def obtenerTarjetas():
    tarjetasTrello = TT.lista_tarjetas_trello(TT.pedidos_idBoard)
    return tarjetasTrello

# Comparar si existe en Trello y crea tarjeta, o actualiza su estado
def cargar_trello(numero, pedidos, tarjetas):
    try:
        nombre, detalle, fechaC, fechaV, local = PD.detalle_pedido(numero)
    except:
        print(numero, "Vacío")
        return None
    else:
        if numero not in tarjetas and datetime.strptime(fechaC, "%Y-%m-%dT%H:%M:%S").date() > FR.hace1Semana and pedidos[numero] == "P (PENDIENTE)":
            post_in_trello(numero, nombre, detalle, fechaC, fechaV, local)
        elif numero in tarjetas:
            modifica_en_trello(numero, pedidos, tarjetas, fechaC)

def modifica_en_trello(numero, pedidos, tarjetas, fechaC):
    estado = pedidos[numero]
    if estado == "P (PENDIENTE)":
        pass
    elif datetime.strptime(fechaC, "%Y-%m-%dT%H:%M:%S").date() < FR.ayer and estado in lista_pedidos_Cerrados:
        elimina_Trello(numero, tarjetas)
    elif estado in lista_pedidos_Cerrados:
        estado = "false"
        TT.mod_trello(tarjetas[numero], estado, TT.listo_idList)
    else:
        print(numero, pedidos[numero])

def post_in_trello(numero, nombre, detalle, fechaC, fechaV, local):
    if "0-02 MAURICIO DANIEL BRAVO CORDERO" in nombre:
        etiqueta = TT.etiqueta_Sodexo
        lista = TT.sodexo_idList
    elif local == "MONS.":
        etiqueta = TT.etiqueta_Monsalve
        lista= TT.monsalve_idList
    elif local == "PLAYA":
        etiqueta = TT.etiqueta_Playa
        lista = TT.playa_idList
    else:
        etiqueta = False
        lista = TT.pendientes_idList
    tarjeta_ID = TT.post_trello(nombre, detalle, fechaC=fechaC, fechaV=fechaV, idLabels=etiqueta, idList=lista)
    b64 = PD.obtener_b64(numero)
    if b64:
        TT.adjunta_pedido_PDF(tarjeta_ID,b64,f"Pedido {numero}.pdf")

# Archiva tarjetas Trello
def elimina_Trello(numero, tarjetas):
    TT.mod_trello(tarjetas[numero], "true", TT.listo_idList)

# Archiva tarjetas Trello que no estén en el listado de pedidos pendientes
def elimina_Trello2(pedidos, tarjetas):
    for numero in tarjetas:
        if numero not in pedidos:
            elimina_Trello(numero, tarjetas)

# Función principal, que ejecuta las funciones necesarias para correr el código
def principal():
    pedidos = obtenerPedidos()
    global registro_pedidos
    if pedidos != registro_pedidos:
        tarjetas = obtenerTarjetas()
        for item in pedidos:
            if item not in registro_pedidos or pedidos[item] != registro_pedidos[item]:
                cargar_trello(item, pedidos, tarjetas)
        registro_pedidos = pedidos
        elimina_Trello2(pedidos, tarjetas)

# Bucle que mantiene el programa actualizándose   
while True:
    try:
        principal()
    except Exception as e:
        print(e)
    # time.sleep(300) # Tiempo de espera: 5 minutos
    # Siempre que esté corriendo en el servidor, no vale la pena tener el tiempo de espera
    FR = reload(FR)


# Test
principal()
# tarjetas = obtenerTarjetas()
# TT.post_trello("7584 - JOYCI ALARCON CANO", "", idList="638f8f9424f8370124782689")
# b64 = PD.obtener_b64("7584")
# TT.adjunta_pedido_PDF(tarjetas["7584"],b64,f"Pedido {7584}.pdf")