#define NUM_BUTTONS 5
#define READ_TIMEOUT 100
#define PIN_TRANSMIT_ENABLE 12
#define PIN_TONE 23
#define MAX_ROUNDS 50

#define CMD_ACK 0x0
#define CMD_BOARD_INFO 0x1
#define CMD_START_GAME 0x2
#define CMD_REQ_STATE 0x3
#define STATE_NOT_FINISHED 0x4
#define STATE_RESULTS 0x5
#define CMD_IS_JOINING 0x6
#define RSP_NOT_JOINING 0x7
#define RSP_JOINING 0x8
#define CMD_DISCOVER 0x9
#define CMD_ECHO 0xF0

#define SHOWING_PATTERN_START 0
#define SHOWING_SPACE 1
#define SHOWING_LIGHT 2

// Game over when haven't received a command in too long
#define CMD_SILENT_TIMEOUT 10000
unsigned long lastCommandTime = 0;

// Initial game parameters
int INIT_BUTTON_LIGHT_TIME = 300;
int INIT_BUTTON_LIGHT_SPACE = 150;
int INIT_BUTTON_TIMEOUT = 3000;
int INIT_PATTERN_START_DELAY = 300;

// Modifiable game parameters
int BUTTON_LIGHT_TIME = 200;
int BUTTON_LIGHT_SPACE = 50;
int BUTTON_TIMEOUT = 3000;
int PATTERN_START_DELAY = 50;

// Fixed game parameters
int ACCELERATION = 0;
boolean WAIT_EACH_ROUND = true;

// Variables for showing pattern
unsigned long showingNextStepTime = 0;
int showingButton = 0;
int showingStep = 0;

byte pattern[MAX_ROUNDS];
int patternLength = 0;
volatile int patternPos = 0;
boolean isGameOver = false;
boolean startGame = false;
volatile boolean nextPattern = false;
volatile boolean roundComplete = false;
boolean gameOverLit = false;
volatile boolean running = false;
boolean gameRunning = false;
boolean joining = false;
boolean showingPattern = false;
volatile int button = 0;
volatile boolean pressed = false;
volatile boolean triggerGameOver = false;
volatile unsigned long lastButton = 0;
volatile short buttonTimes[MAX_ROUNDS];
byte cmdBuffer[256];
byte cmdMagic[] = {0xDE, 0xAD, 0xBE, 0xEF};
byte rspMagic[] = {0xCA, 0xFE, 0xBA, 0xBE};

// Settings variables
// 1-4 - playerNum
// 5 - standalone
// 6 - unallocated
// 7 - unallocated
// 8 - unallocated
byte settings = 0;
int playerNum = 0;
boolean standalone = false;

// LEDs
// 3 - Blue
// 5 - White
// 7 - Green (not working)
// 9 - Yellow
// 11 - Red
int pins[] = {2, 4, 6, 8, 10};
int leds[] = {3, 5, 7, 9, 11};
int tones[] = {415, 360, 310, 252, 209}; // Hz
// Colors  Green, White, REd, Yellow, Blue
int gameOverTone = 42; // Hz


void btnFunc(int pin) {
  boolean pressed = digitalRead(pins[pin]) == LOW;
  if (!showingPattern) {
    if (pressed) {
      button |= 1 << pin;
      digitalWrite(leds[pin], HIGH);
      if (!gameOverLit) {
        tone(PIN_TONE, tones[pin]);
      }
    }
    else {
      button &= ~(1 << pin);
      // Don't clear lit LEDs when showing game over lights
      if (!gameOverLit) {
        digitalWrite(leds[pin], LOW);
        noTone(PIN_TONE);
      }
    }
    
    testButtonPress();
  }
}


// If running the game, tests whether the current button is correct 
// and moves through the pattern
void testButtonPress() {
  if (running && !isGameOver) {
    // If button is pressed, process press (if not already done)
    if (!pressed && button != 0) {
      pressed = true;
      
      if (button == (1 << pattern[patternPos])) {
        // Reset button timer
        buttonTimes[patternPos] = millis() - lastButton;
        lastButton = millis();
      }
      else {
        // If wrong button pressed, game is over
        // since running in interrupt, trigger game over for main loop
        triggerGameOver = true;
      }
    }
        
    // If button was pressed and is no longer, advance pattern
    if (pressed && button == 0) {
      pressed = false;
      
      patternPos += 1;
      if (patternPos == patternLength) {
        roundComplete = true;
        // Start pattern if not waiting between rounds
        if (!WAIT_EACH_ROUND) {
          nextPattern = true;
        } else {
          // Pause game until next round starts
          running = false;
        }
      }
    }
  }
}

