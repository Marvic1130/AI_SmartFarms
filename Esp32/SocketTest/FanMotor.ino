bool setFanState(const int fan_pin, String msg){
    if (msg.indexOf("f::True") != -1) {
        digitalWrite(fan_pin, HIGH);
    } 
    else if(msg.indexOf("f::False") != -1){
        digitalWrite(fan_pin, LOW);
    }
    else return false;

    return true;
}