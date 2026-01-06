"""one line adventure game"""

import time

class GameObject:
    pass

class gamevals:

    def __init__(self):
        self.gameflag=True
        self.cmdflag1=False
        self.cmdflag2=False
        self.sc=sc_start()
        self.flag={
            "can":"hidden",
            "juice":"nothing",
            "door_bldg":"locked",
            "stepladder":"drop",
            "crowbar":"drop",
            "coin":"hidden",
            "door_storeroom":"locked",
            "ceiling":"hidden",
            "hatch":"hidden",
            "key":"hidden",
            "rope":"drop",
            "bucket":"drop",
            "mop":"drop",
            "board":"fixed",
            "glass":"drop",
            "grate":"fixed",
            "ring":"hidden"
        }

class scene:

    def initmsg(self, gv):
        pass

    def cmdexe(self, cmd, gv):
        pass

    def cmd_common(self, cmd, gv):
        gv.cmdflag1=True
        if cmd=="help":
            printw("この町のどこかにあるエメラルドの指輪を探してください。")
            printw("コマンドは［動詞］、［移動方向］、［動詞＋名詞］")
            printw("look, forward, get key など")
            printw("look で周囲の状況がわかります。")
            printw("look xxx でオブジェクトに対するヒントが出ます。")
            printw("オブジェクト（棚など）を詳しく調査したい場合は")
            printw("search xxx と入力してください。")
            printw("使用可能な動詞：")            
            printw("forward, back, up, down, exter, exit (移動)")
            printw("look, search, inventory(持ち物を調べる),")
            printw("open, get, use, put, set, buy, insert, break,")
            printw("move, turn, ride, climb, dig, type, push, remove,")
            printw("tie, pull, clean, wash")
        elif cmd=="inventory" or cmd=="i":
            have=False
            if gv.flag["coin"]=="get":
                printw("コイン（coin）、")
                have=True
            if gv.flag["can"]=="get":
                printw("缶（can）、")
                have=True
            if gv.flag["stepladder"]=="get":
                printw("脚立（stepladder）、")
                have=True
            if gv.flag["crowbar"]=="get":
                printw("バール（crowbar）、")
                have=True
            if gv.flag["key"]=="get":
                printw("鍵（key）、")
                have=True
            if gv.flag["rope"]=="get":
                printw("ロープ（rope）、")
                have=True
            if gv.flag["bucket"]=="get":
                printw("バケツ（bucket）、")
                have=True
            if gv.flag["mop"]=="get":
                printw("モップ（mop）、")
                have=True
            if gv.flag["glass"]=="get":
                printw("ガラスの破片（glass）、")
            if have:
                printw("を持っています。")
            else:
                printw("何も持っていません。")
        elif cmd=="look can":
             if gv.flag["can"]=="get":
                 if gv.flag["juice"]=="mint":
                     printw("ミントではなくヒントでした。")
                     printw("[番号は147]")
                 elif gv.flag["juice"]=="orange":
                     printw("オレンジジュースの缶です。")
                 elif gv.flag["juice"]=="cola":
                     printw("コーラの缶です。")
             else:
                 printw("あなたは持っていません。")
        elif cmd=="look stepladder":
            if gv.flag["stepladder"]=="get":
                printw("立てると１メートルくらいになります。")
            else:
                printw("あなたは持っていません。")
        elif cmd=="look crowbar":
            if gv.flag["crowbar"]=="get":
                printw("なにかを引き剥がしたり釘を抜くのに使います。")
            else:
                printw("あなたは持っていません。")
        elif cmd=="drink can" or cmd=="drink orange" or cmd=="drink cola" or cmd=="drink mint" or cmd=="drink juice":
            if gv.flag["can"]=="get":
                printw("缶の中身を飲みました。")
        elif cmd=="f":
            cmd="forward"
        elif cmd=="b":
            cmd="back"
        elif cmd=="u":
            cmd="up"
        elif cmd=="d":
            cmd="down"
        elif cmd=="north" or cmd=="east" or cmd=="west" or cmd=="south" or cmd=="n" or cmd=="s" or cmd=="w" or cmd=="e" or cmd=="right" or cmd=="left" or cmd=="r" or cmd=="l":
            printw("このゲームで移動可能な方向：")
            printw("forward, back, up, down, enter, exit")
            printw("省略形で f, b, u, d でも移動可能です。")
        else:
            gv.cmdflag1=False
        gv.cmdflag2=True
        gv=gv.sc.cmdexe(cmd, gv)
        if gv.cmdflag1==False and gv.cmdflag2==False:
            printw("それはできません。")
        return gv