void btn1func() {
  btnFunc(0);
}
void btn2func() {
  btnFunc(1);
}
void btn3func() {
  btnFunc(2);
}
void btn4func() {
  btnFunc(3);
}
void btn5func() {
  btnFunc(4);
}

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);  // USB
  Serial1.begin(9600); // RS485
  Serial1.transmitterEnable(PIN_TRANSMIT_ENABLE);
   
  for (int pin = 0; pin < NUM_BUTTONS; pin++) {
    pinMode(pins[pin], INPUT_PULLUP);
  }
  
  for (int led = 0; led < NUM_BUTTONS; led++) {
    pinMode(leds[led], OUTPUT);
    digitalWrite(leds[led], LOW);
  }
  
  // Setup DIP switch pins for input (pulldown)
  // and read settings
  volatile uint32_t *config;
  for (int i = 14; i < 21; i++) {
    config = portConfigRegister(i);
    *portModeRegister(i) = 0;
    __disable_irq();
    // INPUT
    *config &= ~PORT_PCR_MUX_MASK;
    *config |= PORT_PCR_MUX(1);
    // PULLDOWN
    *config |= (PORT_PCR_PE);
    *config &= ~(PORT_PCR_PS);
    __enable_irq()
  }
  readSettings();
 
  randomSeed(analogRead(A5));
  
  attachInterrupt(pins[0], &btn1func, CHANGE);
  attachInterrupt(pins[1], &btn2func, CHANGE);
  attachInterrupt(pins[2], &btn3func, CHANGE);
  attachInterrupt(pins[3], &btn4func, CHANGE);
  attachInterrupt(pins[4], &btn5func, CHANGE);
}

void readSettings() {
  settings = 0;
  for (int i = 14; i < 21; i++) {
    settings |= (digitalRead(i) == HIGH) << (20 - i);
  }
  
  playerNum = settings & 0xF;
  standalone = (settings >> 5) & 1;
}

void getPattern() {
  for (byte i = 0; i < MAX_ROUNDS; i++) {
    pattern[i] = random(NUM_BUTTONS);
  }
}

void initGame() {
  gameRunning = true;
  startGame = true;
  roundComplete = false;
  BUTTON_LIGHT_TIME = INIT_BUTTON_LIGHT_TIME;
  BUTTON_LIGHT_SPACE = INIT_BUTTON_LIGHT_SPACE;
  BUTTON_TIMEOUT = INIT_BUTTON_TIMEOUT;
  PATTERN_START_DELAY = INIT_PATTERN_START_DELAY;
}

void accelerate() {
  BUTTON_LIGHT_TIME = BUTTON_LIGHT_TIME * ((100 - ACCELERATION) / 100.0f);
  BUTTON_LIGHT_SPACE = BUTTON_LIGHT_SPACE * ((100 - ACCELERATION) / 100.0f);
  BUTTON_TIMEOUT = BUTTON_TIMEOUT * ((100 - ACCELERATION) / 100.0f);
  PATTERN_START_DELAY = PATTERN_START_DELAY * ((100 - ACCELERATION) / 100.0f);
}

void gameOver() {
  gameRunning = false; 
  isGameOver = true;
  running = false;
  pressed = false;
  roundComplete = true;
  
  // Mark any unpressed buttons as failed presses
  for (int i = patternPos; i < patternLength; i++) {
    buttonTimes[i] = -1;
  }
  
  // Light LEDs for game over and set time to turn off lights
  gameOverLit = true;
  noTone(PIN_TONE);
  tone(PIN_TONE, gameOverTone);
  for (int i = 0; i < NUM_BUTTONS; i++) {
    digitalWrite(leds[i], HIGH);
  }
  
  showingNextStepTime = millis() + 2000;
}

void showPattern() {
  showingPattern = true;
  showingStep = SHOWING_PATTERN_START;
  showingNextStepTime = millis() + PATTERN_START_DELAY;
}

int getButton() {
  if (digitalRead(A0) == LOW) {
    return 0;
  }
  if (digitalRead(A1) == LOW) {
    return 1;
  }
  if (digitalRead(A2) == LOW) {
    return 2;
  }
  if (digitalRead(A3) == LOW) {
    return 3;
  }
  if (digitalRead(A4) == LOW) {
    return 4;
  }
  return -1;
}

void waitClear() {
  // Wait until no button clear
  while (button != 0) {
  }
}

bool readWithTimeout(byte &readByte) {
  unsigned long startMs = millis();
  while (millis() - startMs < READ_TIMEOUT) {
    if (Serial1.available()) {
      readByte = Serial1.read();
      return true;
    }
  }
  return false;
}

