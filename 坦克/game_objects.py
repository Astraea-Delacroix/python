"""
游戏对象类定义
"""
import pygame
import random

# 从配置文件导入常量
from config import (SCREEN_WIDTH, SCREEN_HEIGHT, TILE_SIZE,
                    BLACK, WHITE, RED, GREEN, BLUE, YELLOW, GRAY, BROWN)

class Tank(pygame.sprite.Sprite):
    """坦克基类"""
    def __init__(self, x, y, game):
        super().__init__()
        self.game = game
        self.width = 40
        self.height = 40
        self.image = pygame.Surface((self.width, self.height))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = 2
        self.direction = 'up'  # up, down, left, right
        self.shoot_delay = 500  # 射击间隔(毫秒)
        self.last_shot_time = 0

    def check_collision(self, dx, dy):
        """检查移动后是否会碰撞"""
        self.rect.x += dx
        self.rect.y += dy

        # 检查边界
        if self.rect.left < 0 or self.rect.right > SCREEN_WIDTH:
            self.rect.x -= dx
            return True
        if self.rect.top < 0 or self.rect.bottom > SCREEN_HEIGHT:
            self.rect.y -= dy
            return True

        # 检查墙壁碰撞
        if pygame.sprite.spritecollide(self, self.game.wall_group, False):
            self.rect.x -= dx
            self.rect.y -= dy
            return True

        return False

    def shoot(self):
        """发射子弹"""
        current_time = pygame.time.get_ticks()
        if current_time - self.last_shot_time > self.shoot_delay:
            bullet = Bullet(self.rect.centerx, self.rect.centery,
                          self.direction, self.bullet_owner, self.game)
            self.game.all_sprites.add(bullet)
            self.game.bullet_group.add(bullet)
            self.last_shot_time = current_time

    def draw_tank(self, color):
        """绘制坦克"""
        self.image.fill(color)
        # 绘制炮管指示方向
        if self.direction == 'up':
            pygame.draw.rect(self.image, BLACK, (15, 0, 10, 20))
        elif self.direction == 'down':
            pygame.draw.rect(self.image, BLACK, (15, 20, 10, 20))
        elif self.direction == 'left':
            pygame.draw.rect(self.image, BLACK, (0, 15, 20, 10))
        elif self.direction == 'right':
            pygame.draw.rect(self.image, BLACK, (20, 15, 20, 10))


class PlayerTank(Tank):
    """玩家坦克"""
    def __init__(self, x, y, game):
        super().__init__(x, y, game)
        self.lives = 3
        self.bullet_owner = 'player'
        self.draw_tank(GREEN)

    def update(self):
        """更新玩家坦克"""
        keys = pygame.key.get_pressed()
        dx, dy = 0, 0

        if keys[pygame.K_w] or keys[pygame.K_UP]:
            dy = -self.speed
            self.direction = 'up'
        elif keys[pygame.K_s] or keys[pygame.K_DOWN]:
            dy = self.speed
            self.direction = 'down'
        elif keys[pygame.K_a] or keys[pygame.K_LEFT]:
            dx = -self.speed
            self.direction = 'left'
        elif keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            dx = self.speed
            self.direction = 'right'

        if dx != 0 or dy != 0:
            self.check_collision(dx, dy)

        self.draw_tank(GREEN)

    def take_damage(self):
        """受到伤害"""
        self.lives -= 1


class EnemyTank(Tank):
    """敌方坦克"""
    def __init__(self, x, y, game):
        super().__init__(x, y, game)
        self.bullet_owner = 'enemy'
        self.speed = 1
        self.move_timer = 0
        self.move_delay = random.randint(1000, 3000)
        self.direction = random.choice(['up', 'down', 'left', 'right'])
        self.shoot_delay = random.randint(1000, 2000)
        self.draw_tank(RED)

    def update(self):
        """更新敌方坦克"""
        current_time = pygame.time.get_ticks()

        # AI移动逻辑
        if current_time - self.move_timer > self.move_delay:
            self.direction = random.choice(['up', 'down', 'left', 'right'])
            self.move_timer = current_time
            self.move_delay = random.randint(1000, 3000)

        # 移动
        dx, dy = 0, 0
        if self.direction == 'up':
            dy = -self.speed
        elif self.direction == 'down':
            dy = self.speed
        elif self.direction == 'left':
            dx = -self.speed
        elif self.direction == 'right':
            dx = self.speed

        if self.check_collision(dx, dy):
            # 碰撞后改变方向
            self.direction = random.choice(['up', 'down', 'left', 'right'])

        # 随机射击
        if random.random() < 0.02:  # 2%概率每帧射击
            self.shoot()

        self.draw_tank(RED)


class Bullet(pygame.sprite.Sprite):
    """子弹类"""
    def __init__(self, x, y, direction, owner, game):
        super().__init__()
        self.game = game
        self.width = 6
        self.height = 6
        self.image = pygame.Surface((self.width, self.height))
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y
        self.direction = direction
        self.owner = owner
        self.speed = 5

    def update(self):
        """更新子弹位置"""
        if self.direction == 'up':
            self.rect.y -= self.speed
        elif self.direction == 'down':
            self.rect.y += self.speed
        elif self.direction == 'left':
            self.rect.x -= self.speed
        elif self.direction == 'right':
            self.rect.x += self.speed

        # 超出屏幕则销毁
        if (self.rect.right < 0 or self.rect.left > SCREEN_WIDTH or
            self.rect.bottom < 0 or self.rect.top > SCREEN_HEIGHT):
            self.kill()

        # 碰到墙壁
        hit_walls = pygame.sprite.spritecollide(self, self.game.wall_group, False)
        if hit_walls:
            for wall in hit_walls:
                if wall.destructible:
                    wall.take_damage()
            self.kill()


class Wall(pygame.sprite.Sprite):
    """墙壁类"""
    def __init__(self, x, y, wall_type='brick'):
        super().__init__()
        self.wall_type = wall_type
        self.width = TILE_SIZE
        self.height = TILE_SIZE
        self.image = pygame.Surface((self.width, self.height))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        if wall_type == 'brick':
            self.image.fill(BROWN)
            self.destructible = True
            self.health = 1
        elif wall_type == 'steel':
            self.image.fill(GRAY)
            self.destructible = False
            self.health = 999
        elif wall_type == 'water':
            self.image.fill(BLUE)
            self.destructible = False
            self.health = 999

    def take_damage(self):
        """受到伤害"""
        if self.destructible:
            self.health -= 1
            if self.health <= 0:
                self.kill()


class Base(pygame.sprite.Sprite):
    """基地类"""
    def __init__(self, x, y, game):
        super().__init__()
        self.game = game
        self.width = 40
        self.height = 40
        self.image = pygame.Surface((self.width, self.height))
        self.image.fill(YELLOW)
        pygame.draw.rect(self.image, RED, (10, 10, 20, 20))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.health = 3

    def take_damage(self):
        """受到伤害"""
        self.health -= 1
        if self.health <= 0:
            self.image.fill(BLACK)
