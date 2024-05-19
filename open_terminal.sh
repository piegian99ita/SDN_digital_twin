#!/bin/bash

# Apri tre finestre di terminale
xterm -fa 'Monospace' -fs 12 -fg white -bg black -e " sudo python3 network.py" &  
xterm -fa 'Monospace' -fs 12 -fg white -bg black -e " sleep 4; ryu-manager --observe-links controller.py" &
xterm -fa 'Monospace' -fs 12 -fg white -bg black -e " sleep 10; python3 traffic_generator.py; sleep 10 " & 
