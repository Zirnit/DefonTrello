import requests
from HeadersKeys import trelloQuery, trelloHeaders
from pprint import pprint

def obtener_boards():
    url = "https://api.trello.com/1/members/me/boards"
    params=trelloQuery
    headers = trelloHeaders
    response = requests.request("GET", url, headers=headers, params=params).json()
    board_ID = {}
    for i in response:
        board_ID[i["id"]] = i["name"]
    print("Board ID\t\t\tBoard name")
    for k, v in board_ID.items():
        print(k, "\t", v)

def obtener_listas(board_ID):
    url = f"https://api.trello.com/1/boards/{board_ID}/lists"
    params=trelloQuery
    headers = trelloHeaders
    response = requests.request("GET", url, headers=headers, params=params).json()
    list_ID = {}
    for i in response:
        list_ID[i["id"]]=i["name"]
    print("List ID\t\t\t\tList name")
    for k, v in list_ID.items():
        print(k, "\t", v)

def obtener_etiquetas(board_ID):
    url = f"https://api.trello.com/1/boards/{board_ID}/labels"
    querystring = trelloQuery
    headers = trelloHeaders
    response = requests.request("GET", url, headers=headers, params=querystring).json()
    label_ID = {}
    for i in response:
        label_ID[i["id"]]=i["name"]
    print("List ID\t\t\t\tList name")
    for k, v in label_ID.items():
        print(k, "\t", v)

def obtener_tarjetas(board_ID):
    url = f"https://api.trello.com/1/boards/{board_ID}/cards"
    querystring = trelloQuery
    headers = trelloHeaders
    response = requests.request("GET", url, headers=headers, params=querystring).json()
    card_ID = {}
    for i in response:
        card_ID[i["id"]]=i["name"]
    print("Card ID\t\t\t\tCard name")
    for k, v in card_ID.items():
        print(k, "\t", v)

# obtener_boards()
# obtener_listas("638f8f736c3c63011f219d78")
# obtener_etiquetas("6373dcefc0f5a70075826fea")
# obtener_tarjetas("638f8f736c3c63011f219d78")
