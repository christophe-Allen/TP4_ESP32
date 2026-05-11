# TP4_ESP32 CAH


## Installation VScode et PlatformIO


## Installation Thonny


### Configuration de Thonny
 

## Code C
En C j'ai seulement utilisé la librairie arduino.

Grace à la fonction pinMode on peut changer nos IOs en entrées ou en sortie
<img width="299" height="75" alt="image" src="https://github.com/user-attachments/assets/b48af25a-7e87-4627-ba18-4c72a5714713" />

Pour lire nos entrées configurer la fonction digitalread est utiliseé
<img width="264" height="42" alt="image" src="https://github.com/user-attachments/assets/4143f37c-e1a1-4a09-a101-cc962bc50681" />

La lecture des deux LEDs se fait avec 2 fonction différente.
Pour la LED D1 sur le DevKit j'ai utiliser la fonction digitalRead
<img width="191" height="46" alt="image" src="https://github.com/user-attachments/assets/d5a9b253-5052-48fc-b29d-a5f3ab0fe466" />

et pour la LED RGB la fonction neopixelWrite
<img width="378" height="36" alt="image" src="https://github.com/user-attachments/assets/a2610ec3-0209-418f-b6dc-582188e7f943" />

## Code MicroPython

### ESP NOW
La librairie ESP_NOW permet aux esp de communiquer. La communication se fait via WIFI en WLAN et n'as pas besoin de routeur WIFI. Les esp communique directment entre eux c'est du 
point à point.
L'esp envoi toute les secondes un message spécifique à tout les esp actif.

### Mode Remote
le bouton S2 des esp32 change la LED RGB avec l'envoi d'un autre message quand on appuie sur le bouton à l'autre carte et les 2 LED clignotent à 2Hz.
Si la connexion est perdu pendant 2s on passera automatiquement en mode local. 

### Mode Local
Dans ce mode le bouton S2 change la couleur de sa LED.
Pour passer dans le mode remote, il faut un autre esp avec comme filtre le message envoyer par l'autre esp.


le bouton S1 change l'état de la LED D1 dans les 2 modes.
