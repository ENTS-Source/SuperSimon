#define COM Serial2
#define HOST Serial

void setup(){
  pinMode(13, OUTPUT);
  
  int i = 0;
  while(i < 5){
    digitalWrite(13, HIGH);
    delay(100);
    digitalWrite(13, LOW);
    delay(100);
    
    i++;
  }
  
  HOST.begin(9600);
  COM.begin(9600);
  COM.transmitterEnable(12);
}

void loop(){
  COM.write(240); // Command (ECHO)
  COM.write(0); // Address (0)
  
  // Length (512)
  COM.write(0);
  COM.write(0);
  COM.write(2);
  COM.write(0);
  
  int expectedReturnAddr = 5;
  for(int i = 0; i < 512; i++){
    if(i == 0){
      COM.write(expectedReturnAddr);
    }else{
      COM.write(128);
    }
  }
  
  delay(2000); // Wait 1 second for data
  
  int cmd = COM.read();
  int addr = COM.read();
  
  // Flush buffer
  for(int i = 0; i < 128 + 4; i++){
    COM.read();
  }
  
  if(addr == expectedReturnAddr){
    digitalWrite(13, HIGH);
    delay(100);
    digitalWrite(13, LOW);
    delay(100);
    digitalWrite(13, HIGH);
    delay(100);
    digitalWrite(13, LOW);
  }else{
    digitalWrite(13, HIGH);
    delay(1000);
    digitalWrite(13, LOW);
  }
  
  //delay(5000);
}
