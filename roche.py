import pygame
import numpy as np
import sys

# ==========================================
# ロシュ限界シミュレーション パラメータ設定
# ==========================================

# 画面設定
WIDTH, HEIGHT = 1000, 800
FPS = 60

# 物理シミュレーション定数
G = 1.0             # 万有引力定数
M_CENTER = 30000.0  # 中心星の質量
G_SELF = 2.0        # 衛星を構成する破片同士の自己重力
SOFTENING = 1.5     # 重力計算のソフトニング（近距離での特異点発散を防止）
K_SPRING = 5.0      # 剛体のバネ定数（衛星内部の岩石同士の結合力）
L_BREAK = 1.25      # バネの破断閾値（自然長の25%伸びたらちぎれる）
D_MIN = 3.0         # 粒子同士の最小距離（近接斥力の判定距離）
K_REP = 20.0        # 近接斥力の強さ（重なりを防ぐ）
PARTICLE_RADIUS = 3 # 描画する粒子の半径

# 衛星の初期設定
R_SAT = 20.0        # 衛星の初期半径
D_LINK = 6.0        # 初期状態で粒子同士が結合する最大距離

# 初期軌道パラメータ (長楕円軌道)
R_ORBIT_A = 350.0   # 遠点距離（一番遠い位置・スタート地点）
R_ORBIT_P = 80.0    # 近点距離（一番近い位置）

# ロシュ限界の計算 (剛体モデルの近似式による理論値)
M_particle = G_SELF / G
M_sat_total = 91 * M_particle # 初期粒子数は91個
ROCHE_LIMIT = R_SAT * (2 * M_CENTER / M_sat_total)**(1/3)

# シミュレーション時間刻み
DT = 0.05
STEPS_PER_FRAME = 4 # 1フレームあたりの物理演算ステップ数（アニメーション速度）

def init_simulation():
    """衛星の初期配置、初期速度、粒子間の結合リンクを生成する"""
    points = []
    dx = 4.0
    dy = dx * np.sqrt(3) / 2
    # 六方最密充填で円形にパーティクルを配置（岩石の塊を作る）
    for i in range(-15, 16):
        for j in range(-15, 16):
            x = i * dx + (j % 2) * dx / 2
            y = j * dy
            if x**2 + y**2 <= R_SAT**2:
                points.append([x, y])
    pos = np.array(points, dtype=float)
    
    # ケプラーの法則（活力方程式）に基づく楕円軌道の初期速度の算出
    a = (R_ORBIT_A + R_ORBIT_P) / 2.0
    v_init = np.sqrt(G * M_CENTER * (2.0 / R_ORBIT_A - 1.0 / a))
    
    pos[:, 0] += R_ORBIT_A  # 遠点に配置
    vel = np.zeros_like(pos)
    vel[:, 1] = v_init      # Y軸方向に初速度を与える
    
    # 近接する粒子同士をバネで結ぶ
    links = []
    for i in range(len(pos)):
        for j in range(i+1, len(pos)):
            dist = np.linalg.norm(pos[i] - pos[j])
            if dist <= D_LINK:
                links.append((i, j, dist))
                
    return pos, vel, links

def compute_acceleration(pos, vel, links):
    """N体シミュレーション：すべての力を計算し、各粒子の加速度を返す"""
    N = len(pos)
    acc = np.zeros_like(pos)
    
    # 1. 中心星からの重力
    r_sq = np.sum(pos**2, axis=1, keepdims=True)
    acc -= G * M_CENTER * pos / (r_sq + 10.0**2)**1.5
    
    # 2. 衛星内部の結合力（剛体バネ）と潮汐力による破壊判定
    new_links = []
    link_mask = np.zeros((N, N), dtype=bool)
    
    if len(links) > 0:
        links_arr = np.array(links)
        idx_i, idx_j = links_arr[:, 0].astype(int), links_arr[:, 1].astype(int)
        l0 = links_arr[:, 2]
        
        diff = pos[idx_i] - pos[idx_j]
        dist = np.linalg.norm(diff, axis=1)
        
        # 破断判定: 引っ張られすぎて限界を超えたバネは切れる（潮汐破壊）
        keep = dist <= L_BREAK * l0
        
        idx_i_keep, idx_j_keep = idx_i[keep], idx_j[keep]
        l0_keep, dist_keep, diff_keep = l0[keep], dist[keep], diff[keep]
        
        new_links = [(i, j, l) for i, j, l in zip(idx_i_keep, idx_j_keep, l0_keep)]
        
        link_mask[idx_i_keep, idx_j_keep] = True
        link_mask[idx_j_keep, idx_i_keep] = True
        
        # フックの法則によるバネの引力
        force_mag = -K_SPRING * (dist_keep - l0_keep)
        dir_vec = diff_keep / (dist_keep[:, np.newaxis] + 1e-6)
        force = dir_vec * force_mag[:, np.newaxis]
        
        # 作用・反作用を加速度に加算
        np.add.at(acc, idx_i_keep, force)
        np.add.at(acc, idx_j_keep, -force)
        
    # 3. 粒子同士の自己重力と近接斥力
    diff_all = pos[:, np.newaxis, :] - pos[np.newaxis, :, :] # 全ペアの差分ベクトル
    dist_all = np.linalg.norm(diff_all, axis=2)
    np.fill_diagonal(dist_all, np.inf)
    
    # 自己重力（引力）
    gravity_force_mag = G_SELF / (dist_all**2 + SOFTENING**2)
    dir_vec_all = diff_all / (dist_all[:, :, np.newaxis] + 1e-6)
    gravity_force = -dir_vec_all * gravity_force_mag[:, :, np.newaxis]
    acc += np.sum(gravity_force, axis=1)
    
    # 斥力（岩石同士がめり込まないようにする力）
    dist_rep = dist_all.copy()
    dist_rep[link_mask] = np.inf
    repulsion_mask = dist_rep < D_MIN
    
    if np.any(repulsion_mask):
        repulsion_force_mag = K_REP * (D_MIN - dist_rep[repulsion_mask])
        rep_dir_vec = diff_all[repulsion_mask] / (dist_rep[repulsion_mask, np.newaxis] + 1e-6)
        rep_force = rep_dir_vec * repulsion_force_mag[:, np.newaxis]
        
        idx_i_rep, _ = np.where(repulsion_mask)
        np.add.at(acc, idx_i_rep, rep_force)
        
    return acc, new_links

