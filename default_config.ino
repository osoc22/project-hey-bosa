#include <PubSubClient.h>
#include <ESP8266WiFi.h>

#define BUTTON 13 //D7 -- the GPIO number of the pin you connect the wire to that is not the Ground (G/GND)
#define TIMEOUT_DEFAULT 10000 // default time-out value found by testing, increase for a longer delay before the signal is given that the user got off the button/pressure plate

bool calm_counter false; // Boolean used to check if the button/pressure plate has been pressed this cycle
int time_out_counter = 0; //the initialisation of the "timer"

const char* ssid     = "osoc22"; // the name of the WiFi network the microcontroller needs to connect to
const char* password = "osoc22osoc22"; // the password of the WiFi network the microcontroller needs to connect to

const char* mqtt_server = "192.168.137.1"; // the IP address of the MQTT server - in this case it is installed on the Network Host device
const char* topic_pub = "hermes/button/start"; // MQTT Topic 1 to publish to
const char* topic_sub = "hermes/button/stop"; // MQTT Topic 2 to publish to

WiFiClient espClient;
PubSubClient client(espClient); //the creation of the WiFi and MQTT Client object.

void setup() {
  Serial.begin(115200); //initialisation of the serial monitor (USB text OUT for debugging)
  pinMode(BUTTON, INPUT_PULLUP); // initialisation of the pin the button is connected to

  WiFi.begin(ssid, password); // starting up the WiFi connection using the known network name and password.
  Serial.println("Connecting"); 
  while (WiFi.status() != WL_CONNECTED) { //whilst not connected to the WiFi network, try again
    delay(500);
    Serial.print(".");
  }
  client.setServer(mqtt_server, 1883); // set the server and port of the MQTT network for the client.
  connect(); // connect to the MQTT server - or return the error code (look up online for error code legend)
}

void connect() { // connect to the MQTT server - or return the error code (look up online for error code legend). The Error code is printed on teh Serial Monitor.
  Serial.println("Connecting to MQTT...");
  if (client.connect("JEFF")) {
    Serial.println("connected");
  } else {
    Serial.print("failed with state ");
    Serial.print(client.state());
    delay(2000);
  }
}

void loop() {
  while (!client.connected()) { // Whilst not connected to the MQTT client, try to connect!
    connect();
  }
  client.loop(); // check if any new MQTT messages have been sent to you (remainder from when the ESP8266 was both a publisher and subscriber)
  while (calm_counter) { // when the button has been pressed and is held, enter this while-loop -- this loop exists due to problems with button connection (not a perfectly stable 1 or 0)
    while (!client.connected()) { // zolang ik niet geconnecteerd ben met MQTT, probeer het opnieuw en zodra ik geconnecteerd ben
      connect();
    }
    client.loop();
    if (digitalRead(BUTTON) == LOW) { //whilst the button is held down 
      time_out_counter = TIMEOUT_DEFAULT; //reset the timer, nullifying the count-down until the shutdown MQTT message 
    } else { // if the button is not held down
      time_out_counter -= 1; // decrement the timer, starting the count-down until the button gives the shutdown signal
    if (time_out_counter == 0) { // when the button has not been held for some time
      calm_counter = false; // tell the system the button is no longer held down
      client.publish(topic_sub, "DEPRESSED"); // tell the entire MQTT network the button is no longer held down (the user is gone)
    }
    }
  }

  if (digitalRead(BUTTON) == LOW && calm_counter == 0 && time_out_counter == 0) { // if the button has been reset/just started and is then pressed
    calm_counter = true; // tell the system your button has been pressed
    client.publish(topic_pub, "PRESSED"); // tell the entire MQTT network the button has been pressed
    time_out_counter = TIMEOUT_DEFAULT; // start the timer.
  }
}
