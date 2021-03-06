#include <WiFi.h>
#include <HTTPClient.h>//para hacer peticiones http como un cliente
//#include <WiFiClient.h>
#include <WebServer.h>
#include <MFRC522.h>
#include <SPI.h>
//Librerias para telegram
#include <WiFiClientSecure.h>
#include <UniversalTelegramBot.h>
#include <ArduinoJson.h>

#define SS_PIN    SDA
#define RST_PIN   13
#define SIZE_BUFFER     18
#define MAX_SIZE_BLOCK  16
#define BOTtoken "1648938190:AAGZqh0WKrItje4kQgHIDnJ4ESfOvGGB8jU"  // your Bot Token (Get from Botfather)

const char* ssid = "SANTOSTOUR";
const char* password = "W24LPYFWatch";

//used in authentication
MFRC522::MIFARE_Key key;
//authentication return status code
MFRC522::StatusCode status;
// Defined pins to module RC522
MFRC522 mfrc522(SS_PIN, RST_PIN); 

// TCP server at port 80 will respond to HTTP requests
WebServer server(80);

WiFiClientSecure client;
UniversalTelegramBot bot(BOTtoken, client);
WiFiClientSecure client2;
UniversalTelegramBot bot2(BOTtoken, client2);

void readCard();
void telegram();
String GetBonus(String idchat);

TaskHandle_t task2;

void setup() {
  Serial.begin(115200);
  SPI.begin();//Init SPI bus
  mfrc522.PCD_Init();
  
  // Connect to WiFi network
  WiFi.begin(ssid, password);
  Serial.println("iniciando");

  // Wait for connection
  while (WiFi.status() != WL_CONNECTED) {
      delay(500);
      Serial.print(".");
  }

  Serial.println("");
  Serial.print("Connected to ");
  Serial.println(ssid);
  Serial.print("IP address: ");
  Serial.println(WiFi.localIP());

  xTaskCreatePinnedToCore(telegram,"telegram",10000,NULL,1,&task2,1);
  //se declaran las direcciones de servicio
  server.on("/",readCard);
  server.on("/telegram",SendTelegramPedido);
  server.on("/bonoreclamado",SendTelegramBono);
  
  // Start TCP (HTTP) server
  server.begin();
  Serial.println("HTTP server started");
  
  delay(100);
}

//reads data from card/tag
void readingData()
{
    if(mfrc522.PICC_IsNewCardPresent() && mfrc522.PICC_ReadCardSerial()){
      Serial.println("new card detected");
      
      mfrc522.PICC_DumpDetailsToSerial(&(mfrc522.uid));//prints the technical details of the card/tag
      mfrc522.PICC_HaltA();//instructs the PICC when in the ACTIVE state to go to a "STOP" state
      mfrc522.PCD_StopCrypto1();// "stop" the encryption of the PCD, it must be called after communication with authentication, otherwise new communications can not be initiated
    }

}

void readCard(){
  Serial.println("____________________");
  
  WiFiClient client = server.client();
  Serial.print("consulta realizada por ");
  Serial.print(client.localIP());
  Serial.print(":");
  Serial.println(client.localPort());
  
  //readingData();
  String data = "{\"id\": \"";
  // UID
  Serial.print("Card UID: ");
  if (mfrc522.uid.size == 0){
    data += "0";//significa que no hay ninguna
  }
  for (byte i = 0; i < mfrc522.uid.size; i++) {
    data += String(mfrc522.uid.uidByte[i],HEX);
    Serial.print(mfrc522.uid.uidByte[i],HEX);
  } 
  data +="\"}";
  Serial.println("");

  server.sendHeader("Access-Control-Allow-Headers","*");
  server.sendHeader("Access-Control-Allow-Origin","*");
  server.send(200, "json", data);

  Serial.println("____________________");
}
String GetBonus(String idchat){
   HTTPClient http;
   String str = "http://jsilva2021.pythonanywhere.com/bonus_by_tgm/"+idchat;
   http.begin(str);
   int httpResponseCode = http.GET();
   String response;
   if (httpResponseCode>0){
      Serial.print("HTTP response code: ");
      Serial.println(httpResponseCode);
      response = "";

      String json = http.getString();
      DynamicJsonDocument doc(2048);
      
      DeserializationError error = deserializeJson(doc,json);
      if (error){
        Serial.println("error serialization");
      }

      for(int i=0;i < doc.size(); i++){
        //Serial.println(obj[String(i)]);
        String emp = doc[i]["empresa"].as<String>();
        String puntos = doc[i]["puntos"].as<String>();
        response += "• ";
        response += String(emp);
        response += " ";
        response += String(puntos);
        response += " Puntos\n";
      }
   }

   http.end();
   return response;
}
void handleNewMessages(int numNewMessages) {//bot telegram
  Serial.print("handleNewMessages : ");
  Serial.println(String(numNewMessages));
  for (int i=0; i<numNewMessages; i++) {
    String chat_id = String(bot.messages[i].chat_id);//se obtiene el id del chat
    String text = bot.messages[i].text;//se obtiene el mensaje
    String from_name = bot.messages[i].from_name;//de quien viene el mensaje

    Serial.println(from_name);
    Serial.println(chat_id);
    Serial.println(text);

    if (text == "/bonus") {
      String bonos = GetBonus(chat_id);
      bot.sendMessage(chat_id, "Bonos Disponibles:\n"+bonos, "");
    }else{
      if (text == "/start")
      bot.sendMessage(chat_id,"Bienvenido "+from_name+" el servicio CardShop esta disponible");
      else
      bot.sendMessage(chat_id,"comando no disponible");
    }
    
  }
}

void telegram(void *pvParameters){
  for(;;){
    int numNewMessages = bot.getUpdates(bot.last_message_received + 1);
    while(numNewMessages) {
      Serial.println("got response");
      handleNewMessages(numNewMessages);
      numNewMessages = bot.getUpdates(bot.last_message_received + 1);
    }
  }
}

void SendTelegramPedido(){
  Serial.println("telegram de pedido listo enviado");
  //Serial.println(server.arg(0));
  String chat_id = server.arg(0);
  String str = "Su pedido esta listo";
  bot2.sendMessage(chat_id,str,"");
  server.sendHeader("Access-Control-Allow-Headers","*");
  server.sendHeader("Access-Control-Allow-Origin","*");
  server.send(200);
}
void SendTelegramBono(){
  String chat_id = server.arg(0);
  String empresa = server.arg(1);
  String point = server.arg(2);
  String str = "acaba de reclamar el bono de "+empresa+"\n Tienes Puntos: "+point;
  bot2.sendMessage(chat_id,str,"");
  server.sendHeader("Access-Control-Allow-Headers","*");
  server.sendHeader("Access-Control-Allow-Origin","*");
  server.send(200);
}

void loop() {
  readingData();//lee si hay una tarjeta disponible
  server.handleClient();//matiene el servidor http en escucha
  //telegram();  
}