def draw_text(screen, font, text, x, y, color=(255, 255, 255)):
    surface = font.render(text, True, color)
    screen.blit(surface, (x, y))

def main():
    # --- Pygame 初期化 ---
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("ロシュ限界（Roche Limit）シミュレーション")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 24)

    # シミュレーション初期状態のセットアップ
    pos, vel, links = init_simulation()
    acc, links = compute_acceleration(pos, vel, links)
    com_trail = []
    running = True
    paused = False

    # --- メインループ ---
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    paused = not paused
                elif event.key == pygame.K_r: # リセット
                    pos, vel, links = init_simulation()
                    acc, links = compute_acceleration(pos, vel, links)
                    com_trail = []

        if not paused:
            # ベロシティ・ベレ法（Velocity Verlet法）による高精度な数値積分
            for _ in range(STEPS_PER_FRAME):
                pos += vel * DT + 0.5 * acc * DT**2
                new_acc, links = compute_acceleration(pos, vel, links)
                vel += 0.5 * (acc + new_acc) * DT
                acc = new_acc
                
            # 衛星がほぼ原型を留めている場合のみ、重心の軌跡を記録
            if len(links) > len(pos):
                com_trail.append(np.mean(pos, axis=0))
                if len(com_trail) > 400:
                    com_trail.pop(0)

        # --- 描画処理 ---
        screen.fill((10, 10, 18)) # 宇宙空間の背景色
        cx, cy = WIDTH // 2, HEIGHT // 2
        
        # 軌跡描画
        if len(com_trail) > 1:
            points = [(int(p[0] + cx), int(p[1] + cy)) for p in com_trail]
            pygame.draw.lines(screen, (80, 80, 100), False, points, 2)

        # ロシュ限界の描画 (薄い赤い円)
        pygame.draw.circle(screen, (80, 40, 40), (cx, cy), int(ROCHE_LIMIT), 2)

        # 中心星の描画 (発光効果)
        for r_glow in range(40, 15, -5):
            alpha = 255 - int(255 * (r_glow - 15) / 25)
            glow_surface = pygame.Surface((r_glow * 2, r_glow * 2), pygame.SRCALPHA)
            pygame.draw.circle(glow_surface, (255, 200, 50, alpha // 4), (r_glow, r_glow), r_glow)
            screen.blit(glow_surface, (cx - r_glow, cy - r_glow))
        pygame.draw.circle(screen, (255, 220, 100), (cx, cy), 15)

        # 衛星の結合（緑色のバネ）描画
        for i, j, l0 in links:
            p1 = (int(pos[i, 0] + cx), int(pos[i, 1] + cy))
            p2 = (int(pos[j, 0] + cx), int(pos[j, 1] + cy))
            pygame.draw.line(screen, (50, 150, 100), p1, p2, 1)

        # 衛星の岩石（粒子）描画
        for p in pos:
            px, py = int(p[0] + cx), int(p[1] + cy)
            pygame.draw.circle(screen, (200, 220, 255), (px, py), PARTICLE_RADIUS)

        # UI 情報テキスト描画
        dist_to_center = np.linalg.norm(np.mean(pos, axis=0))
        draw_text(screen, font, f"Particles: {len(pos)}", 10, 10)
        draw_text(screen, font, f"Active Links (Cohesion): {len(links)}", 10, 30)
        draw_text(screen, font, f"Distance from Star: {dist_to_center:.1f}", 10, 50)
        draw_text(screen, font, "[SPACE]: Pause / Resume", 10, 90)
        draw_text(screen, font, "[R]: Reset Simulation", 10, 110)
        
        # 状態の警告表示
        if dist_to_center < ROCHE_LIMIT and len(links) > 10:
            draw_text(screen, font, "WARNING: INSIDE ROCHE LIMIT!", 10, 150, (255, 80, 80))
        elif len(links) <= 10:
            draw_text(screen, font, "SATELLITE DESTROYED (Tidal Disruption)", 10, 150, (150, 150, 255))

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()