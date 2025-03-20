#define BLYNK_TEMPLATE_ID "TMPL35vEu-Y1o"
#define BLYNK_TEMPLATE_NAME "Smart Agriculture"
#define BLYNK_AUTH_TOKEN "jc6A-r6_qjlfwBBWzn0dXNvuKAsIFb9s"

#include <Wire.h>
#include <LiquidCrystal_I2C.h>
#include <WiFi.h>
#include <BlynkSimpleEsp32.h>
#include <DHT.h>

// Updated WiFi Credentials
const char* ssid = "Agriculture";
const char* password = "safalsingh";

// Pin Definitions
#define MOISTURE_SENSOR_1 34  
#define MOISTURE_SENSOR_2 35  
#define DHTPIN 4              
#define RELAY_1 26            
#define RELAY_2 27            
#define LED_PIN 2             // ESP32 built-in LED for status
#define DHTTYPE DHT22        

DHT dht(DHTPIN, DHTTYPE);
LiquidCrystal_I2C lcd(0x27, 16, 2);  // Keep this  

const int moistureThreshold = 30; 

BlynkTimer timer;

void setup() {
    Serial.begin(115200);

    // WiFi Connection
    Serial.println("Connecting to WiFi...");
    WiFi.begin(ssid, password);
    while (WiFi.status() != WL_CONNECTED) {
        delay(500);
        Serial.print(".");
    }
    Serial.println("\nConnected to WiFi!");
    Blynk.begin(BLYNK_AUTH_TOKEN, ssid, password);
    
    // LCD Setup
    lcd.begin();   // Initialize LCD
    lcd.backlight();
    lcd.clear();
    lcd.setCursor(0, 0);
    lcd.print("Smart Agriculture");


    // Sensor & Relay Setup
    dht.begin();
    pinMode(RELAY_1, OUTPUT);
    pinMode(RELAY_2, OUTPUT);
    pinMode(LED_PIN, OUTPUT);  // LED for status indication

    digitalWrite(RELAY_1, HIGH);  // Relay OFF (Assuming Active LOW)
    digitalWrite(RELAY_2, HIGH);
    digitalWrite(LED_PIN, LOW);   // LED OFF initially

    // Blynk Timer (Every 2 seconds)
    timer.setInterval(2000L, sendSensorData);
}

void sendSensorData() {
    int moisture1 = map(analogRead(MOISTURE_SENSOR_1), 4095, 0, 0, 100);
    int moisture2 = map(analogRead(MOISTURE_SENSOR_2), 4095, 0, 0, 100);
    float temperature = dht.readTemperature();
    float humidity = dht.readHumidity();

    // Send Data to Blynk
    Blynk.virtualWrite(V1, moisture1);
    Blynk.virtualWrite(V2, moisture2);
    Blynk.virtualWrite(V3, temperature);
    Blynk.virtualWrite(V4, humidity);

    // Relay Control Logic
    bool relay1State = (moisture1 < moistureThreshold) ? LOW : HIGH;
    bool relay2State = (moisture2 < moistureThreshold) ? LOW : HIGH;

    digitalWrite(RELAY_1, relay1State);
    digitalWrite(RELAY_2, relay2State);

    Blynk.virtualWrite(V5, relay1State == LOW ? 1 : 0);
    Blynk.virtualWrite(V6, relay2State == LOW ? 1 : 0);

    // LED Indicator for Relay Activity
    digitalWrite(LED_PIN, (relay1State == LOW || relay2State == LOW) ? HIGH : LOW);

    // Update LCD
    displayLCD(moisture1, moisture2, temperature, humidity, relay1State, relay2State);
}

void displayLCD(int moisture1, int moisture2, float temp, float hum, bool relay1, bool relay2) {
    static int displayState = 0;
    lcd.clear();
    
    if (displayState == 0) {
        lcd.setCursor(0, 0);
        lcd.print("Moisture1: " + String(moisture1) + "%");
        lcd.setCursor(0, 1);
        lcd.print("Moisture2: " + String(moisture2) + "%");
    } else if (displayState == 1) {
        lcd.setCursor(0, 0);
        lcd.print("Temp: " + String(temp) + "C");
        lcd.setCursor(0, 1);
        lcd.print("Humidity: " + String(hum) + "%");
    } else {
        lcd.setCursor(0, 0);
        lcd.print("Relay1: " + String(relay1 == LOW ? "ON" : "OFF"));
        lcd.setCursor(0, 1);
        lcd.print("Relay2: " + String(relay2 == LOW ? "ON" : "OFF"));
    }

    displayState = (displayState + 1) % 3;
}

// Manual Blynk Relay Control
BLYNK_WRITE(V7) {
    int value = param.asInt();
    digitalWrite(RELAY_1, value ? LOW : HIGH);
    Serial.print("Relay 1: ");
    Serial.println(value ? "ON" : "OFF");
}

BLYNK_WRITE(V8) {
    int value = param.asInt();
    digitalWrite(RELAY_2, value ? LOW : HIGH);
    Serial.print("Relay 2: ");
    Serial.println(value ? "ON" : "OFF");
}

void loop() {
    Blynk.run();
    timer.run();
}  