void writeLong(long data) {
  Serial1.write(data >> 24);
  Serial1.write(data >> 16);
  Serial1.write(data >> 8);
  Serial1.write(data);
}

bool readLong(long &data) {
  long dataLen = 0;
  byte readByte = 0;
  if (!readWithTimeout(readByte)) {
    return false;
  }
  dataLen ^= readByte << 24;
  if (!readWithTimeout(readByte)) {
    return false;
  }
  dataLen ^= readByte << 16;
  if (!readWithTimeout(readByte)) {
    return false;
  }
  dataLen ^= readByte << 8;
  if (!readWithTimeout(readByte)) {
    return false;
  }
  dataLen ^= readByte;
  data = dataLen;
  return true;
}

// For easier debugging / testing through arduino IDE
void oldReadCommand() {
  char cmd;
  if (cmd == 'S') {
    initGame();
  }
  else if (cmd == 's') {
    // Start round
    nextPattern = true;
  }
  else if (cmd == 'L') {
    // Read button light time
    INIT_BUTTON_LIGHT_TIME = Serial.parseInt();
  }
  else if (cmd == 'K') {
    // Read button light space
    INIT_BUTTON_LIGHT_SPACE = Serial.parseInt();
  }
  else if (cmd == 'R') {
    // Random seed
    randomSeed(Serial.parseInt());
  }
  else if (cmd == 'D') {
    // Pattern start delay
    INIT_PATTERN_START_DELAY = Serial.parseInt();
  }
  else if (cmd == 'W') {
    // Wait each round?
    WAIT_EACH_ROUND = Serial.parseInt() == 1;
  }
  else if (cmd == 'A') {
    // Set acceleration
    ACCELERATION = Serial.parseInt();
  }
  else if (cmd == 'T') {
    // Send status: playing/passed/failed
    // Wait for next byte (playerNum)
   while (!Serial.available()) {} 
   char cmd = Serial.read();
   if (cmd - '0' == playerNum) {
     Serial.write('X');
   }
  }
  else if (cmd == 'E') {
    // Echo (debug)
    Serial.println("Echo");
  }
  else if (cmd == 'Q') {
    // Echo settings
    readSettings();
    Serial.println(settings, BIN);
  }
}

// Should timeout if reading command but no data
void readCommand() {
  // Clear buffer
  for (int i = 0; i < 100; i++) {
    cmdBuffer[i] = 0;
  }
  
  byte readByte;
  
  // All commands should start with 0xDEADBEEF
  if (!readWithTimeout(readByte) || readByte != 0xDE) {
    return;
  }
  if (!readWithTimeout(readByte) || readByte != 0xAD) {
    return;
  }
  if (!readWithTimeout(readByte) || readByte != 0xBE) {
    return;
  }
  if (!readWithTimeout(readByte) || readByte != 0xEF) {
    return;
  }
  
  lastCommandTime = millis();
  
  char cmd;
  byte addr;
  
  // Read cmd
  if (!readWithTimeout(readByte)) {
    return;
  }
  cmd = readByte;

  if (cmd == CMD_BOARD_INFO) {
    if (!readWithTimeout(addr)) {
      return;
    }
    if (addr != playerNum) {
      return;
    }
    
    long dataLen = 0;
    if (!readLong(dataLen)) {
      return;
    }
    
    patternLength = dataLen;
    
    for (long i = 0; i < dataLen; i++ ){
      if (!readWithTimeout(readByte)) {
        return;
      }
      // Ignore more rounds than we can store
      if (dataLen < MAX_ROUNDS) {
        pattern[i] = readByte - 1;
      }
    }
    
    Serial1.write(rspMagic, 4);
    Serial1.write(CMD_ACK);
    
    if (gameRunning) {
      nextPattern = true;
    }
    else {
      initGame();
    } 
  }
  else if (cmd == CMD_START_GAME) {
    if (!joining) {
      // Do not start if not joining game
      // Standalone would get messed up
      return;
    }
    
    if (gameRunning) {
      nextPattern = true;
    }
    else {
      initGame();
    }  
  }
  else if (cmd == CMD_REQ_STATE) {
    if (!readWithTimeout(addr)) {
      return;
    }
    if (addr != playerNum) {
      return;
    }
    
    Serial1.write(rspMagic, 4);
    if (!roundComplete) {
      Serial1.write(STATE_NOT_FINISHED);
    }
    else {
      Serial1.write(STATE_RESULTS);
      Serial1.write((byte)playerNum);
      writeLong(patternLength * 3);
      for (int i = 0; i < patternLength; i++) {
        Serial1.write(pattern[i] + 1);
        Serial1.write(buttonTimes[i] >> 8);
        Serial1.write(buttonTimes[i]);
      }
    }
  }
  else if (cmd == CMD_IS_JOINING) {
    if (!readWithTimeout(addr)) {
      return;
    }
    if (addr != playerNum) {
      return;
    }
    
    Serial1.write(rspMagic, 4);
    Serial1.write(joining ? RSP_JOINING : RSP_NOT_JOINING);
  }
  // TODO - game end 0xA
  else if (cmd == CMD_DISCOVER) {
    if (!readWithTimeout(addr)) {
      return;
    }
    if (addr != playerNum) {
      return;
    }
    Serial1.write(rspMagic, 4);
    Serial1.write(CMD_ACK);
  }
  else if (cmd == CMD_ECHO) {
    if (!readWithTimeout(addr)) {
      return;
    }
    if (addr != playerNum) {
      return;
    }
    
    long dataLen = 0;
    if (!readLong(dataLen)) {
      return;
    }    
    
    for (int i = 0; i < dataLen; i++) {
      if (!readWithTimeout(readByte)) {
        return;
      }
      cmdBuffer[i] = readByte;
    }
    
    Serial1.write(rspMagic, 4);
    Serial1.write(CMD_ECHO);
    Serial1.write(cmdBuffer[0]);
    writeLong(dataLen);
    Serial1.write(cmdBuffer, dataLen);
  }
}

