#ifndef __CC3200R1M1RGC__
#include <SPI.h>
#endif
#include <WiFi.h>

void printFloat(float value, int places);
// START: WiFi settings
char SSID[] = "Nokia 8";
char PASSWORD[] = "hello123";
char* HOST="ps-makeathon.herokuapp.com";
String dataToSend; //String variable which will be containing the JSON data to send
WiFiClient client;
boolean isConnectedToIoTHub = false;
void printWifiStatus() {
  // print the SSID of the network you're attached to:
  Serial.print("SSID: ");
  Serial.println(WiFi.SSID());

  // print your WiFi shield's IP address:
  IPAddress ip = WiFi.localIP();
  Serial.print("IP Address: ");
  Serial.println(ip);

  // print the received signal strength:
  long rssi = WiFi.RSSI();
  Serial.print("signal strength (RSSI):");
  Serial.print(rssi);
  Serial.println(" dBm");
}
void setup() {
    Serial.begin(115200);
  Serial.print("\nInitializing TMP006 sensor ...  ");
  
  Serial.println("OK");
   Serial.print("Attempting to connect to Network named: ");
    Serial.println(SSID);
    WiFi.begin(SSID, PASSWORD);
    while ( WiFi.status() != WL_CONNECTED) {
      Serial.print(".");
      delay(300);
  }
  Serial.println("\nYou're connected to the network");
  Serial.println("Waiting for an ip address");
  
  while (WiFi.localIP() == INADDR_NONE) {
    Serial.print(".");
    delay(300);
  }

  Serial.println("\nIP Address obtained");
  printWifiStatus();

  Serial.println("\nStarting connection to IoT Hub...");
  isConnectedToIoTHub = client.sslConnect(HOST, 443);

  while(!isConnectedToIoTHub){    
    Serial.print(".");
    delay(300);
  }
  
  Serial.println("Setup is finished ...");
}
const char* IOT_HUB_END_POINT = "v1/test/?test_data=";
//char* DEVICE_ID="Jassal ka ITO Device/";
char* path = "/v1/test";
char* query = "?test_data=Happy Happy Data";
char* KEY;
void loop() {
  float diet = 3.14;
  Serial.print("Die Temperature: "); Serial.print(diet); Serial.println("*C");  
  char outstr[15]; //buffer to use in float to char array conversion
  dtostrf(diet,4, 1, outstr);  
  dataToSend = "{temperature: '" + (String)outstr + "'}";
  Serial.println("Sending data to Azure IoT Hub...");
  
  if (isConnectedToIoTHub) {
    String request = String("POST ")  + (String)path + (String)query +"\r\r"+ " HTTP/1.1\r\n" +
                     "Host: ps-makeathon.herokuapp.com \r\n" +
                     "Connection: keep-alive\r\n"+ 
                     "User-Agent: Texas Board" ;                  
    /*String request = String("GET ") +
                     "Host: " + HOST + "\r"+ 
                     "/v1/test?test_data=" +
                     dataToSend;
                     */
    client.print(request);

    String response = "";
    while (client.connected()) {      
      response += client.readStringUntil('}');
    }  
    Serial.println();
    Serial.print("Response code: ");
    Serial.println(response.substring(9, 12));
    Serial.println(response);
    Serial.println("END");
  }
   
  delay(10000);
}
