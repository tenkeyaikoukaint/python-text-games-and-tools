import pygame
import random
import sys

# --- 定数 ---
GRID_W, GRID_H = 5, 21
CELL_SIZE = 30
SCREEN_W = 300
SCREEN_H = CELL_SIZE * GRID_H + 100

# 色 (レトロなグリーンディスプレイ風)
COLOR_BG = (0, 20, 0)
COLOR_BLOCK = (0, 255, 0)
COLOR_EMPTY = (0, 40, 0)
COLOR_TEXT = (0, 255, 0)

class CounterShoot:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))
        pygame.display.set_caption("Counter Shoot")
        self.font = pygame.font.SysFont("monospace", 20, bold=True)
        self.clock = pygame.time.Clock()
        self.reset(500)

    def reset(self, gap):
        # グリッド初期化 (JSの mc 配列に相当)
        self.mc = [["　" for _ in range(GRID_W)] for _ in range(GRID_H)]
        self.score = 0
        self.line = 0
        self.gap = gap
        self.is_gameover = False
        
        # タイマーイベント
        self.MOVE_EVENT = pygame.USEREVENT + 1
        pygame.time.set_timer(self.MOVE_EVENT, self.gap)
        
        # ショット消去用
        self.CLEAR_SHOT_EVENT = pygame.USEREVENT + 2
        self.active_shot_col = -1
        self.active_shot_start_row = -1

    def generate_new_row(self):
        """JSの move() 内の do-while ロジックを再現"""
        while True:
            row = ["　"] * GRID_W
            row[1] = "ロ" if random.random() < 0.66 else "　"
            row[2] = "ロ" if random.random() < 0.66 else "　"
            row[3] = "ロ" if random.random() < 0.66 else "　"
            # 1,2,3列目が全部埋まっていないこと
            if not (row[1] == "ロ" and row[2] == "ロ" and row[3] == "ロ"):
                return row

    def move_enemies(self):
        """敵を一行進める"""
        if self.is_gameover: return

        # 下から順にシフト
        for i in range(GRID_H - 1, 0, -1):
            self.mc[i] = list(self.mc[i-1])
        
        # 最上段に新しい行
        self.mc[0] = self.generate_new_row()
        
        self.line += 1
        if self.line >= 20:
            self.is_gameover = True
            pygame.time.set_timer(self.MOVE_EVENT, 0)

    def shoot(self, x):
        """JSの keyin() ロジックを再現"""
        if self.is_gameover: return

        # ペナルティ：既に敵がいる場所に撃つと敵が進む
        if self.mc[self.line][x] == "ロ":
            self.move_enemies()

        # 下から line 行目までを埋める
        for i in range(self.line, GRID_H):
            self.mc[i][x] = "ロ"
        
        # 消去判定用に情報を保存 (JSの clear() 予約に相当)
        self.active_shot_col = x
        self.active_shot_start_row = self.line + 1
        pygame.time.set_timer(self.CLEAR_SHOT_EVENT, 50) # 50ms後に消去

        # 揃ったか判定 (JSの mc[fl*5+1]=="ロ"...)
        # 判定対象は現在の境界線である self.line 行
        if self.mc[self.line][1] == "ロ" and \
           self.mc[self.line][2] == "ロ" and \
           self.mc[self.line][3] == "ロ":
            
            self.score += 1
            # 揃った行を消す
            self.mc[self.line][1] = "　"
            self.mc[self.line][2] = "　"
            self.mc[self.line][3] = "　"
            # 敵を押し戻す
            self.line = max(0, self.line - 1)

    def clear_shot(self):
        """JSの clear() 関数を再現"""
        if self.active_shot_col != -1:
            x = self.active_shot_col
            # ショットで埋めた部分（境界線より下）を空に戻す
            for j in range(self.active_shot_start_row, GRID_H):
                self.mc[j][x] = "　"
            self.active_shot_col = -1
            pygame.time.set_timer(self.CLEAR_SHOT_EVENT, 0)

    def draw(self):
        self.screen.fill(COLOR_BG)
        
        # グリッド描画
        start_y = 50
        start_x = (SCREEN_W - (GRID_W * CELL_SIZE)) // 2
        
        for r in range(GRID_H):
            for c in range(GRID_W):
                rect = pygame.Rect(start_x + c * CELL_SIZE, start_y + r * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                # 枠だけ描画
                pygame.draw.rect(self.screen, COLOR_EMPTY, rect, 1)
                
                char = self.mc[r][c]
                if char == "ロ":
                    # JSの「ロ」を矩形で表現。境界線(line)より上は敵、下は自弾
                    color = COLOR_BLOCK if r <= self.line else (0, 150, 0)
                    pygame.draw.rect(self.screen, color, rect.inflate(-4, -4))
                
                # 境界線の視覚化 (デバッグ用からゲーム性向上へ)
                if r == self.line:
                    pygame.draw.line(self.screen, (0, 80, 0), rect.bottomleft, rect.bottomright, 1)

        # スコア
        score_surf = self.font.render(f"SCORE: {self.score}", True, COLOR_TEXT)
        self.screen.blit(score_surf, (20, 10))

        if self.is_gameover:
            msg = self.font.render("GAME OVER", True, (255, 0, 0))
            self.screen.blit(msg, (SCREEN_W//2 - msg.get_width()//2, SCREEN_H//2))
            retry = self.font.render("Press SPACE to Menu", True, COLOR_TEXT)
            self.screen.blit(retry, (SCREEN_W//2 - retry.get_width()//2, SCREEN_H//2 + 30))

        pygame.display.flip()

    def run(self):
        menu = True
        while True:
            if menu:
                self.show_menu()
                menu = False
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit(); sys.exit()
                
                if event.type == self.MOVE_EVENT:
                    self.move_enemies()
                
                if event.type == self.CLEAR_SHOT_EVENT:
                    self.clear_shot()
                
                if event.type == pygame.KEYDOWN:
                    if self.is_gameover:
                        if event.key == pygame.K_SPACE: menu = True
                    else:
                        # オリジナルキー: ,(44) .(46) /(47)
                        if event.key == pygame.K_COMMA:  self.shoot(1)
                        if event.key == pygame.K_PERIOD: self.shoot(2)
                        if event.key == pygame.K_SLASH:  self.shoot(3)
                        # モダン補助キー
                        if event.key == pygame.K_z: self.shoot(1)
                        if event.key == pygame.K_x: self.shoot(2)
                        if event.key == pygame.K_c: self.shoot(3)

            self.draw()
            self.clock.tick(60)

    def show_menu(self):
        while True:
            self.screen.fill(COLOR_BG)
            t = self.font.render("COUNTER SHOOT", True, COLOR_TEXT)
            m1 = self.font.render("1: NORMAL", True, COLOR_TEXT)
            m2 = self.font.render("2: HARD", True, COLOR_TEXT)
            self.screen.blit(t, (SCREEN_W//2-t.get_width()//2, 100))
            self.screen.blit(m1, (SCREEN_W//2-m1.get_width()//2, 200))
            self.screen.blit(m2, (SCREEN_W//2-m2.get_width()//2, 250))
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.QUIT: pygame.quit(); sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_1: self.reset(500); return
                    if event.key == pygame.K_2: self.reset(300); return

if __name__ == "__main__":
    CounterShoot().run()