class sc_start(scene):

    def initmsg(self, gv):
        printw("スタート：あなたは道にいます。")

    def cmdexe(self, cmd, gv):
        if cmd=="look":
            printw("自動販売機（vender）があります。")
        elif cmd=="look vender":
            printw("オレンジジュース（orange）、コーラ（cola）、ミント（mint）を売っています。")
            printw("コインの投入口があります。")
        elif cmd=="insert coin":
            if gv.flag["coin"]=="get":
                printw("何を買うのですか？")
            else:
                printw("あなたは持っていません。")
        elif cmd=="buy orange":
            if gv.flag["coin"]=="get":
                printw("オレンジジュースを買いました！")
                gv.flag["can"]="get"
                gv.flag["juice"]="orange"
                gv.flag["coin"]="used"
            else:
                printw("あなたはコインを持っていません。")
        elif cmd=="buy cola":
            if gv.flag["coin"]=="get":
                printw("コーラを買いました！")
                gv.flag["can"]="get"
                gv.flag["juice"]="cola"
                gv.flag["coin"]="used"
            else:
                printw("あなたはコインを持っていません。")
        elif cmd=="buy mint":
            if gv.flag["coin"]=="get":
                printw("ミントの缶を買いました！")
                gv.flag["can"]="get"
                gv.flag["juice"]="mint"
                gv.flag["coin"]="used"
            else:
                printw("あなたはコインを持っていません。")
        elif cmd=="put stepladder":
            printw("なんのために置くのですか？")
        elif cmd=="forward":
            printw("前に進みます。")
            gv.sc=sc_underconstruction()
        elif cmd=="back":
            printw("そちらには進めません。")
        else:
            gv.cmdflag2=False
        return gv

class sc_underconstruction(scene):

    def initmsg(self, gv):
        printw("あなたは工事現場にいます。")

    def cmdexe(self, cmd, gv):
         if cmd=="look":
             printw("建物（building）があります。")
             printw("番号式のロック（keypad）があります。")
         elif cmd=="enter building" or cmd=="enter":
             if gv.flag["door_bldg"]=="open":
                 printw("ビルのなかに入りました。")
                 gv.sc=sc_building()
             else:
                 printw("入口が閉まっています。")
         elif cmd=="look building":
             printw("ガラスのドア（door）があります。")
         elif cmd=="look keypad":
             printw("数字が並んでいます。")
         elif cmd=="look door":
             printw("キーロック式のドアです。")
         elif cmd=="147" or cmd=="push 147" or cmd=="type 147":
             printw("ドアのロックが解除されました!")
             gv.flag["door_bldg"]="open"
         elif cmd=="put stepladder":
             printw("なんのために置くのですか？")
         elif cmd=="forward":
             printw("前に進みます。")
             gv.sc=sc_park()
         elif cmd=="back":
             printw("後ろにもどります。")
             gv.sc=sc_start()
         else:
             gv.cmdflag2=False
         return gv

