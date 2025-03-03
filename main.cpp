/*
 * WebSocketClient.ino
 *
 *  Created on: 24.05.2015
 *
 */

#include <Arduino.h>

#include <WiFi.h>
#include <WiFiMulti.h>
#include <WiFiClientSecure.h>


#include <WebSocketsClient.h>
#include <Arduino_JSON.h>



WiFiMulti WiFiMulti;
WebSocketsClient webSocket;



#define USE_SERIAL Serial1

void hexdump(const void *mem, uint32_t len, uint8_t cols = 16) {
	const uint8_t* src = (const uint8_t*) mem;
	USE_SERIAL.printf("\n[HEXDUMP] Address: 0x%08X len: 0x%X (%d)", (ptrdiff_t)src, len, len);
	for(uint32_t i = 0; i < len; i++) {
		if(i % cols == 0) {
			USE_SERIAL.printf("\n[0x%08X] 0x%08X: ", (ptrdiff_t)src, i);
		}
		USE_SERIAL.printf("%02X ", *src);
		src++;
	}
	USE_SERIAL.printf("\n");
}

void getCommand(JSONVar command){
  if(command.hasOwnProperty("type")) {
    Serial.println("type = ");
    Serial.print(".");
    Serial.print((const char*)command["type"]);
    Serial.print(".");


  }
  String testtest = "target_position";
  if(testtest == (const char*)command["type"]) {
    Serial.println("target_position = ");
    Serial.print((int)command["x"]);
    Serial.print((int)command["y"]);


  }
}

void webSocketEvent(WStype_t type, uint8_t * payload, size_t length) {
  char newstring[length+1];
  for (int i = 0; i < length; i++) {
    newstring[i] = (char)payload[i];
  }
  JSONVar myObject = JSON.parse(newstring);
	switch(type) {
		case WStype_DISCONNECTED:
			Serial.println("[WSc] Disconnected!\n");
			break;
		case WStype_CONNECTED:
			Serial.println("[WSc] Connected to url: %s\n");

			// send message to server when Connected
			webSocket.sendTXT("{\"type\":\"connect\",\"fake\":false,\"robot_name\":\"MEGA RAT\"}");
			break;
		case WStype_TEXT:
			getCommand(myObject);



			// send message to server
			// webSocket.sendTXT("message here");
			break;
		case WStype_BIN:
			USE_SERIAL.printf("[WSc] get binary length: %u\n", length);
			hexdump(payload, length);

			// send data to server
			// webSocket.sendBIN(payload, length);
			break;
		case WStype_ERROR:			
		case WStype_FRAGMENT_TEXT_START:
		case WStype_FRAGMENT_BIN_START:
		case WStype_FRAGMENT:
		case WStype_FRAGMENT_FIN:
			break;
	}

}

void setup() {

	// USE_SERIAL.begin(921600);
	USE_SERIAL.begin(115200);
  Serial.begin(115200);
  Serial.println("Start");
	//Serial.setDebugOutput(true);
	USE_SERIAL.setDebugOutput(true);

	USE_SERIAL.println();
	USE_SERIAL.println();
	USE_SERIAL.println();

	for(uint8_t t = 4; t > 0; t--) {
		USE_SERIAL.printf("[SETUP] BOOT WAIT %d...\n", t);
		USE_SERIAL.flush();
		delay(1000);
	}

	WiFiMulti.addAP("Tesla IoT", "fsL6HgjN");

	//WiFi.disconnect();
	while(WiFiMulti.run() != WL_CONNECTED) {
		delay(100);
    Serial.print(".");

	}
  Serial.println("Connected to WiFi");
	// server address, port and URL
	webSocket.begin("145.137.121.173", 8001, "/");

	// event handler
	webSocket.onEvent(webSocketEvent);

	
	// try ever 5000 again if connection has failed
	webSocket.setReconnectInterval(5000);

}

void loop() {
	webSocket.loop();
}