const int BUTTON_1 = 12;
const int BUTTON_2 = 11;
const int BUTTON_3 = 10;
const int BUTTON_4 = 9;
const int BUTTON_5 = 8;
const int BUTTON_6 = 7;
const int BUTTON_7 = 6;
const int BUTTON_8 = 5;
const int BUTTON_9 = 4;
const int BUTTON_10 = 3;
const int LED = 3;
int BUTTON_1_state = 0;
int BUTTON_2_state = 0;
int BUTTON_3_state = 0;
int BUTTON_4_state = 0;
int BUTTON_5_state = 0;
int BUTTON_6_state = 0;
int BUTTON_7_state = 0;
int BUTTON_8_state = 0;
int BUTTON_9_state = 0;
int BUTTON_10_state = 0;
bool pressed = false;

int slider0_val = 0;
int slider1_val = 0;
int slider2_val = 0;
int slider3_val = 0;

void setup()
{
  Serial.begin(9600);
  Serial.setTimeout(1);
  pinMode(BUTTON_1, INPUT);
  pinMode(BUTTON_2, INPUT);
  pinMode(LED, OUTPUT);
}

void loop()
{
  BUTTON_1_state = digitalRead(BUTTON_1);
  BUTTON_2_state = digitalRead(BUTTON_2);
  BUTTON_3_state = digitalRead(BUTTON_3);
  BUTTON_4_state = digitalRead(BUTTON_4);
  BUTTON_5_state = digitalRead(BUTTON_5);
  BUTTON_6_state = digitalRead(BUTTON_6);
  BUTTON_7_state = digitalRead(BUTTON_7);
  BUTTON_8_state = digitalRead(BUTTON_8);
  BUTTON_9_state = digitalRead(BUTTON_9);
  BUTTON_10_state = digitalRead(BUTTON_10);
  slider0_val = analogRead(A0);
  slider0_val = map(slider0_val, 0, 1023, 0, 100);
  slider1_val = analogRead(A1);
  slider1_val = map(slider1_val, 0, 1023, 0, 100);
  slider2_val = analogRead(A3);
  slider2_val = map(slider2_val, 0, 1023, 0, 100);
  slider3_val = analogRead(A4);
  slider3_val = map(slider3_val, 0, 1023, 0, 100);

  Serial.print(slider0_val);
  Serial.print("\t");
  Serial.print(slider1_val);
  Serial.print("\t");
  Serial.print(slider2_val);
  Serial.print("\t");
  Serial.println(slider3_val);
  
  if (BUTTON_1_state == HIGH && pressed == false)
  {
    //digitalWrite(LED, HIGH);
    pressed = true;
    Serial.println("0");
  } 

  if (BUTTON_2_state == HIGH && pressed == false)
  {
    //digitalWrite(LED, HIGH);
    pressed = true;
    Serial.println("1");
  } 

  if (BUTTON_3_state == HIGH && pressed == false)
  {
    //digitalWrite(LED, HIGH);
    pressed = true;
    Serial.println("2");
  } 

  if (BUTTON_4_state == HIGH && pressed == false)
  {
    //digitalWrite(LED, HIGH);
    pressed = true;
    Serial.println("3");
  } 

  if (BUTTON_5_state == HIGH && pressed == false)
  {
    //digitalWrite(LED, HIGH);
    pressed = true;
    Serial.println("4");
  } 

  if (BUTTON_6_state == HIGH && pressed == false)
  {
    //digitalWrite(LED, HIGH);
    pressed = true;
    Serial.println("5");
  } 

  if (BUTTON_7_state == HIGH && pressed == false)
  {
    //digitalWrite(LED, HIGH);
    pressed = true;
    Serial.println("6");
  } 

  if (BUTTON_8_state == HIGH && pressed == false)
  {
    //digitalWrite(LED, HIGH);
    pressed = true;
    Serial.println("7");
  } 

  if (BUTTON_9_state == HIGH && pressed == false)
  {
    //digitalWrite(LED, HIGH);
    pressed = true;
    Serial.println("8");
  } 

  if (BUTTON_10_state == HIGH && pressed == false)
  {
    //digitalWrite(LED, HIGH);
    pressed = true;
    Serial.println("9");
  } 

  
  if (BUTTON_1_state == LOW && BUTTON_2_state == LOW && BUTTON_3_state == LOW && BUTTON_4_state == LOW && BUTTON_5_state == LOW && BUTTON_6_state == LOW && BUTTON_7_state == LOW && BUTTON_8_state == LOW && BUTTON_9_state == LOW && BUTTON_10_state == LOW)
  {
    pressed = false;
    //digitalWrite(LED, LOW);
    //Serial.println("false");
  }
}
