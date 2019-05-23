#include<Servo.h>

Servo servoVer; //Vertical Servo
Servo servoHor; //Horizontal Servo

int x;
int y;

int midx = 250;
int midy = 200;

double kp = -0.035;

int servoX = 90;
int servoY = 90;

void setup()
{
  Serial.begin(9600);
  servoVer.attach(5); 
  servoHor.attach(6); 
  servoVer.write(servoX);
  servoHor.write(servoY);
}

void Pos()
{
  double deltax = x - midx;
  double deltay = y - midy;

  double gainX = kp * deltax;
  double gainY = kp * deltay;

  if (servoX + gainX < 180 && servoX + gainX > 0 && servoY + gainY < 180 && servoY + gainY > 0)
  {
    servoX += gainX;
    servoY += gainY;
  }

  servoX = min(servoX, 178);
  servoX = max(servoX, 2);
  servoY = min(servoY, 178);
  servoY = max(servoY, 2);

  servoHor.write(servoX);
  servoVer.write(servoY);
}

void loop()
{
  if(Serial.available() > 0)
  {
    if(Serial.read() == 'X')
    {
      x = Serial.parseInt();
      if(Serial.read() == 'Y')
      {
        y = Serial.parseInt();
       Pos();
      }
    }
    while(Serial.available() > 0)
    {
      Serial.read();
    }
  }
}
