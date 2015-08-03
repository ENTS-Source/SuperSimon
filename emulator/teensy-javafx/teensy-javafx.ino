#define HOST Serial
#define PROXY Serial2

void setup(){
  pinMode(13, OUTPUT);
  digitalWrite(13, HIGH);
  
  HOST.begin(9600);
  
  PROXY.begin(9600);
  PROXY.transmitterEnable(12);
  
  digitalWrite(13, LOW);
}

int serialFind[] = {0xD, 0xE, 0xA, 0xD, 0xC, 0x0, 0xD, 0xE}; // 0xDEADCODE
int magicLength = 8;
int magicIndex = 0;

void loop(){
  if(magicIndex > 0){
    digitalWrite(13, HIGH);  
  }else{
    digitalWrite(13, LOW);
  }
  if(HOST.available() > 0){
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
  if(PROXY.available() > 0 && magicIndex == 0){
    HOST.write(PROXY.read());
  }
}
