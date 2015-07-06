void setup(){
  pinMode(13, OUTPUT);
  
  pinMode(14, INPUT_PULLUP);
  pinMode(15, INPUT_PULLUP);
  pinMode(16, INPUT_PULLUP);
  
  Serial.begin(9600);
  Serial2.begin(9600, SERIAL_8N1);
  Serial2.transmitterEnable(12);

//  Serial2.write(100);
//  Serial2.write(1);
  
  int address = getAddress();
  int c = 0;
  while(c < address + 1){
    digitalWrite(13, HIGH);
    delay(200);
    digitalWrite(13, LOW);
    delay(200);
    c++;
  }
}

int getAddress(){
  int currentAddress = -1;
  
  if(digitalRead(14) == LOW){
    currentAddress = 0;
  }else if(digitalRead(15) == LOW){
    currentAddress = 1;
  }else if(digitalRead(16) == LOW){
    currentAddress = 2;
  }
  
  return currentAddress;
}

int lastCommand = -1;
int lastAddress = -1;
void loop(){
  // Check current address
  int currentAddress = getAddress();
  
  int val = Serial2.read();
  if(val >= 0){
    Serial.println("READ = " + (String)val);
  }
  if(lastCommand < 0){
    lastCommand = val;
  } else {
    lastAddress = val;
  }
    
  if(lastCommand >= 0 && lastAddress >= 0){
    Serial.println("Cmd = " + (String)lastCommand + ", Addr = " + (String)lastAddress);
    if(lastAddress == currentAddress){
      if(lastCommand == 1){
        digitalWrite(13, HIGH);
      }else if(lastCommand == 0){
        digitalWrite(13, LOW);
      }else if(lastCommand == 2){
        delay(1000);
        Serial2.write(1); // Command
        Serial2.write(2); // Address (5 for placeholder)
        Serial.println("Sent command 3 to address 5");
      }
    }
    
    lastCommand = -1;
    lastAddress = -1;
  }
}
