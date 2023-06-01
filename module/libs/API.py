import requests

def get_exchange_rate():
    url = 'https://cbu.uz/oz/arkhiv-kursov-valyut/json/'
    response = requests.get(url)
    res = response.json()   
    USD = float(res[0]['Rate'])

    return USD