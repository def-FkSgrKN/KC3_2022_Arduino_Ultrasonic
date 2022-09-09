double Duration = 0; //受信した間隔
double Distance = 0; //距離
int echoPin = 2;
int trigPin = 3;
void setup() {
Serial.begin( 9600 );
//Serial.begin(4800);
pinMode( echoPin, INPUT );
pinMode( trigPin, OUTPUT );
}
void loop() {
  digitalWrite(trigPin, LOW); 
  delayMicroseconds(2); 
  digitalWrite( trigPin, HIGH ); //超音波を出力
  delayMicroseconds( 10 ); //
  digitalWrite( trigPin, LOW );
  Duration = pulseIn( echoPin, HIGH ); //センサからの入力
  if (Duration > 0) {
    Duration = Duration/2; //往復距離を半分にする
    Distance = Duration*340*100/1000000; // 音速を340m/sに設定
    
    if (Distance <= 30) {
       Serial.println(Distance);
       analogWrite(11, int(255 - Distance * 255 / 50));
    }
    else {
       Serial.println(100);
       analogWrite(11, 0);
    }

    //delay(10); 
       
  }
}
