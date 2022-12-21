import APIDefontana as CD
import APITrello as TT
import FechasRelativas as FR
import positionstack as PS
import time
from datetime import datetime
from importlib import reload

registro_compras = {}

# Consultar Compras en defontana
def obtenerCompras():
    ComprasDefontana = CD.lista_Compras()
    return ComprasDefontana

# Consultar tarjetas existentes en Trello
def obtenerTarjetas():
    tarjetasTrello = TT.lista_tarjetas_trello(TT.compras_idBoard)
    return tarjetasTrello

# Comparar si existe en Trello y crea tarjeta, o actualiza su estado
def cargar_trello(numero, Compras, tarjetas):
    try:
        nombre, detalle, fechaEmision, fechaRecepcion, comuna, despacho = CD.detalle_Compra(numero)
    except:
        print(numero, Compras[numero], "Vacío")
        return None
    else:
        if numero not in tarjetas and datetime.strptime(fechaEmision, "%Y-%m-%dT%H:%M:%S").date() > FR.hace2Semanas:
            post_in_trello(nombre, detalle, fechaEmision, fechaRecepcion, comuna, despacho)
        elif numero in tarjetas:
            modificar_en_trello(numero, Compras, tarjetas, fechaEmision, fechaRecepcion)

def post_in_trello(nombre, detalle, fechaEmision, fechaRecepcion, comuna, despacho):
    if despacho == "Calle Poeta Pedro Prado 1689 oficina 06":
        etiqueta = ""
        lista = TT.ordenes_idList_compras
        coordenada = ""
    else:
        etiqueta = TT.IraBuscar_idLabel_compras
        lista = TT.buscar_idList_compras
        detalle += f"\nIr a buscar a {despacho}"
        coordenada, latitude, longitude= PS.obtenerCoordenadas(despacho, comuna)
    TT.post_trello(nombre, detalle, fechaC=fechaEmision, fechaV=fechaRecepcion, coordenada=coordenada, idLabels=etiqueta, idList=lista)

def modificar_en_trello(numero, Compras, tarjetas, fechaEmision, fechaRecepcion):
    estado = Compras[numero]
    if estado == "Aprobado" and fechaRecepcion == FR.hoy:
        TT.mod_trello(tarjetas[numero], "false", TT.en_ruta_idList_compras)
    elif estado == "Anulado":
        TT.mod_trello(tarjetas[numero], idLabel=TT.Anulado_idLabel_compras, idList=TT.recibidos_idList_compras)
    elif datetime.strptime(fechaEmision, "%Y-%m-%dT%H:%M:%S").date() < FR.hace2Semanas and estado == "Cerrado":
        elimina_Trello(numero, tarjetas)
    elif estado == "Cerrado":
        TT.mod_trello(tarjetas[numero], "false", TT.recibidos_idList_compras)
    else:
        print(numero, Compras[numero])

# Archiva tarjetas Trello
def elimina_Trello(numero, tarjetas):
    TT.mod_trello(tarjetas[numero], "true", TT.recibidos_idList_compras)

# Archiva tarjetas Trello que no estén en el listado de Compras pendientes
def elimina_Trello2(Compras, tarjetas):
    for numero in tarjetas:
        if numero not in Compras:
            elimina_Trello(numero, tarjetas)

# Función principal, que ejecuta las funciones necesarias para correr el código

def principal():
    Compras = obtenerCompras()
    global registro_compras
    if Compras != registro_compras:
        tarjetas = obtenerTarjetas()
        for item in Compras:
            if item not in registro_compras or Compras[item] != registro_compras[item]:
                cargar_trello(item, Compras, tarjetas)
        registro_compras = Compras
    # elimina_Trello2(Compras, tarjetas)

# Bucle que mantiene el programa actualizándose   
# while True:
#     try:
#         principal()
#     except Exception as e:
#         print("Error en bucle principal Compras ",e)
#     # time.sleep(300) # Tiempo de espera: 5 minutos
#     # Siempre que esté corriendo en el servidor, no vale la pena tener el tiempo de espera
#     FR = reload(FR)

principal() #Test