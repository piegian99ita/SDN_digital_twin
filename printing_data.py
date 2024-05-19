from scapy.all import *
from time import sleep

def print_ip_addresses(pcap_file):
    # Lista per memorizzare gli indirizzi IP univoci
    

    # Carica il file pcap
    packets = rdpcap(pcap_file)

    # Analizza ogni pacchetto nel file pcap
    for packet in packets:
        # Verifica se il pacchetto ha un layer IP
         if IP in packet and packet.haslayer(IP):
            print("Indirizzi IP degli host nel file pcap:")
            print(packet[IP].src)
            print(packet[IP].dst)
            # Aggiungi l'indirizzo IP di origine e di destinazione alla lista
            
            
            

    # Stampa gli indirizzi IP univoci
    
    




if __name__ == "__main__":
  # File pcap da analizzare
    pcap_file = "h1_final.pcap"
    # Carica il file pcap
    
    packets = rdpcap(pcap_file)
    # Chiama la funzione per stampare gli indirizzi IP
    #print_ip_addresses(pcap_file)
    print("SUMMARY:")
    i=0
    for packs in packets:
        print(i)
        i+=1
        print(packs.summary())
    