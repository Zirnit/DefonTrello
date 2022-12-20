import requests
import FechasRelativas as FR
import HeadersKeys as HK

Base_URL = "https://api.defontana.com/api/"
# Pedidos
# Para obtener la lista de pedidos y su status en un dict
def lista_pedidos():
    lista_pedidos_URL = "Order/List"
    URL = Base_URL+lista_pedidos_URL
    querystring = {"FromDate":FR.hace2Semanas,"ToDate":FR.en1Semana,"ItemsPerPage":"1000","PageNumber":"0","fromNumber":"4400"}
    listaPedidosJson = requests.request("GET", URL, headers=HK.headersDefontana, params=querystring).json()
    listaStatusPedidosDefon = {}
    for i in listaPedidosJson["items"]:
        listaStatusPedidosDefon[str(i["number"])] = i["status"]
    return listaStatusPedidosDefon

# Para obtener del pedido solicitado: ("número de pedido - nombre", "detalle (código, cantidad, descripción)", "fecha de vencimiento")
def detalle_pedido(numero):
    detalle_pedido_URL = "Order/Get"
    URL = Base_URL+detalle_pedido_URL
    querystring = {"number":numero}
    pedidoJson = requests.request("GET", URL, headers=HK.headersDefontana, params=querystring)
    try:
        nombreCliente = pedidoJson.json()["orderData"]["client"]["name"]
    except:
        return None
    else:
        fechaCrea = pedidoJson.json()["orderData"]["creationDate"][:10]+"T11:00:00"
        fechaVenc = pedidoJson.json()["orderData"]["expirationDate"][:10]+"T11:00:00"
        localPedido = pedidoJson.json()["orderData"]["shopID"]
        comentario = pedidoJson.json()["orderData"]["comment"]
        comentario_factura = pedidoJson.json()["orderData"]["billingComment"]
        comentario_despacho = pedidoJson.json()["orderData"]["dispatchComment"]
        detallePedido = ""
        if comentario:
            detallePedido += "\nComentario: "+comentario
        if comentario_factura:
            detallePedido += "\nComentario factura: "+comentario_factura
        if comentario_despacho:
            detallePedido += "\nComentario despacho: "+comentario_despacho
        nombrePedidoTrello = str(numero)+" - "+nombreCliente
        return nombrePedidoTrello, detallePedido, fechaCrea, fechaVenc, localPedido

# Regresa un base64 del pedido
def obtener_pedido_b64(numero):
    obtener_b64_URL = "Order/GetOrderStandardPDFDocumentBase64"
    URL = Base_URL+obtener_b64_URL
    querystring = {"folio" : numero}
    # Trata de extraer el documento 5 intentos antes de retornar False
    for _ in range(5):
        try:
            response = requests.request("GET", URL, headers=HK.headersDefontana, params=querystring).json()
            return response["document"]
        except Exception as e:
            print(e)
    return False


# Ruta
Vendedores = {
			"101": "MAURICIO BRAVO 9 8294 6356",
			"102": "CRISTOBAL BRAVO 9 8258 7699",
			"103": "MATIAS BRAVO 9 8258 3218",
			"104": "GABRIELA 9 3377 0533",
			"105": "RAQUEL 9 4233 7926",
			"106": "FRANCISCO",
			"124869064": "RAQUEL GÓMEZ",
			"201": "C.N.OB.",
			"202": "RICARDO VARGAS",
			"301": "Moroso",
			"VENDEDOR": "VENDEDOR"
}

def lista_facturas():
    lista_facturas_URL = "Sale/GetSalebyDate"
    URL = Base_URL+lista_facturas_URL
    querystring1 = {"initialDate":FR.hace1Semana,"endingDate":FR.hoy,"itemsPerPage":"1000","pageNumber":"0", "documentType": "FVAELECT"}
    querystring2 = {"initialDate":FR.hace1Semana,"endingDate":FR.hoy,"itemsPerPage":"1000","pageNumber":"0", "documentType": "FVARSELECT"}
    listaFacturasJson = requests.request("GET", URL, headers=HK.headersDefontana, params=querystring1).json()
    listaFacturasJson2 = requests.request("GET", URL, headers=HK.headersDefontana, params=querystring2).json()
    listaFacturasDefon = {}
    for i in listaFacturasJson["saleList"]:
        listaFacturasDefon[str(i["firstFolio"])] = i["documentType"]
    for i in listaFacturasJson2["saleList"]:
        listaFacturasDefon[str(i["firstFolio"])] = i["documentType"]
    return listaFacturasDefon