class sc_building(scene):

    def initmsg(self, gv):
        print("あなたは工事現場の建物のなかにいます。")

    def cmdexe(self, cmd, gv):
        if cmd=="look":
            printw("木材（wood）があります。")
            if gv.flag["stepladder"]=="drop":
                printw("脚立（stepladder）があります。")
            if gv.flag["crowbar"]=="drop":
                printw("バール（crowbar）があります。") 
        elif cmd=="look wood":
            printw("細長い建築用の木材です。")
        elif cmd=="get stepladder":
            if gv.flag["stepladder"]=="drop":
                printw("脚立を取りました！")
                gv.flag["stepladder"]="get"
            elif gv.flag["stepladder"]=="get":
                printw("すでに持っています。")
            else:
                printw("ここにはありません。")
        elif cmd=="get crowbar":
            if gv.flag["crowbar"]=="drop":
                printw("バールを取りました！")
                gv.flag["crowbar"]="get"
            elif gv.flag["crowbar"]=="get":
                printw("すでに持っています。")
        elif cmd=="get wood":
            printw("持ちはこぶのは大変そうです。")
        elif cmd=="put stepladder":
            printw("なんのために置くのですか？")
        elif cmd=="forward":
            printw("そちらには進めません。")
        elif cmd=="back" or cmd=="exit" or cmd=="exit building":
            printw("工事現場にもどります。")
            gv.sc=sc_underconstruction()
        else:
            gv.cmdflag2=False
        return gv

class sc_park(scene):

    def initmsg(self, gv):
        printw("あなたは公園にいます。")

    def cmdexe(self, cmd, gv):
        if cmd=="look":
            printw("ブランコ（swing）があります。")
            printw("砂場（sandbox）があります。")
            printw("トイレ（washroom）があります。")
            printw("公園の奥に柵（fence）があります")
            if gv.flag["coin"]=="appear":
                printw("コイン（coin）があります。")
            if gv.flag["stepladder"]=="park":
                printw("脚立（stepladder）が置いてあります。")
        elif cmd=="play swing" or cmd=="ride swing":
            printw("子供のころにもどってブランコで遊びました。")
            printw("しばらくすると飽きたのでブランコから降りました。")
        elif cmd=="look fence":
            printw("柵の向こう側の下のほうに川(river)が流れているのが見えます。")
        elif cmd=="up":
            printw("どこに登るのですか？")
        elif cmd=="ride fence" or cmd=="climb fence":
            if gv.flag["stepladder"]!="park":
                printw("高すぎて登れません。")
            else:
                printw("あなたは脚立を使って柵を登ろうとしました。")
                printw("ところが、柵の向こう側は断崖になっていて降りる場所がありません。")
                printw("あなたは脚立から降りました。")
        elif cmd=="put stepladder":
            if gv.flag["stepladder"]=="get":
                printw("柵の近くに脚立を置きました。")
                gv.flag["stepladder"]="park"
        elif cmd=="get stepladder":
            if gv.flag["stepladder"]=="park":
                printw("脚立を取りました。")
                gv.flag["stepladder"]=="get"
            elif gv.flag["stepladder"]=="get":
                printw("すでに持っています。")
            else:
                printw("ここにはありません。")
        elif cmd=="look river":
            printw("おや？　川原にきらきらしたものが落ちています。")
        elif cmd=="dig sandbox":
            if gv.flag["coin"]=="hidden":
                printw("コイン（coin）がありました。")
                gv.flag["coin"]="appear"
            else:
                printw("ほかには何も見当たりません。")
        elif cmd=="get coin" and gv.flag["coin"]=="appear":
            print("コインを取りました！")
            gv.flag["coin"]="get"
        elif cmd=="enter" or cmd=="enter washroom" or cmd=="enter toilet" or cmd=="enter rest room" or cmd=="enter restroom":
            print("公園のトイレに入ります。")
            gv.sc=sc_toilet()
        elif cmd=="forward":
            printw("前に進みます。")
            gv.sc=sc_bridge()
        elif cmd=="back":
            printw("後ろにもどります。")
            gv.sc=sc_underconstruction()
        else:
            gv.cmdflag2=False
        return gv

