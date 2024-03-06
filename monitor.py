import requests
import time

#questo script serve per definire la topologia della rete ricevendo dal controller queste informazioni 


# Definizione degli endpoint dell'API REST
BASE_URL = 'http://127.0.0.1:6633/v1.0/topology'
SWITCHES_ENDPOINT = '/switches'
LINKS_ENDPOINT = '/links'
HOSTS_ENDPOINT = '/hosts'

# Funzione per ottenere informazioni su tutti gli switch nella topologia
def get_switches():
    response = requests.get(BASE_URL + SWITCHES_ENDPOINT)
    if response.status_code == 200:
        return response.json()
    else:
        return None

# Funzione per ottenere informazioni su tutti i collegamenti nella topologia
def get_links():
    response = requests.get(BASE_URL + LINKS_ENDPOINT)
    if response.status_code == 200:
        return response.json()
    else:
        return None

# Funzione per ottenere informazioni su tutti gli host nella topologia
def get_hosts():
    response = requests.get(BASE_URL + HOSTS_ENDPOINT)
    if response.status_code == 200:
        return response.json()
    else:   
        return None

# Esempio di utilizzo delle funzioni per ottenere le informazioni sulla topologia
if __name__ == "__main__":
    print("START MONITORING!")
    switches = get_switches()
    if switches:
        print("Switches:")
        for switch in switches:
            print(switch)
    
    links = get_links()
    if links:
        print("\nLinks:")
        for link in links:
            print(link)
    
    hosts = get_hosts()
    if hosts:
        print("\nHosts:")
        for host in hosts:
            print(host)
    
    while True:
        print("sto continuando a processare")
        time.sleep(10)

