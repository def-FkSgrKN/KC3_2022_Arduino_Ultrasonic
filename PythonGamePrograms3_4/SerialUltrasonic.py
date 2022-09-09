#takuのアトリエ, Arduino→Python(PC)間シリアル通信でstr,float型のデータを受信してみた, 
#https://taku-info.com/arduinotopython_serialdata/, 2022年6月13日.

import serial

#シリアル通信のクラス
class GetData(object):

    #クラスの初期化でシリアルポートを開く
    def __init__(self):
        self.port = 'COM4'   #usbポートをArduinoに揃える
        self.baudrate = 9600 #1秒間に受信するデータ量[byte]をArduinoに揃える
        print("Open Port") 
        #シリアル通信のポートを開く。
        self.ser = serial.Serial(self.port, self.baudrate, timeout=1)

    #シリアル通信でデータを取得する関数
    def get_data(self):
        value = self.ser.readline() #受信した1行分のデータ全体を読み取る。
        value = value.decode() #\r\nといった文章の改行コードの文字を除く
        value = value.rstrip() #引数の中の文字を除去する。省略するとスペースを除去
        return value           #整えられた文字列をデータとして返す。                        

    #ポートを閉じる関数
    def ser_close(self):
        print("Close Port")
        self.ser.close() #ポートを閉じる
        
if __name__ == '__main__':
    data = GetData()
    while True:
        try:
            value = data.get_data()
            print("Value:" + value)
            print(type(value))
        except KeyboardInterrupt:
            data.ser_close()
            break