#include <SoftwareSerial.h>   // 引用程式庫
#include <Servo.h>
Servo myservo;


// 定義連接藍牙模組的序列埠
SoftwareSerial BT(8, 9); // 接收腳, 傳送腳
char val;  // 儲存接收資料的變數

void setup() {
  Serial.begin(9600);   // 與電腦序列埠連線
  Serial.println("BT is ready!");

  // 設定HC-05藍牙模組，AT命令模式的連線速率。
  BT.begin(9600);

  myservo.attach(A5, 400, 2400); // 修正伺服馬達脈衝寬度範圍
  //myservo.write(90); // 一開始先置中90度
  //delay(3000);
}

void loop() {
  // 若收到「序列埠監控視窗」的資料，則送到藍牙模組
  /* if (Serial.available()) {
    val = Serial.read();//要設定藍芽或測試時再開啟，沒事不要開
     BT.print(val);
  
  }  */

  // 若收到藍牙模組的資料，則送到「序列埠監控視窗」
  if (BT.available()) {
    val = BT.read();
    Serial.print(val);//設定指令時使用
   
    //提筆ｏｒ下筆
    if (val > 0)
    {
      switch (val)
      {
        case 49: // Press "1"提筆
          for (int i = 1200; i <= 1602; i += 3) { //數字大的是下筆
            myservo.write(i); // 直接以脈衝寬度控制
            delay(1);//速度
          }
          for (int i = 1602; i <= 1656; i += 3) { //數字大的是下筆
            myservo.write(i); // 直接以脈衝寬度控制
            delay(5);//速度
          }
          Serial.println("down");
          break;
        case 50:  //Press "2"下筆
          for (int i = 1656; i >= 1254; i -= 3) {
            myservo.write(i);
            delay(1);
          }
            for (int i = 1254; i >= 1200; i -= 3) {
            myservo.write(i);
            delay(5);
          }
          Serial.println("up");
          break;
      }
    }
  }
}
