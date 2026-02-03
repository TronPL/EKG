#include <Arduino.h>

/*
 * Konfiguracja Pinów
 */
const int SENSOR_PIN = 4; // GPIO 4 (ADC)
const int LED_PIN = 2;    // GPIO 2

// --- KONFIGURACJA ECG ---
// Próg detekcji - dostosuj wg Teleplot!
int threshold = 3000; 

// --- ZMIENNE DO BPM ---
long lastBeatTime = 0;       
long currentMillis = 0;      
const int refractoryPeriod = 300; // Min. 300ms między uderzeniami

// --- ZMIENNE DO UŚREDNIANIA (Średnia Krocząca) ---
const int numReadings = 20;     // Liczba pomiarów do średniej
int readings[numReadings];      // Tablica (bufor) na wyniki
int readIndex = 0;              // Pozycja w tablicy
long total = 0;                 // Suma wyników w tablicy
int averageBPM = 0;             // Wynik końcowy (uśredniony)
int validReadingsCount = 0;     // Licznik ile mamy już poprawnych próbek (na start)

void setup() {
  Serial.begin(115200);
  delay(2000);

  pinMode(SENSOR_PIN, INPUT);
  pinMode(LED_PIN, OUTPUT);

  // Zerowanie bufora historii
  for (int i = 0; i < numReadings; i++) {
    readings[i] = 0;
  }
  
  Serial.println("Start systemu EKG (Średnia z 20 uderzeń)...");
}

void loop() {
  int sensorValue = analogRead(SENSOR_PIN);
  currentMillis = millis();

  // Wykrywanie piku
  if (sensorValue > threshold && (currentMillis - lastBeatTime > refractoryPeriod)) {
    
    long delta = currentMillis - lastBeatTime;
    lastBeatTime = currentMillis;

    // 1. Obliczamy chwilowe BPM
    int instantBPM = 60000 / delta;

    // Zabezpieczenie: Ignorujemy nierealne wyniki (np. szumy dające 300 BPM lub < 30)
    if (instantBPM > 30 && instantBPM < 240) {
      
      // 2. Obsługa średniej kroczącej (Circular Buffer)
      
      // Odejmujemy najstarszy odczyt od sumy
      total = total - readings[readIndex];
      
      // Wstawiamy nowy odczyt do tablicy
      readings[readIndex] = instantBPM;
      
      // Dodajemy nowy odczyt do sumy
      total = total + readings[readIndex];
      
      // Przesuwamy indeks na kolejne miejsce
      readIndex = readIndex + 1;

      // Jeśli dotarliśmy do końca tablicy, wracamy na początek
      if (readIndex >= numReadings) {
        readIndex = 0;
      }

      // Licznik próbek (tylko na początku, żeby nie dzielić przez 20, gdy mamy 2 wyniki)
      if (validReadingsCount < numReadings) {
        validReadingsCount++;
      }

      // 3. Obliczamy średnią
      averageBPM = total / validReadingsCount;
      
      // Mignięcie diodą
      digitalWrite(LED_PIN, HIGH);
    }
  } else {
    if(sensorValue < threshold) {
       digitalWrite(LED_PIN, LOW);
    }
  }

  // --- TELEPLOT ---
  // EKG w czasie rzeczywistym
  Serial.print(">ECG:");
  Serial.println(sensorValue);
  
  // Próg
  Serial.print(">Threshold:");
  Serial.println(threshold);

  // Średnie tętno (to nas interesuje)
  Serial.print(">AvgBPM:");
  Serial.println(averageBPM);

  // (Opcjonalnie) Chwilowe tętno - żebyś widział różnicę, jak skacze
  // Serial.print(">InstantBPM:");
  // Serial.println(60000 / (currentMillis - lastBeatTime)); // To tylko poglądowo, może być niedokładne poza if-em

  delay(10);
}