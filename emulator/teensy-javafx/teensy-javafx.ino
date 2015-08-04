#define HOST Serial
#define PROXY Serial2

void setup(){
  pinMode(13, OUTPUT);
  
  HOST.begin(9600);
  
  PROXY.begin(9600);
  PROXY.transmitterEnable(12);
  
  int i = 0;
  while(i < 5){
    digitalWrite(13, HIGH);
    delay(100);
    digitalWrite(13, LOW);
    delay(100);
    
    i++;
  }
}

int serialFind[] = {0xD, 0xE, 0xA, 0xD, 0xC, 0x0, 0xD, 0xE}; // 0xDEADCODE
int magicLength = 8;
int magicIndex = 0;

int lastOn = millis();

void loop(){
  if(HOST.available() > 0){
    lastOn = millis();
    digitalWrite(13, HIGH);  
    int b = HOST.read();
    if(b == serialFind[magicIndex]){
      magicIndex++;
      if(magicIndex >= magicLength){
        HOST.println("HELLOWORLD");
        magicIndex = 0;
      }
    }else{
      for(int i = 0; i < magicIndex; i++){
        PROXY.write(serialFind[i]);
      }
      PROXY.write(b);
      magicIndex = 0;
    }
  }
  if(millis() - lastOn > 500 || true){
    digitalWrite(13, LOW);
  }
  if(PROXY.available() > 0 && magicIndex == 0){
    HOST.write(PROXY.read());
  }
}
