from machine import Pin
import time
import neopixel
import network, espnow

# Configuration IO
BTN_S1 = Pin(4, Pin.IN)
BTN_S2 = Pin(5, Pin.IN)
LED = Pin(6, Pin.OUT)
# Configuration pour la LED RGB
RGB_PIN = Pin(48, Pin.OUT)              # LED RGB (NeoPixel)
rgb = neopixel.NeoPixel(RGB_PIN, 1)     # 1 LED RGB

# Configuration pour la communication pour ESP-NOW 
sta = network.WLAN(network.STA_IF)
sta.active(True)
sta.disconnect() 

e = espnow.ESPNow()
e.active(True)

peer_bcast = b'\xff\xff\xff\xff\xff\xff'
e.add_peer(peer_bcast)

FILTER = b"CAH_TP4"
CMD_COLOR = b'CHANGE_COLOR'

# Variables d'état
last_S1 = 1 # Boutons en Pull-up (repos à 1)
last_S2 = 1
led_val = 0 # LED D1 sur le devkit
color_index = 0 # index de la couleur de la LED RGB
colors = [(1, 0, 0), (0, 1, 0), (0, 0, 1)] # tableau des couleurs RGB

is_remote_mode = False # Variable pour le mode de fonctionnement
#Varaible pour le clignotement
last_blink_time = 0
blink_state = False

# Gestion du Heartbeat et Timeout
last_send_time = 0
last_rx_time = 0
connection_timeout = 2000 # Retour au mode local après 2s sans signal

rgb[0] = (0, 0, 0)
rgb.write()

if __name__ == "__main__":
    try:
        while True:
            now = time.ticks_ms()
            # lecture des valeurs des boutons
            current_S1 = BTN_S1.value()
            current_S2 = BTN_S2.value()
    
            # Signal de présence
            if time.ticks_diff(now, last_send_time) > 1000:
                try:
                    e.send(peer_bcast, FILTER, False)
                except OSError:
                    pass
                last_send_time = now
    
            # Réception du message d'identification
            host, msg = e.recv(0)
            if msg == FILTER:
                last_rx_time = now 
                is_remote_mode = True
        
            # Action : Seulement si l'autre a appuyé sur S2
            if msg == CMD_COLOR:
                color_index = (color_index + 1) % len(colors)
        
            # détection de flanc S1
            if current_S1 == 0 and last_S1 != 0:
                led_val = not led_val
                LED.value(led_val)
    
            # fonctionnement en mode remote
            if is_remote_mode:
                # détection de flanc S2
                if current_S2 == 0 and last_S2 != 0:
                    try:
                        e.send(peer_bcast, CMD_COLOR, False)
                    except OSError:
                        pass
        
                # Clignotement à 2 Hz
                if time.ticks_diff(now, last_blink_time) > 250:
                    blink_state = not blink_state
                    if blink_state:
                        rgb[0] = colors[color_index]
                    else:
                        rgb[0] = (0, 0, 0)
                    rgb.write()
                    last_blink_time = now

                # Vérification du Timeout
                if time.ticks_diff(now, last_rx_time) > connection_timeout:
                    is_remote_mode = False
                    print("Mode Local : Partenaire perdu")
                    rgb[0] = colors[color_index]
                    rgb.write()

            # fonctionnement en mode local       
            else:
                if current_S2 == 0 and last_S2 != 0:
                    color_index = (color_index + 1) % len(colors)
                    rgb[0] = colors[color_index]
                    rgb.write()
    
            # SAUVEGARDE de l'état (doit être DANS la boucle while)
            last_S1 = current_S1    
            last_S2 = current_S2
            time.sleep_ms(1)

    except KeyboardInterrupt:
        print("Arrêt du script")
        rgb[0] = (0, 0, 0)
        rgb.write()