void loop() {  
  readCommand();
  
  if (!isGameOver && (millis() - lastCommandTime > CMD_SILENT_TIMEOUT)) {
    gameOver();
  }
  
  if (gameOverLit) {
    // Do not proceed until ready for next step
    if (millis() < showingNextStepTime) {
      return;
    }
    gameOverLit = false;
    for (int i = 0; i < NUM_BUTTONS; i++) {
      digitalWrite(leds[i], LOW);
    }
    noTone(PIN_TONE);
  }
  
  if (showingPattern) {
    // Do not proceed until ready for next step
    if (millis() < showingNextStepTime) {
      return;
    }
    
    switch (showingStep) {
      case SHOWING_PATTERN_START:
        showingButton = 0;
        showingStep = SHOWING_SPACE;
        break;
      case SHOWING_SPACE:
        // Start showing button
        noTone(PIN_TONE);
        digitalWrite(leds[pattern[showingButton]], HIGH);
        tone(PIN_TONE, tones[pattern[showingButton]]);
        showingStep = SHOWING_LIGHT;
        showingNextStepTime = millis() + BUTTON_LIGHT_SPACE;
        break;
      case SHOWING_LIGHT:
        // Stop showing button
        digitalWrite(leds[pattern[showingButton]], LOW);
        noTone(PIN_TONE);
        showingButton += 1;
        showingStep = SHOWING_SPACE;
        showingNextStepTime = millis() + BUTTON_LIGHT_TIME;
        if (showingButton >= patternLength) {
          showingPattern = false;
        }
        break;
    }
    
    // Must reset button timer after displaying pattern (otherwise auto gameover)
    lastButton = millis();
    
    // Do not process game while showing pattern
    return;
  }
  
  if (!running && button != 0) {
    while(button != 0) {
      // Wait for button to be released
      // TODO - will miss commands?
    }
    
    if (standalone) {
      delay(1000);
      initGame();
    }
    else {
      joining = true;
    }
  }
  
  if (startGame) {
    joining = false;
    isGameOver = false;
    startGame = false;
    if (standalone) {
      getPattern();
      WAIT_EACH_ROUND = false;
      // In managed mode, pattern length comes from board info command
      patternLength = 0;
    }
    
    // Game start is always pattern start
    nextPattern = true;
  }
  
  if (nextPattern) {
    roundComplete = false;
    nextPattern = false;
    accelerate();
    // In managed mode, pattern length comes from board info command
    if (standalone) {
      patternLength += 1;
    }
    patternPos = 0;
    showPattern();
    running = true;
    // Reset button timer
    for (int i = 0; i < MAX_ROUNDS; i++) {
      buttonTimes[i] = 0;
    }
    lastButton = millis();
  }
  
  if (running && !isGameOver) {
    // If too long between buttons, game is over
    if (millis() - lastButton >= BUTTON_TIMEOUT) {
      gameOver();
    }
    
    if (triggerGameOver) {
      triggerGameOver = false;
      gameOver();
    }
  }
}


void animate() {
  for (int i = 0; i < 10; i++) {
    for (int x = 0; x < NUM_BUTTONS; x++) {
      digitalWrite(leds[x], HIGH);
      delay(100);
      digitalWrite(leds[x], LOW);
    }
  }
}


