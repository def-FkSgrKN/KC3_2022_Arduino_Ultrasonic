import pygame #ゲームを作るためのライブラリ
import random #乱数を生成するためのライブラリ
import SerialUltrasonic #超音波センサからのシリアル通信の取得


#クラス(同じものを複製できるプログラムの鋳型のようなもの)
#中に関数や変数を書き込むことができる。プログラムの基本的な単位

#Entity(ゲームの中で動き回るもの)のクラス キャラクタともいう
#ex) プレイヤ、敵、アイテムなど
class Entity(pygame.sprite.Sprite):
    #クラスの初期化、クラスの中で使える変数をそれぞれ初期化する。
    def __init__(self, image, x, y): #image、x、yは、self.image、self.x、self.yというように取得できる。
        self.image = pygame.image.load(image) #画像の読み込み
        self.rect = self.image.get_rect() #画像の直方体
        self.rect.center = (x, y) #キャラクタの座標
        
    #更新するための関数 ここでは、passとなり何もしない。
    def update(self):
        pass

    #画面にキャラクタの画像を画面に描画する
    def draw(self, screen):
        screen.blit(self.image, self.rect)
    
    #当たり判定のためにキャラ自身の直方体を取得する
    def getRect(self):
        return self.rect

#プレイヤのクラスは、キャラクタのクラスの子クラス
#共通する部分を親クラスとし、異なる部分を子クラスとして作るときれいに記述できる。
class Player(Entity):
    def __init__(self, image, x, y):
        super().__init__(image, x, y) #親クラスを継承し、新たにupdate関数の内容が上書きされている。

    #更新するための関数が改変された。
    def update(self, data):

        value = 0 #超音波から取得した距離の値を保持する変数
        
        #3回文の距離を平均化することで、動作を滑らかにしている。
        for i in range(3):
            temp = data.get_data() #データを一時的に保持し、
            if temp != '':         #それが何もないデータでないことを確認してから、
                value += float(temp) #加算する。
        
        value /= 3 #3で割ることで平均値を計算
        #print(value)

       
        #「何もない」ではない　かつ　「100」でない　かつ　「30」以下であるとき
        if value != '' and value != '100' and value <= 30:

            # Player犬のy座標　が　超音波センサと手との距離をゲームのスケールに変換した値　よりも　大きいなら、　
            if self.rect.center[1] > int(480 / 30 * (30 - float(value))):

                #上記の条件を満たす場合、Player犬のy座標を-5ずつ動かす。
                while self.rect.center[1] > int(480 / 30 * (30 - float(value))):
                    self.rect = self.rect.move(0, -5)

            #上記以外の場合、
            # Player犬のy座標　が　超音波センサと手との距離をゲームのスケールに変換した値　よりも　小さいか、等しいなら
            else:

                #上記の条件を満たす場合、Player犬のy座標を5ずつ動かす。
                while self.rect.center[1] + 20 < int(480 / 30 * (30 - float(value))):
                    self.rect = self.rect.move(0, 5)

#敵のクラス
class Enemy(Entity):
    def __init__(self, image, x, y):
        super().__init__(image, x, y) #クラスの中で使える変数に「xspeed」とその内容の表示を追加(上書き)
        self.xspeed = random.randint(-10, -5)
        print(self.xspeed)

    #更新するための関数を改変(上書き)
    def update(self):
        self.rect = pygame.Rect.move(self.rect, self.xspeed, 0)

        #敵のx座標が0よりも小さいとき
        if self.rect.x < 0:
            self.rect.x = 640 #敵のx座標を640にする
            #self.rect.y = random.randint(0, 480) #敵のy座標を0から480までの整数の乱数の何れかの値にする。
            self.rect.y = random.randint(64, 416) #敵のy座標を64から416までの整数の乱数の何れかの値にする。(改変)


#main関数では、ゲーム全体の動きを司る。
def main():
    #--- ゲームの初めの設定部分(初めに1回だけ実行される) ---
    pygame.init() #pygameの初期化
    pygame.display.set_caption("Window name here") #表示の設定
    screen = pygame.display.set_mode((640, 480)) #ゲームの画面を横640×縦480で生成する。
    clock = pygame.time.Clock() #時間
    running = True #ゲームが動いている。
    data = SerialUltrasonic.GetData() #dataの実体化 鋳型(クラス)なので複製を作るときは、鋳物(インスタンス)を作る。
                                    #これをクラスの実体化または、インスタンス化という。
                                    #超音波センサからの距離

    background = Entity("images/background.png", 320, 240) #Entityクラスのインスタンス化
    player = Player("images/player.png", 100, 240) #Playerクラスのインスタンス化
    enemy = Enemy("images/enemy.png", 540, random.randint(0, 480)) #Enemyクラスのインスタンス化

    
    #--- ゲームの繰り返される部分 ---
    #ゲームが動いている間
    while running: 

        for event in pygame.event.get(): 
            if event.type == pygame.QUIT:
                running = False

        player.update(data) #プレイヤを更新するために必要な「距離のデータ」を更新するために渡す
        enemy.update() #敵を更新する

        #プレイヤと敵との間の当たり判定を確かめる。
        collision = pygame.Rect.colliderect(player.getRect(), enemy.getRect())

        #当たり判定が「真」であるときにゲームを終了する。
        if collision:
            running = False
        
        # screen.fill((0, 0, 0))
        background.draw(screen) #背景を描画する
        player.draw(screen) #プレイヤを描画する
        enemy.draw(screen) #敵を描画する
        
        pygame.display.flip() #画面を次の画面に切り替える(ゲームの画面がアニメのように絵を1枚めくるようなイメージ)
        clock.tick(60) #pygameの1秒あたりに実行するwhile文の繰り返しの数 ここでは、1秒間に60回となっている。
        
    #ゲームのループを抜けるとゲームを終了する。
    pygame.quit()


#このファイルを直接実行した場合は、ここ以下の部分がまず一番初めに動く。
if __name__ == "__main__":
    main()