# Para obtener de la Factura solicitada: ("número de Factura - nombre", "detalle (código, cantidad, descripción)", "fecha de vencimiento")
def detalle_Factura(numero, docType):
    detalle_factura_URL = "Sale/GetSale"
    URL = Base_URL+detalle_factura_URL
    querystring = {"number": numero, "documentType" : docType}
    FacturasJson = requests.request("GET", URL, headers=HK.headersDefontana, params=querystring).json()[0]
    tipoDocumento = FacturasJson["documentType"]
    fechaEmision = FacturasJson["dateTime"][:10]+"T11:00:00"
    codigoCliente = FacturasJson["clientFile"]
    direccionCliente = FacturasJson["contactIndex"]
    vendedorID = FacturasJson["sellerFileId"]
    nombreVendedor = Vendedores[vendedorID]
    comuna = FacturasJson["district"]+", "+FacturasJson["city"]
    glosa = FacturasJson["gloss"]
    local = FacturasJson["shopId"]
    nombreCliente = consulta_Cliente(codigoCliente)
    nombre = f"{numero} - {nombreCliente}"
    try:
        numeroPedido = FacturasJson["attachedDocuments"][0]["attachedDocumentNumber"]
    except:
        numeroPedido = "Sin pedido asociado"
    detalle = f"Dirección: {direccionCliente}, {comuna}\nComentario: {glosa}\nReferencia pedido: {numeroPedido}\nVendedor: {nombreVendedor}"
    return nombre, detalle, fechaEmision, direccionCliente, comuna, local, tipoDocumento

def consulta_Cliente(id):
    consulta_Cliente_URL = "Sale/GetClientsByFileID"
    URL = Base_URL+consulta_Cliente_URL
    params = {"status": "0", "itemsPerPage" : "1", "pageNumber" : "0", "fileID": id}
    ClienteJson = requests.request("GET", URL, headers=HK.headersDefontana, params=params).json()
    try:
        Cliente = ClienteJson["clientList"][0]["name"]
    except:
        Cliente = "Sin información"
    return Cliente

def obtener_factura_b64(folio, documentType):
    obtener_b64_URL = "Sale/GetNewPDFDocumentBase64"
    URL = Base_URL+obtener_b64_URL
    querystring = {
        "folio" : folio,
        "documentType": documentType,
        "isCedible" : "false"
        }
    # Trata de extraer el documento 5 intentos antes de retornar False
    for _ in range(5):
        try:
            response = requests.request("GET", URL, headers=HK.headersDefontana, params=querystring).json()
            return response["document"]
        except Exception as e:
            pass
    print("error folio ", folio, e)
    return False

# Compras
def lista_Compras():
    lista_Compras_URL = "PurchaseOrder/List"
    URL = Base_URL+lista_Compras_URL
    querystring1 = {"FromDate":FR.hace1mes,"ToDate":FR.hoy,"ItemsPerPage":"100","Page":"0"}
    listaComprasJson2 = requests.request("GET", URL, headers=HK.headersDefontana, params=querystring1).json()
    querystring2 = {"FromDate":FR.hace1mes,"ToDate":FR.hoy,"ItemsPerPage":"100","Page":"1"}
    listaComprasJson = requests.request("GET", URL, headers=HK.headersDefontana, params=querystring2).json()
    listaComprasDefon = {}
    for i in listaComprasJson["data"]:
        listaComprasDefon[str(i["number"])] = i["status"]
    for i in listaComprasJson2["data"]:
        listaComprasDefon[str(i["number"])] = i["status"]
    return listaComprasDefon

# Para obtener de la Compra solicitada: ("número de Compra - nombre", "detalle (código, cantidad, descripción)", "fecha de vencimiento")
def detalle_Compra(numero):
    detalle_Compra_URL = "PurchaseOrder/Get"
    URL = Base_URL+detalle_Compra_URL
    querystring = {"number": numero}
    request = requests.request("GET", URL, headers=HK.headersDefontana, params=querystring)
    ComprasJson = request.json()["purchaseOrderData"]
    fechaEmision = ComprasJson["emissionDate"][:10]+"T11:00:00"
    fechaRecepcion = ComprasJson["receiptDate"][:10]+"T11:00:00"
    proveedor = ComprasJson["providerInfo"]["name"]
    direccionProveedor = ComprasJson["providerInfo"]["address"]
    comuna = ComprasJson["dispatchDistrict"]
    despacho = ComprasJson["dispatchAddress"]
    glosa = ComprasJson["comment"]
    nombre = f"{numero} - {proveedor}"
    detalle = ["Productos:\n"]
    for i in ComprasJson["purchaseOrderDetail"]:
        detalle.append(i["productId"])
        detalle.append("\t")
        detalle.append(str(i["quantity"]))
        detalle.append("\t")
        detalle.append(i["product"]["description"])
        if i["comment"]:
            detalle.append("\nComentario: ")
            detalle.append(i["comment"])
        detalle.append("\n")
    detalle.append(glosa)
    detalle.append(f"\nDirección proveedor: {direccionProveedor}")
    detalle = "".join(detalle)
    return nombre, detalle, fechaEmision, fechaRecepcion, comuna, despacho
# detalle_Compra(115)