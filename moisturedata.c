#define BLYNK_PRINT Serial
#define BLYNK_TEMPLATE_ID "TMPL3cKhhlI9F"
#define BLYNK_TEMPLATE_NAME "Quickstart Device"
#define BLYNK_AUTH_TOKEN "C9fIQMhtIVfjvjbNBJcy6HqawNML58OW"

#include <WiFi.h>
#include <BlynkSimpleEsp32.h>
#include <DHT.h>
#include <WebServer.h>
#include <Wire.h>
#include <LiquidCrystal_I2C.h>

// 🔹 WiFi Credentials
const char *ssid = "M34";  
const char *password = "KUNAL1018";

// 🔹 Blynk Authentication Token
char auth[] = BLYNK_AUTH_TOKEN;

// 🔹 Sensor & Relay Pin Definitions
#define SOIL_SENSOR_1 34
#define SOIL_SENSOR_2 35
#define DHT_PIN 4
#define RELAY_1 25
#define RELAY_2 26

// 🔹 Moisture Threshold for Pump Activation
#define MOISTURE_THRESHOLD 30

// 🔹 Initialize DHT Sensor
DHT dht(DHT_PIN, DHT22);

// 🔹 Create Web Server
WebServer server(80);

// 🔹 LCD Display - Initialize LCD with I2C address, columns, and rows
LiquidCrystal_I2C lcd(0x27, 16, 2);  // LCD address 0x27 for 16x2 LCD

// 🔹 Global Variables for Sensor Readings
int moisture1 = 0, moisture2 = 0;
float temperature = 0.0, humidity = 0.0;

// 🚀 Handle Web Page Request
void handleRoot() {
    String webpage = "<html><head><title>ESP32 Agriculture</title>";
    webpage += "<meta http-equiv='refresh' content='5'>";
    webpage += "<style>body { font-family: Arial; text-align: center; }</style>";
    webpage += "</head><body>";
    webpage += "<h1>🌱 Smart Agriculture System</h1>";
    webpage += "<h3>📊 Sensor Readings</h3>";
    webpage += "<p>🌿 Soil Moisture 1: <b>" + String(moisture1) + "%</b></p>";
    webpage += "<p>🌿 Soil Moisture 2: <b>" + String(moisture2) + "%</b></p>";
    webpage += "<p>🌡️ Temperature: <b>" + String(temperature) + "°C</b></p>";
    webpage += "<p>💧 Humidity: <b>" + String(humidity) + "%</b></p>";
    webpage += "<h3>💡 Relay Status</h3>";
    webpage += "<p>🚰 Pump 1: <b>" + String(moisture1 < MOISTURE_THRESHOLD ? "ON" : "OFF") + "</b></p>";
    webpage += "<p>🚰 Pump 2: <b>" + String(moisture2 < MOISTURE_THRESHOLD ? "ON" : "OFF") + "</b></p>";
    webpage += "</body></html>";

    server.send(200, "text/html", webpage);
}

// 🚀 Setup Function
void setup() {
    Serial.begin(115200);

    // 🔹 Connect to WiFi
    WiFi.begin(ssid, password);
    Serial.print("Connecting to WiFi");
    while (WiFi.status() != WL_CONNECTED) {
        delay(1000);
        Serial.print(".");
    }
    Serial.println("\n✅ WiFi Connected!");
    Serial.print("📡 IP Address: ");
    Serial.println(WiFi.localIP());

    // 🔹 Start Web Server
    server.on("/", handleRoot);
    server.begin();
    Serial.println("✅ Web Server Started!");

    // 🔹 Connect to Blynk
    Blynk.begin(auth, ssid, password);
    Serial.println("✅ Connected to Blynk!");

    // 🔹 Initialize DHT Sensor
    dht.begin();

    // 🔹 Set Relay Pins as Output & Turn Off Initially
    pinMode(RELAY_1, OUTPUT);
    pinMode(RELAY_2, OUTPUT);
    digitalWrite(RELAY_1, HIGH);
    digitalWrite(RELAY_2, HIGH);

    // 🔹 Initialize LCD
    lcd.begin();          // Initialize 16x2 LCD
    lcd.setBacklight(1);       // Turn on backlight
    lcd.clear();               // Clear the display
    lcd.setCursor(0, 0);       // Set cursor to top left
    lcd.print("Smart Agriculture");  // Display initial text
}

// 🚀 Main Loop Function
void loop() {
    Blynk.run();  // Keep Blynk Connected
    server.handleClient();  // Handle Web Requests

    // 🔹 Read Moisture Levels
    moisture1 = analogRead(SOIL_SENSOR_1);
    moisture2 = analogRead(SOIL_SENSOR_2);
    moisture1 = map(moisture1, 4095, 0, 0, 100);
    moisture2 = map(moisture2, 4095, 0, 0, 100);

    // 🔹 Read Temperature & Humidity (Every 2 Seconds)
    temperature = dht.readTemperature();
    humidity = dht.readHumidity();

    // 🔹 Debugging Data
    Serial.print("Moisture 1: "); Serial.print(moisture1); Serial.print("% | ");
    Serial.print("Moisture 2: "); Serial.print(moisture2); Serial.print("% | ");
    Serial.print("Temp: "); Serial.print(temperature); Serial.print("°C | ");
    Serial.print("Humidity: "); Serial.print(humidity); Serial.println("%");

    // 🔹 Control Relays Based on Moisture Level
    digitalWrite(RELAY_1, moisture1 < MOISTURE_THRESHOLD ? LOW : HIGH);
    digitalWrite(RELAY_2, moisture2 < MOISTURE_THRESHOLD ? LOW : HIGH);

    // 🔹 Send Data to Blynk
    Blynk.virtualWrite(V11, moisture1);
    Blynk.virtualWrite(V12, moisture2);
    Blynk.virtualWrite(V13, temperature);
    Blynk.virtualWrite(V14, humidity);

    // 🔹 Update LCD Display
    lcd.clear();               // Clear previous data on LCD
    lcd.setCursor(0, 0);       // Move cursor to the top-left
    lcd.print("M1: " + String(moisture1) + "%"); // Display Moisture 1
    lcd.setCursor(0, 1);       // Move cursor to next line
    lcd.print("M2: " + String(moisture2) + "%"); // Display Moisture 2

    delay(2000);  // Delay before next reading
}

// 🚀 Manual Relay Control via Blynk App
BLYNK_WRITE(V15) {
    int relayState = param.asInt();
    digitalWrite(RELAY_1, relayState);
    Serial.print("🔴 Relay 1 Manual Control: ");
    Serial.println(relayState ? "ON" : "OFF");
}

BLYNK_WRITE(V16) {
    int relayState = param.asInt();
    digitalWrite(RELAY_2, relayState);
    Serial.print("🔴 Relay 2 Manual Control: ");
    Serial.println(relayState ? "ON" : "OFF");
}
