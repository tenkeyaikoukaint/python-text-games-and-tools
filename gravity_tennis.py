import pygame
import sys

# --- 初期設定 ---
pygame.init()

# 画面サイズ
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Side View Tennis (Parabolic Physics)")

# 色の定義
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (50, 150, 255)
RED = (255, 100, 100)

# --- ゲームパラメータ ---
FPS = 60
GRAVITY = 0.5          # 重力加速度（放物線を作る鍵）
BOUNCE_STRENGTH = -15  # パドルで打ったときの上昇力
FRICTION_X = 0.999     # 空気の抵抗（横方向の減速、少しだけ入れると自然）

# --- クラス定義 ---

class Ball:
    def __init__(self):
        self.radius = 15
        self.reset()

    def reset(self):
        self.x = WIDTH // 2
        self.y = HEIGHT // 3
        self.vx = 5  # 横方向の初速
        self.vy = 0  # 縦方向の初速

    def move(self):
        # 重力を加算（放物線を描くための処理）
        self.vy += GRAVITY
        
        # 位置の更新
        self.x += self.vx
        self.y += self.vy

        # --- 衝突判定 ---
        
        # 左右の壁（ご指定の仕様：Yベクトルはそのままで横だけ反射）
        if self.x - self.radius < 0:
            self.x = self.radius
            self.vx *= -1  # 反転
        elif self.x + self.radius > WIDTH:
            self.x = WIDTH - self.radius
            self.vx *= -1  # 反転

        # 天井（跳ね返るように設定）
        if self.y - self.radius < 0:
            self.y = self.radius
            self.vy *= -0.8 # 少し勢いを殺して跳ね返る

    def draw(self, screen):
        pygame.draw.circle(screen, RED, (int(self.x), int(self.y)), self.radius)

class Paddle:
    def __init__(self):
        self.width = 120
        self.height = 20
        self.x = WIDTH // 2 - self.width // 2
        self.y = HEIGHT - 50
        self.speed = 8
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def move(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] and self.rect.right < WIDTH:
            self.rect.x += self.speed

    def draw(self, screen):
        pygame.draw.rect(screen, BLUE, self.rect)

# --- メインループ ---

def main():
    clock = pygame.time.Clock()
    ball = Ball()
    paddle = Paddle()
    
    running = True
    while running:
        # 1. イベント処理
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            # スペースキーでリセット
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    ball.reset()

        # 2. 更新処理
        paddle.move()
        ball.move()

        # パドルとの衝突判定
        # ボールが落下中(vy > 0)かつ、パドルの範囲内にある場合のみヒット
        if ball.vy > 0:
            # ボールの矩形（当たり判定用）
            ball_rect = pygame.Rect(ball.x - ball.radius, ball.y - ball.radius, ball.radius*2, ball.radius*2)
            
            if ball_rect.colliderect(paddle.rect):
                # パドルの上面に接触したか確認
                if ball.y + ball.radius < paddle.rect.centery + 10:
                    ball.vy = BOUNCE_STRENGTH  # 上向きの力をセット
                    
                    # 遊び要素：パドルの当たった位置によって横方向の速度を変化させる
                    # パドルの中心からの距離
                    hit_pos = (ball.x - paddle.rect.centerx) / (paddle.width / 2)
                    ball.vx += hit_pos * 3  # 端で打つと横に飛びやすくする

        # ゲームオーバー判定（下に落ちたらリセット）
        if ball.y > HEIGHT + 50:
            ball.reset()

        # 3. 描画処理
        screen.fill(BLACK) # 背景
        
        # ガイド線（地面）
        pygame.draw.line(screen, WHITE, (0, HEIGHT-10), (WIDTH, HEIGHT-10), 2)
        
        paddle.draw(screen)
        ball.draw(screen)

        # 情報表示
        font = pygame.font.SysFont(None, 24)
        info_text = font.render("Left/Right: Move Paddle | Space: Reset", True, WHITE)
        screen.blit(info_text, (10, 10))

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()