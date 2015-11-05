const int analogInPin = A0;
volatile long revolutions = 0;

void setup() {
  Serial.begin(250000);
  while (!Serial);
  Serial.println("ready");
}

int c = 0;
#define SIZE 3
int readings[SIZE] = {};

void loop() {
  int sensorValue = analogRead(analogInPin);
  readings[c] = sensorValue;
  c++;
  if (c == SIZE) {
    c = 0;
    int v = 0;
    for (int k = 0; k < SIZE; k++) v += readings[k];
    v /= SIZE;
    Serial.println(v);
    delay(100);
  }
}

