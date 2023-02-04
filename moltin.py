import requests
import os
from pprint import pprint
from dotenv import load_dotenv
load_dotenv()


def fetch_headers():
	# data = {
	# 	'client_id': os.environ["CLIENT_ID"],
	# 	'grant_type': 'implicit',
	# }
	data = {
		'client_id': os.environ["CLIENT_ID"],
		'client_secret': os.environ["CLIENT_SECRET"],
		'grant_type': 'client_credentials',
	}
	response = requests.post('https://api.moltin.com/oauth/access_token', data=data)
	response.raise_for_status()
	access_token = response.json()['access_token']
	headers = {
		'Authorization': 'Bearer {}'.format(access_token),
	}
	return headers


def fetch_products():
    headers = fetch_headers()
    url = 'https://api.moltin.com/pcm/products'
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()['data']


def add_to_cart(pcs, prod_id, user_id, prod_name):
    headers = fetch_headers()
    data = {'data':
        {
            'name':prod_name,
            'id':prod_id,
            'type':'cart_item',
            'quantity':pcs,
        }
    }
    print(data)
    url = f'https://api.moltin.com/v2/carts'
    response = requests.post(url=url, headers=headers, json=data)
    print(response.json())

pcs = 1
products = fetch_products()
prod_id = fetch_products()[0]['id']
user_id = os.environ["CLIENT_ID"]
prod_name = fetch_products()[0]['attributes']['name']
add_to_cart(pcs, prod_id, user_id, prod_name)