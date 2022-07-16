#define COM Serial2
#define HOST Serial

void setup(){
  pinMode(13, OUTPUT);
  
  int i = 0;
  while(i < 5){
    digitalWrite(13, HIGH);
    delay(25);
    digitalWrite(13, LOW);
    delay(25);
    
    i++;
  }
  
  HOST.begin(9600);
  COM.begin(9600);
  COM.transmitterEnable(12);
}

void loop(){
  // Host -> Com
  if(HOST.available() > 0){
    COM.write(HOST.read());
    digitalWrite(13, HIGH);
  }
  
  // Com -> Host
  if(COM.available() > 0){
    HOST.write(COM.read());
    digitalWrite(13, HIGH);
  }
}
