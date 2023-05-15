#include "ESP32Servo.h"

bool setServoState(Servo &servo, String msg){
  int angle = 100;
    if (msg.indexOf("s::True") != -1) {
        servo.write(angle);
    } 
    else if(msg.indexOf("s::False") != -1){
        servo.write(0);
    }
    else return false;

    return true;
}
