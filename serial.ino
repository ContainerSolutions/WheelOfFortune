const int analogInPin = A0;
const int digitalOutPin = 13;
int sensorValue = 0;

volatile long revolutions = 0;

void setup() {
  Serial.begin(250000);
  while (!Serial);
  pinMode(digitalOutPin, OUTPUT);

  //  attachInterrupt(digitalPinToInterrupt(2), ISR, mode);

  Serial.println("ready");
}





void loop() {
  sensorValue = analogRead(analogInPin);
  if (sensorValue < 505) { // notice that the normal value of the sensor is 510
    digitalWrite(digitalOutPin, HIGH);
  } else {
    digitalWrite(digitalOutPin, LOW);
  }

  Serial.println(sensorValue);



  delay(10);
}

