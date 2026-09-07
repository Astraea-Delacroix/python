import math
import random
import pygame
from typing import List, Tuple

# ===================== 全局配置（统一参数） =====================
class Config:
    GRAVITY = 0.0
    AIR_DRAG = 1.0
    FLING_FORCE = 3.0
    TANGENT_FORCE = 2.2
    FPS = 120
    PATH_SMOOTHNESS = 300
    HEART_PARTICLE_COUNT = 800
    ROSE_PETAL_COUNT = 200
    SCREEN_WIDTH = 1200
    SCREEN_HEIGHT = 800
    # 冰晶蓝配色
    MAIN_BLUE = (0, 204, 255, 220)
    LIGHT_BLUE = (102, 229, 255, 200)
    DARK_BLUE = (0, 102, 204, 255)

# ===================== 爱心流光模块 =====================
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

class HeartParticle:
    __slots__ = ('x', 'y', 'vx', 'vy', 'image', 'life')
    def __init__(self, x: float, y: float, heart_center: Tuple[float, float], move_dir: Tuple[float, float]):
        self.x, self.y = x, y
        self.life = 1.0
        dx_to_center = x - heart_center[0]
        dy_to_center = y - heart_center[1]
        dist_to_center = math.hypot(dx_to_center, dy_to_center) or 1
        radial_dir_x, radial_dir_y = dx_to_center/dist_to_center, dy_to_center/dist_to_center

        move_dist = math.hypot(*move_dir) or 1
        tangent_dir_x, tangent_dir_y = move_dir[0]/move_dist, move_dir[1]/move_dist

        outward_speed = Config.FLING_FORCE * random.uniform(0.6, 1.4)
        tangent_speed = Config.TANGENT_FORCE * random.uniform(0.5, 1.2)
        random_angle = random.uniform(0, 2*math.pi)
        random_speed = Config.FLING_FORCE * random.uniform(0.1, 0.4)

        self.vx = radial_dir_x*outward_speed + tangent_dir_x*tangent_speed + math.cos(random_angle)*random_speed
        self.vy = radial_dir_y*outward_speed + tangent_dir_y*tangent_speed
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

# ===================== 蓝蔷薇+水滴模块 =====================
class RosePetal:
    def __init__(self, x, y, size, angle):
        self.x = x
        self.y = y
        self.size = size
        self.angle = angle
        self.life = 1.0

    def draw(self, screen):
        if self.life > 0:
            surface = pygame.Surface((self.size*2, self.size*2), pygame.SRCALPHA)
            t = pygame.draw
            t.circle(surface, Config.MAIN_BLUE, (self.size, self.size), self.size, 2)
            t.circle(surface, Config.LIGHT_BLUE, (self.size, self.size), self.size*0.6, 1)
            surface.set_alpha(int(self.life*255))
            screen.blit(surface, (self.x-self.size, self.y-self.size))

    def update(self, dt):
        self.life -= dt * 0.2

class WaterDrop:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.speed = random.randint(3,6)
        self.life = 1.0

    def update(self, dt):
        self.y += self.speed
        self.life -= dt * 0.03

    def draw(self, screen):
        if self.life > 0:
            pygame.draw.circle(screen, Config.LIGHT_BLUE, (int(self.x), int(self.y)), 3)

# ===================== 主融合程序（已删除所有字体代码） =====================
def main():
    pygame.init()
    screen = pygame.display.set_mode((Config.SCREEN_WIDTH, Config.SCREEN_HEIGHT))
    pygame.display.set_caption("心海流光 · 蓝蔷薇")
    clock = pygame.time.Clock()
    heart_center = (Config.SCREEN_WIDTH//2, Config.SCREEN_HEIGHT//2 - 50)
    rose_center = (Config.SCREEN_WIDTH//2, Config.SCREEN_HEIGHT//2 + 120)
    path = SmoothPath(heart_center, 12)

    heart_particles = []
    rose_petals = []
    water_drops = []
    trail_surface = pygame.Surface(screen.get_size(), pygame.SRCALPHA)

    running = True
    while running:
        dt = clock.tick(Config.FPS) / 1000
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                running = False

        # 1. 生成爱心流光粒子
        if len(heart_particles) < Config.HEART_PARTICLE_COUNT:
            t = random.random()
            px, py = path.get_point(t)
            move_dir = (math.cos(t*math.pi*2), math.sin(t*math.pi*2))
            heart_particles.append(HeartParticle(px, py, heart_center, move_dir))

        # 2. 生成蓝蔷薇花瓣
        if len(rose_petals) < Config.ROSE_PETAL_COUNT:
            angle = random.uniform(0, math.pi*2)
            size = random.randint(20,60)
            x = rose_center[0] + math.cos(angle)*random.randint(30,120)
            y = rose_center[1] + math.sin(angle)*random.randint(20,80)
            rose_petals.append(RosePetal(x, y, size, angle))

        # 3. 生成蔷薇水滴
        if random.random() < 0.08:
            water_drops.append(WaterDrop(rose_center[0]+random.randint(-60,60), rose_center[1]))

        # 4. 更新+绘制所有元素
        trail_surface.fill((0,0,0,18), special_flags=pygame.BLEND_RGBA_MIN)
        # 爱心粒子
        for p in heart_particles[:]:
            p.update(dt)
            p.draw(trail_surface)
            if p.life <= 0:
                heart_particles.remove(p)
        # 蔷薇花瓣
        for petal in rose_petals[:]:
            petal.update(dt)
            petal.draw(trail_surface)
            if petal.life <= 0:
                rose_petals.remove(petal)
        # 水滴
        for drop in water_drops[:]:
            drop.update(dt)
            drop.draw(trail_surface)
            if drop.life <= 0 or drop.y > Config.SCREEN_HEIGHT:
                water_drops.remove(drop)

        screen.fill((0,0,0))
        screen.blit(trail_surface, (0,0))
        pygame.display.flip()
    pygame.quit()

if __name__ == "__main__":
    main()