class sc_toilet(scene):

    def initmsg(self, gv):
        printw("あなたは公園のトイレにいます。")

    def cmdexe(self, cmd, gv):
        if cmd=="look":
            printw("用具入れ（storeroom）があります。")
            printw("用具入れのドア（door）があります。")
            printw("電灯（light）があります。")
            if gv.flag["stepladder"]=="toilet":
                printw("脚立（stepladder）があります。")
            if gv.flag["hatch"]=="appear":
                printw("天井についているふた（hatch）があります。")
        elif cmd=="look light":
            printw("ちかちか点滅しています。")
        elif cmd=="put stepladder" or cmd=="drop stepladder":
            printw("床に脚立を置きました。")
            gv.flag["stepladder"]="toilet"
        elif cmd=="up" or cmd=="ride stepladder" or cmd=="climb stepladder":
            if gv.flag["stepladder"]=="toilet":
                printw("脚立に乗りました。")
                gv.sc=sc_stepladder()
            else:
                printw("どこにものぼれそうなところはありません。")
        elif cmd=="get stepladder":
            if gv.flag["stepladder"]=="toilet":
                printw("脚立を取りました！")
                gv.flag["stepladder"]="get"
            elif gv.flag["stepladder"]=="get":
                printw("すでに持っています。")
            else:
                printw("ここにはありません。")
        elif cmd=="get light" or cmd=="search light" or cmd=="get light":
            printw("天井の高いところにあるのでとどきません。")
        elif cmd=="put rope" or cmd=="tie rope" or cmd=="set rope" or cmd=="use rope":
            printw("どこに結ぶのですか？")
        elif cmd=="clean" or cmd=="clean up" or cmd=="clean up floor" or cmd=="clean up toilet" or cmd=="clean up washroom" or cmd=="clean washroom":
            if gv.flag["mop"]=="get":
                printw("水がないのでモップで床をからぶきします。")
                printw("すこしはきれいになったかな？")
            else:
                printw("道具を持っていません。")
        elif cmd=="enter" or cmd=="enter door" or cmd=="enter storeroom":
            if gv.flag["door_storeroom"]=="open":
                printw("用具入れのなかに入ります。")
                gv.sc=sc_storeroom()
            else:
                printw("鍵がかかっています。")
        elif cmd=="open door":
            if gv.flag["door_storeroom"]=="locked":
                if gv.flag["key"]=="get":
                    printw("ドアが開きました！")
                    gv.flag["door_storeroom"]="open"
        elif cmd=="back" or cmd=="exit" or cmd=="exit toilet" or cmd=="exit washroom" or cmd=="exit restroom" or cmd=="exit rest room":
            printw("公園にもどります。")
            gv.sc=sc_park()
        elif cmd=="forward":
            printw("その方向には行けません。")
        else:
            gv.cmdflag2=False
        return gv

