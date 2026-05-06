#include <Arduino.h>

// 1. Définitions des broches
#define BTN_S1  4
#define BTN_S2  5
#define LED     6
#define RGB     48

// 2. Variables globales
int color = 1;
bool led = LOW;
bool Last_S2 = HIGH;
bool Last_S1 = HIGH;
bool CurrentS1 = LOW;
bool CurrentS2 = LOW;

void setup() {
  // Configuration des broches
  pinMode(BTN_S1, INPUT_PULLUP);
  pinMode(BTN_S2, INPUT_PULLUP);
  pinMode(LED, OUTPUT);
  // Initialisation de la LED (Eteinte au début)
  neopixelWrite(RGB, 0, 0, 0);
}

void loop() {
  // Lecture du bouton
  CurrentS1 = digitalRead(BTN_S1);
  CurrentS2 = digitalRead(BTN_S2);
  if ((CurrentS1 == LOW) && (Last_S1 == HIGH)) 
  {
    led = !led;
    digitalWrite(LED,led);
  }

  // Détection de l'appui (Front descendant car INPUT_PULLUP)
  if ((CurrentS2 == LOW) && (Last_S2 == HIGH)) 
  {
    if (color > 2) 
    color = 0;
    // Changement de couleur
    switch (color)
    {
    case 0:
      neopixelWrite(RGB, 1, 0, 0); // Rouge
      break;
    case 1:
      neopixelWrite(RGB, 0, 1, 0); // Rouge
      break;
      case 2:
      neopixelWrite(RGB, 0, 0, 1); // Rouge
      break;
    default:
      neopixelWrite(RGB, 1, 0, 0);
      break;
    }
    color++;
  }
  Last_S1 = CurrentS1;
  Last_S2 = CurrentS2;
  delay(50); // Anti-rebond
}