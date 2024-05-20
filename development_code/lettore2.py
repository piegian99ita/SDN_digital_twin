import os
import time

def start_capture(filename):
    os.system(f"tcpdump -i any not host 127.0.0.1 and not port 22 and not ether proto 0x88cc and not icmp6 -w {filename} &")

def stop_capture():
    os.system("pkill tcpdump")


  

if __name__ == "__main__":
  interval = 10  # Intervallo in secondi per la creazione di nuovi file pcap
  file_count = 1

  try:
    while True:
      filename = f"2capture_{file_count}.pcap"
      start_capture(filename)
      time.sleep(interval)
      stop_capture()
      file_count += 1
  except KeyboardInterrupt:
    stop_capture()
