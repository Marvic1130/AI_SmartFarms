
bool setLedState(const int* ledarr, String msg){
    int led_pin = ledarr[int(msg[1] - '0')];
    if (msg.indexOf("::True") != -1) {
        digitalWrite(led_pin, HIGH);
    } 
    else if(msg.indexOf("::False") != -1){
        digitalWrite(led_pin, LOW);
    }
    else return false;

    return true;
}