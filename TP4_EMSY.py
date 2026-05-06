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

peer_bcast = b'\xff' * 6
e.add_peer(peer_bcast)

# Variables d'état
last_S1 = 1 # Boutons en Pull-up (repos à 1)
last_S2 = 1
led_val = 0 # LED D1 sur le devkit
color_index = 0 # index de la coueur de la LED RGB
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

while True:
    now = time.ticks_ms()
    # lecture des valeurs des boutons
    current_S1 = BTN_S1.value()
    current_S2 = BTN_S2.value()
    
    # Signal de présence
    # Envoi automatique toutes les secondes pour détecter un autre esp
    if time.ticks_diff(now, last_send_time) > 1000:
        try:
            # False = n'attend pas une réponse si aucun esp répond
            e.send(peer_bcast, b"CAH_TP4", False)
        except OSError:
            pass
        last_send_time = now
    
    # Réception du message d'identification
    host, msg = e.recv(0)
    if msg == b"CAH_TP4":
        last_rx_time = now 
        is_remote_mode = True
        
        # Action : Seulement si l'autre a appuyé sur S2
        if msg == b'CHANGE_COLOR':
            color_index = (color_index + 1) % len(colors)
    
    # fonctionnement en mode remote
    if is_remote_mode:
        # détection de flanc
        if current_S2 == 0 and last_S2 == 1:
            try:
                # envoi de l'ordre de changer la LED RGB de l'autre ESP
                e.send(peer_bcast, b'CHANGE_COLOR', False)
            # empeche de bloquer le code    
            except OSError:
                pass
        # détection de flanc    
        if current_S1 == 0 and last_S1 == 1:
            led_val ^= 1
            LED.value(led_val)
        # Clignotement à 2 Hz
        if time.ticks_diff(now, last_blink_time) > 250:
            blink_state = not blink_state
            
            if blink_state :
                rgb[0] = colors[color_index]
            else:
                rgb[0] = (0, 0, 0)
                
            rgb.write()
            last_blink_time = now
        # Vérification de la connexion et passe en mode local
        if is_remote_mode and time.ticks_diff(now, last_rx_time) > connection_timeout:
            is_remote_mode = False
            print("Mode Local : Partenaire perdu")
            current_color = colors[color_index]
            rgb[0] = current_color
            rgb.write()
            print("LED fixée sur :", current_color)
    # fonctionnement en mode local       
    else:
        # détection de flanc
        if current_S1 == 0 and last_S1 == 1:
            led_val ^= 1
            LED.value(led_val)
        # détection de flanc
        if current_S2 == 0 and last_S2 == 1:
            color_index = (color_index + 1) % len(colors)
            rgb[0] = colors[color_index]
            rgb.write()
    # sauvgarde de l'ancien état des boutons    
    last_S1 = current_S1    
    last_S2 = current_S2
    time.sleep_ms(1)