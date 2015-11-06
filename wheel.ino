#define READ_PIN    A0
#define TRESHOLD    450
#define LOOP_DELAY  10
#define BAUD_RATE   250000

bool state = HIGH;
int lowRead;

void setup() {
  Serial.begin(BAUD_RATE);
  while (!Serial);
  Serial.println("ready");
}

void loop() {
  int sensorValue = analogRead(READ_PIN);
  if (sensorValue <= TRESHOLD) {
    state = LOW;
    lowRead = sensorValue;
  } else if (state == LOW) {
    state = HIGH;

    char buff[200];
    sprintf(buff, "%3d at %lu", lowRead, millis());
    Serial.println(buff);
  }
  delay(LOOP_DELAY);
}