class sc_stepladder(scene):

    def initmsg(self, gv):
         printw("あなたは公園のトイレで脚立のうえに立っています。")

    def cmdexe(self, cmd, gv):
        if cmd=="look":
            printw("電灯（light）が見えます。")
            if gv.flag["ceiling"]=="appear":
                printw("天井（ceiling）が見えます。")
            if gv.flag["hatch"]=="appear":
                printw("天井にふた（hatch）がついています。")
            if gv.flag["key"]=="appear":
                printw("鍵（key）があります。")
        elif cmd=="look light":
            printw("天井（ceiling）に備え付けられています。")
            gv.flag["ceiling"]="appear"
        elif cmd=="look ceiling":
             printw("なにかありそうです。")
        elif cmd=="search ceiling":
            print("天井に開けられそうなふた（hatch）がついていました。")
            gv.flag["hatch"]="appear"
        elif cmd=="look hatch":
            if gv.flag["hatch"]=="appear":
                printw("かんたんに開きそうです。")
            elif gv.flag["hatch"]=="open":
                printw("開いています。")
            else:
                printw("ここには見当たりません。")
        elif cmd=="open hatch":
            if gv.flag["hatch"]=="appear":
                printw("ふたが開きました！")
                gv.flag["hatch"]="open"
            elif gv.flag["hatch"]=="open":
                printw("すでに開いています。")
            else:
                printw("それはどこにあるのですか？")
        elif cmd=="search hatch":
            if gv.flag["hatch"]=="open":
                if gv.flag["key"]=="hidden":
                    printw("鍵（key）がありました！")
                    gv.flag["key"]="appear"
                else:
                    printw("ほかにはなにもありません。")
            elif gv.flag["hatch"]=="appear":
                printw("ふたを開けてください。")
            else:
                printw("それはどこにあるのですか？")
        elif cmd=="get key":
            if gv.flag["key"]=="appear":
                printw("鍵を取りました！")
                gv.flag["key"]="get"
            elif gv.flag["key"]=="hidden":
                printw("それはどこにあるのですか？")
            else:
                printw("すでに持っています。")
        elif cmd=="get stepladder":
            printw("あぶないですよ？")
        elif cmd=="down" or cmd=="get off" or cmd=="exit" or cmd=="get off stepladder" or cmd=="jump":
            printw("脚立を降ります。")
            gv.sc=sc_toilet()
        elif cmd=="forward" or cmd=="back":
            printw("脚立を降りないと動けません。")
        else:
            gv.cmdflag2=False
        return gv

class sc_storeroom(scene):

    def initmsg(self, gv):
        printw("あなたは公園のトイレの用具入れのなかにいます。")

    def cmdexe(self, cmd, gv):
        if cmd=="look":
            have=False
            if gv.flag["rope"]=="drop":
                printw("ロープ（rope）があります。")
                have=True
            if gv.flag["bucket"]=="drop":
                printw("バケツ（bucket）があります。")
                have=True
            if gv.flag["mop"]=="drop":
                printw("モップ（mop）があります。")
                have=True
            if have==False:
                printw("なにもありません。")
        elif cmd=="get rope":
            if gv.flag["rope"]=="drop":
                printw("ロープを取りました！")
                gv.flag["rope"]="get"
            elif gv.flag["rope"]=="get":
                printw("すでに持っています。")
            else:
                printw("ここにはありません。")
        elif cmd=="get bucket":
            if gv.flag["bucket"]=="drop":
                printw("バケツを取りました！")
                gv.flag["bucket"]="get"
            elif gv.flag["bucket"]=="get":
                printw("すでに持っています。")
            else:
                printw("ここにはありません。")
        elif cmd=="get mop":
            if gv.flag["mop"]=="drop":
                printw("モップを取りました！")
                gv.flag["mop"]="get"
            elif gv.flag["mop"]=="get":
                printw("すでに持っています。")
            else:
                printw("ここにはありません。")
        elif cmd=="put stepladder":
            printw("なんのために置くのですか？")
        elif cmd=="forward":
            printw("その方向には行けません。")
        elif cmd=="back" or cmd=="exit" or cmd=="exit storeroom":
            printw("用具入れから出ます。")
            gv.sc=sc_toilet()
        else:
            gv.cmdflag2=False
        return gv

class sc_bridge(scene):

    def initmsg(self, gv):
        print("あなたは橋の上にいます。")

    def cmdexe(self, cmd, gv):
        if cmd=="look":
            printw("欄干（railing）があります。")
            printw("橋の下を川（river）が流れています。")
        elif cmd=="look railing":
            printw("肩ほどの高さの欄干です。")
        elif cmd=="look river":
            printw("川原にきらきらしたものが見えます。")
        elif cmd=="put rope" or cmd=="tie rope" or cmd=="set rope" or cmd=="use rope":
            if gv.flag["rope"]=="get":
                printw("欄干にロープを結びつけました！")
                gv.flag["rope"]="put"
            elif gv.flag["rope"]=="put":
                printw("すでに結んであります。")
            else:
                printw("あなたはそれを持っていません。")
        elif cmd=="back":
            printw("後ろにもどります。")
            gv.sc=sc_park()
        elif cmd=="forward":
            printw("そちらには進めません。")
        elif cmd=="down":
            if gv.flag["rope"]=="put":
                printw("ロープを使って川原に降ります。")
                gv.sc=sc_river()
            else:
                printw("あぶないですよ？！")
        else:
            gv.cmdflag2=False
        return gv

