import APIDefontana as FD
import APITrello as TT
import FechasRelativas as FR
import positionstack as PS
import ZeoRoutePlanner as ZRP
import time
from datetime import datetime
from importlib import reload

registro_facturas = {}
registro_tarjetas = {}

# Consultar Facturas en defontana
def obtenerFacturas():
    FacturasDefontana = FD.lista_facturas()
    return FacturasDefontana

# Consultar tarjetas existentes en Trello
def obtenerTarjetas():
    tarjetasTrello = TT.lista_tarjetas_trello(TT.ruta_idBoard)
    return tarjetasTrello

# Comparar si existe en Trello y crea tarjeta, o actualiza su estado
def cargar_trello(numero, Facturas, tarjetas):
    try:
        nombre, detalle, fecha, direccionCliente, comuna, local, tipo_documento = FD.detalle_Factura(numero, Facturas[numero])
    except:
        print(numero, Facturas[numero], "Vacío")
        return None
    else:
        if numero not in tarjetas and datetime.strptime(fecha, "%Y-%m-%dT%H:%M:%S").date() > FR.hace4dias:
            post_in_trello(numero, nombre, detalle, fecha, direccionCliente, comuna, local, tipo_documento)
        # Ya que Trello puede archivar automáticamente tarjetas, prefiero no usar esta funcion.
        # elif numero in tarjetas:
        #     modifica_en_trello(numero, tarjetas, fecha)

def modifica_en_trello(numero, tarjetas, fecha):
    if datetime.strptime(fecha, "%Y-%m-%dT%H:%M:%S").date() < FR.hace1Semana:
        elimina_Trello(numero, tarjetas)

def post_in_trello(numero, nombre, detalle, fecha, direccionCliente, comuna, local, tipo_documento):
    if "0-02 MAURICIO DANIEL BRAVO CORDERO" in nombre:
        etiquetas = [TT.Sodexo_idLabel_ruta, TT.Santiago_idLabel_ruta]
        lista = TT.facturas_idList_ruta
        coordenada, latitude, longitude = PS.obtenerCoordenadas(direccionCliente, comuna)
    elif local == "MONS.":
        etiquetas = [TT.Monsalve_idLabel_ruta]
        lista = TT.mons_idList_ruta
        coordenada = ""
    elif local == "PLAYA":
        etiquetas = [TT.Playa_idLabel_ruta]
        lista = TT.facturas_idList_ruta
        coordenada, latitude, longitude = PS.obtenerCoordenadas(direccionCliente, comuna)
                # ZRP.ingresa_punto(direccionCliente, comuna, latitude, longitude, detalle,fecha,nombre), "\n", detalle, fecha, nombre
    elif local == "Local":
        etiquetas = [TT.Santiago_idLabel_ruta]
        lista = TT.facturas_idList_ruta
        coordenada, latitude, longitude = PS.obtenerCoordenadas(direccionCliente, comuna)
                # ZRP.ingresa_punto(direccionCliente, comuna, latitude, longitude, detalle,fecha,nombre), "\n", detalle, fecha, nombre
    else:
        etiquetas = ""
        lista = TT.facturas_idList_ruta
        coordenada = ""
    factura_ID = TT.post_trello(nombre, detalle, fechaC=fecha, coordenada=coordenada, idLabels=etiquetas, idList=lista)
    b64 = FD.obtener_factura_b64(numero, tipo_documento)
    if b64:
        TT.adjunta_PDF(factura_ID,b64,f"Factura {numero}.pdf")

# Archiva tarjetas Trello
def elimina_Trello(numero, tarjetas):
    TT.mod_trello(tarjetas[numero], "true", TT.listo_idList_ruta)

# Archiva tarjetas Trello que no estén en el listado de Facturas pendientes
def elimina_Trello2(Facturas, tarjetas):
    for numero in tarjetas:
        if numero not in Facturas:
            elimina_Trello(numero, tarjetas)

# Función principal, que ejecuta las funciones necesarias para correr el código
def principal():
    Facturas = obtenerFacturas()
    tarjetas = obtenerTarjetas()
    global registro_facturas
    global registro_tarjetas
    if Facturas != registro_facturas:
        for item in Facturas:
            if item not in registro_facturas or Facturas[item] != registro_facturas[item]:
                cargar_trello(item, Facturas, tarjetas)
        registro_facturas = Facturas
    if tarjetas != registro_tarjetas:
        for item in registro_tarjetas:
            if item in Facturas and item not in tarjetas:
                cargar_trello(item, Facturas, tarjetas)
        registro_tarjetas = tarjetas
    # elimina_Trello2(Facturas, tarjetas)

# Bucle que mantiene el programa actualizándose   
while True:
    try:
        principal()
    except Exception as e:
        print("Error en bucle principal Ruta ",e)
    # time.sleep(300) # Tiempo de espera: 5 minutos
    # Siempre que esté corriendo en el servidor, no vale la pena tener el tiempo de espera
    FR = reload(FR)

principal() #Test