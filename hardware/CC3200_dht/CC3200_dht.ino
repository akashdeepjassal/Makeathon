#ifndef __CC3200R1M1RGC__
// Do not include SPI for CC3200 LaunchPad
//https://github.com/MORA99/Stokerbot/tree/master/Libraries/dht
#include <SPI.h>
#endif
#include <WiFi.h>
#include <dht.h>
// your network name also called SSID
char ssid[] = "Nokia 8";
// your network password
char password[] = "hello123";
// if you don't want to use DNS (and reduce your sketch size)
// use the numeric IP instead of the name for the server:
//IPAddress server(50,62,217,1);  // numeric IP for Google (no DNS)
char server[] = "ps-makeathon.herokuapp.com";    // name address for Google (using DNS)
// Initialize the Ethernet client library
// with the IP address and port of the server
// that you want to connect to (port 80 is default for HTTP):
WiFiClient client;
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
float temperature, humidity;
void setup() {
  //Initialize serial and wait for port to open:
  Serial.begin(115200);
  // attempt to connect to Wifi network:
  Serial.print("Attempting to connect to Network named: ");
  // print the network name (SSID);
  Serial.println(ssid); 
  // Connect to WPA/WPA2 network. Change this line if using open or WEP network:
  WiFi.begin(ssid, password);
  while ( WiFi.status() != WL_CONNECTED) {
    // print dots while we wait to connect
    Serial.print(".");
    delay(300);
  }
  Serial.println("\nYou're connected to the network");
  Serial.println("Waiting for an ip address");
  
  while (WiFi.localIP() == INADDR_NONE) {
    // print dots while we wait for an ip addresss
    Serial.print(".");
    delay(300);
  }
  Serial.println("\nIP Address obtained");
  printWifiStatus();
  
  
  
}
void loop() {
  // if there are incoming bytes available
  // from the server, read them and print them:

  if (client.connect(server, 80)) {
    Serial.println("connected to server");
    // Make a HTTP request:
    if (dht::readFloatData(10, &temperature, &humidity, false) == 0)
    {
      Serial.print("T: ");
      Serial.print(temperature);
      Serial.print(" H: ");
      Serial.println(humidity);    
      Serial.println(String(temperature));
    }
//    char buffer[19];
//    sprintf(buffer, "%.2f", temperature);
//    Serial.println(buffer);
    
    client.println("GET /v1/test?data=Happy%20Happy%20Data%201234 HTTP/1.1");
    //String(temperature)+"HTTP/1.1");
//Happy_Happy_Data_1234 HTTP/1.1");
    client.println("Host: ps-makeathon.herokuapp.com");
    client.println("Connection: close");
    client.println();
  }
   
  w1hile (client.available()) {
    char c = client.read();
    Serial.print("\r");
    Serial.write(c);
    Serial.print("\nStarting connection to server...");
  // if you get a connection, report back via serial:
  
  }
   if (!client.connected()) {
    //Serial.println();
    Serial.println("disconnecting from server.");
    client.stop();
    // do nothing forevermore:
 //   while (true); 
}
}