class sc_river(scene):

    def initmsg(self, gv):
        printw("あなたは川原にいます。")

    def cmdexe(self, cmd, gv):
        if cmd=="look":
            printw("地下道の入口（hole）があります。")
            if gv.flag["board"]=="drop":
                printw("板（board）が置いてあります。")
            if gv.flag["glass"]=="drop":
                printw("ガラスの破片（glass）が落ちています。")
            if gv.flag["rope"]=="put":
                printw("橋に結んであるロープ（rope）がみえます。")
        elif cmd=="look hole":
            printw("人の入れそうな大きさの穴です。")
            if gv.flag["board"]=="fixed":
                printw("板(board)が打ち付けてあります。")
            else:
                printw("入口が大きく口を開けています。")
        elif cmd=="look glass":
            printw("なんの役にも立ちそうにありません。")
        elif cmd=="use crowbar" or cmd=="remove board":
            if gv.flag["crowbar"]=="get":
                printw("板を外しました！")
                gv.flag["board"]="drop"
        elif cmd=="enter" or cmd=="enter hole":
            if gv.flag["board"]=="fixed":
                printw("板が邪魔で入ることはできません。")
            else:
                printw("地下道に入ります。")
                gv.sc=sc_sewer()
        elif cmd=="back" or cmd=="up" or cmd=="climb rope":
            if gv.flag["rope"]=="put":
                printw("ロープを使ってのぼってゆきます。")
                gv.sc=sc_bridge()
        else:
            gv.cmdflag2=False
        return gv

class sc_sewer(scene):

    def initmsg(self, gv):
         printw("あなたは地下道のなかにいます。")

    def cmdexe(self, cmd, gv):
        if cmd=="look":
            printw("壁に鉄格子（grate）があります。")
            if gv.flag["ring"]=="appear":
                printw("エメラルドの指輪（ring）があります。")
        elif cmd=="open grate" or cmd=="move grate" or cmd=="remove grate":
            if gv.flag["grate"]=="fixed":
                printw("堅くて動きません。")
            elif gv.flag["grate"]=="movable":
                printw("鉄格子が開きました！")
                gv.flag["grate"]="open"
        elif cmd=="turn grate":
            if gv.flag["grate"]=="fixed":
                printw("鉄格子が回転しました！")
                gv.flag["grate"]="movable"
            else:
                printw("これ以上は回りません。")
        elif cmd=="search grate":
            if gv.flag["ring"]=="hidden":
                printw("エメラルドの指輪（ring）がありました！")
                gv.flag["ring"]="appear"
            else:
                printw("これ以上何かをさがす必要はないでしょう？")
        elif cmd=="get ring":
            if gv.flag["ring"]=="appear":
                printw("あなたはエメラルドの指輪を手に入れました！")
                printw("ゲームエンド")
                gv.gameflag=False
        elif cmd=="forward":
            printw("この先は真っ暗です。")
        elif cmd=="back" or cmd=="exit" or cmd=="exit grate":
            printw("地下道から出ます。")
            gv.sc=sc_river()
        else:
            gv.cmdflag2=False
        return gv

def printw(stg):
    print(stg)
    time.sleep(0.1)

gv=gamevals()
printw("python one line adventure")
printw("2022 tenkey aikoukai")
printw("help で説明が表示されます。")
while gv.gameflag:
    gv.sc.initmsg(gv)
    inp=input("command:")
    gv=gv.sc.cmd_common(inp, gv)
