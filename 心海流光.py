import math
import random
import pygame
from typing import List, Tuple

# ===================== 全局配置（和截图参数完全一致） =====================
class Config:
    GRAVITY = 0.0
    AIR_DRAG = 1.0
    FLING_FORCE = 3.0
    TANGENT_FORCE = 2.2
    FPS = 120
    PATH_SMOOTHNESS = 300
    PARTICLE_COUNT = 800
    SCREEN_WIDTH = 1200
    SCREEN_HEIGHT = 800

# ===================== 心形轨迹生成（笛卡尔心形公式） =====================
def generate_heart_path(center: Tuple[float, float], scale: float, num_points: int):
    path = []
    for i in range(num_points):
        t = 2 * math.pi * i / num_points
        x_rel = 16 * math.sin(t) ** 3
        y_rel = 13 * math.cos(t) - 5 * math.cos(2*t) - 2 * math.cos(3*t) - math.cos(4*t)
        x = center[0] + x_rel * scale
        y = center[1] - y_rel * scale
        path.append((x, y))
    return path

# 路径平滑重采样
def resample_path_evenly(path: List[Tuple[float, float]], target_count: int) -> List[Tuple[float, float]]:
    arc_lengths = [0.0]
    for i in range(1, len(path)):
        dx = path[i][0] - path[i-1][0]
        dy = path[i][1] - path[i-1][1]
        arc_lengths.append(arc_lengths[-1] + math.hypot(dx, dy))
    total_length = arc_lengths[-1]
    even_path = []
    for i in range(target_count):
        target_dist = total_length * i / target_count
        idx = arc_lengths.index(next(x for x in arc_lengths if x >= target_dist))
        even_path.append(path[idx])
    return even_path

# ===================== 平滑路径类 =====================
class SmoothPath:
    def __init__(self, center: Tuple[float, float], scale: float):
        self.center = center
        self.scale = scale
        raw = generate_heart_path(center, scale, Config.PATH_SMOOTHNESS)
        self.raw_path = resample_path_evenly(raw, Config.PATH_SMOOTHNESS)
        self.points = self.raw_path.copy()
        self.length = len(self.points)

    def get_point(self, t: float):
        idx = int(t * self.length) % self.length
        return self.points[idx]

# ===================== 流光粒子类（物理运动逻辑） =====================
class Petal:
    __slots__ = ('x', 'y', 'vx', 'vy', 'image', 'angle', 'angle_speed', 'life')
    def __init__(self, x: float, y: float, heart_center: Tuple[float, float], move_dir: Tuple[float, float]):
        self.x, self.y = x, y
        self.life = 1.0
        # 径向力（指向爱心中心）
        dx_to_center = x - heart_center[0]
        dy_to_center = y - heart_center[1]
        dist_to_center = math.hypot(dx_to_center, dy_to_center) or 1
        radial_dir_x, radial_dir_y = dx_to_center/dist_to_center, dy_to_center/dist_to_center

        move_dist = math.hypot(*move_dir) or 1
        tangent_dir_x, tangent_dir_y = move_dir[0]/move_dist, move_dir[1]/move_dist

        # 流光物理参数
        outward_speed = Config.FLING_FORCE * random.uniform(0.6, 1.4)
        tangent_speed = Config.TANGENT_FORCE * random.uniform(0.5, 1.2)
        random_angle = random.uniform(0, 2*math.pi)
        random_speed = Config.FLING_FORCE * random.uniform(0.1, 0.4)

        self.vx = radial_dir_x*outward_speed + tangent_dir_x*tangent_speed + math.cos(random_angle)*random_speed
        self.vy = radial_dir_y*outward_speed + tangent_dir_y*tangent_speed
        self.angle = random.uniform(0, math.pi*2)
        self.angle_speed = random.uniform(-0.05, 0.05)
        self.image = pygame.Surface((4,4), pygame.SRCALPHA)
        pygame.draw.circle(self.image, (255,255,255,220), (2,2), 2)

    def update(self, dt: float):
        self.vx *= Config.AIR_DRAG
        self.vy *= Config.AIR_DRAG + Config.GRAVITY
        self.x += self.vx * dt * 60
        self.y += self.vy * dt * 60
        self.life -= dt * 0.3

    def draw(self, screen):
        if self.life > 0:
            self.image.set_alpha(int(self.life*255))
            screen.blit(self.image, (self.x, self.y))

# ===================== 主程序 =====================
def main():
    pygame.init()
    screen = pygame.display.set_mode((Config.SCREEN_WIDTH, Config.SCREEN_HEIGHT))
    pygame.display.set_caption("心海流光")
    clock = pygame.time.Clock()
    heart_center = (Config.SCREEN_WIDTH//2, Config.SCREEN_HEIGHT//2 - 50)
    path = SmoothPath(heart_center, 12)
    particles = []
    trail_surface = pygame.Surface(screen.get_size(), pygame.SRCALPHA)

    running = True
    while running:
        dt = clock.tick(Config.FPS) / 1000
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                running = False

        # 持续生成爱心流光粒子
        if len(particles) < Config.PARTICLE_COUNT:
            t = random.random()
            px, py = path.get_point(t)
            move_dir = (math.cos(t*math.pi*2), math.sin(t*math.pi*2))
            particles.append(Petal(px, py, heart_center, move_dir))

        # 拖尾效果+粒子更新
        trail_surface.fill((0,0,0,18), special_flags=pygame.BLEND_RGBA_MIN)
        for p in particles[:]:
            p.update(dt)
            p.draw(trail_surface)
            if p.life <= 0:
                particles.remove(p)

        screen.fill((0,0,0))
        screen.blit(trail_surface, (0,0))
        pygame.display.flip()
    pygame.quit()

if __name__ == "__main__":
    main()