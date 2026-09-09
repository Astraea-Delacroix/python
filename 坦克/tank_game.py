"""
坦克大战游戏 - 主程序
"""
import pygame
import sys
import os

# 初始化pygame
pygame.init()

# 从配置文件导入常量
from config import (SCREEN_WIDTH, SCREEN_HEIGHT, FPS, TILE_SIZE,
                    BLACK, WHITE, RED, GREEN, BLUE, YELLOW, GRAY, BROWN)

# 导入游戏模块
from game_objects import PlayerTank, EnemyTank, Bullet, Wall, Base
from game_map import GameMap

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("坦克大战")
        self.clock = pygame.time.Clock()
        self.running = True

        self.reset_game()

    def reset_game(self):
        """重置游戏"""
        self.game_over = False
        self.win = False

        # 清空所有精灵组
        if hasattr(self, 'all_sprites'):
            self.all_sprites.empty()
            self.player_group.empty()
            self.enemy_group.empty()
            self.bullet_group.empty()
            self.wall_group.empty()

        # 游戏对象组
        self.all_sprites = pygame.sprite.Group()
        self.player_group = pygame.sprite.Group()
        self.enemy_group = pygame.sprite.Group()
        self.bullet_group = pygame.sprite.Group()
        self.wall_group = pygame.sprite.Group()

        # 创建地图
        self.game_map = GameMap(self)
        self.game_map.load_level()

        # 创建玩家坦克
        self.player = PlayerTank(100, 500, self)
        self.all_sprites.add(self.player)
        self.player_group.add(self.player)

        # 创建基地
        self.base = Base(SCREEN_WIDTH // 2 - 20, SCREEN_HEIGHT - 60, self)
        self.all_sprites.add(self.base)

        # 敌人生成
        self.enemy_spawn_timer = 0
        self.enemy_spawn_delay = 3000  # 3秒
        self.max_enemies = 5
        self.total_enemies_spawned = 0
        self.max_total_enemies = 20

        # 分数
        self.score = 0
        self.font = pygame.font.Font(None, 36)

    def spawn_enemy(self):
        """生成敌方坦克"""
        if len(self.enemy_group) < self.max_enemies and self.total_enemies_spawned < self.max_total_enemies:
            import random
            x = random.choice([50, SCREEN_WIDTH // 2, SCREEN_WIDTH - 50])
            enemy = EnemyTank(x, 50, self)
            self.all_sprites.add(enemy)
            self.enemy_group.add(enemy)
            self.total_enemies_spawned += 1

    def handle_events(self):
        """处理事件"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not self.game_over:
                    self.player.shoot()
                elif event.key == pygame.K_r and self.game_over:
                    self.reset_game()  # 调用重置方法而不是__init__

    def update(self):
        """更新游戏状态"""
        if self.game_over:
            return

        # 更新所有精灵
        self.all_sprites.update()

        # 敌人生成逻辑
        current_time = pygame.time.get_ticks()
        if current_time - self.enemy_spawn_timer > self.enemy_spawn_delay:
            self.spawn_enemy()
            self.enemy_spawn_timer = current_time

        # 检查子弹碰撞
        for bullet in self.bullet_group:
            # 玩家子弹打中敌人
            if bullet.owner == 'player':
                hit_enemies = pygame.sprite.spritecollide(bullet, self.enemy_group, True)
                if hit_enemies:
                    bullet.kill()
                    self.score += 100
            # 敌人子弹打中玩家
            elif bullet.owner == 'enemy':
                if pygame.sprite.spritecollide(bullet, self.player_group, False):
                    bullet.kill()
                    self.player.take_damage()
                    if self.player.lives <= 0:
                        self.game_over = True
                # 敌人子弹打中基地
                if pygame.sprite.collide_rect(bullet, self.base):
                    bullet.kill()
                    self.base.take_damage()
                    if self.base.health <= 0:
                        self.game_over = True

        # 检查胜利条件
        if self.total_enemies_spawned >= self.max_total_enemies and len(self.enemy_group) == 0:
            self.game_over = True
            self.win = True

    def draw(self):
        """绘制游戏画面"""
        self.screen.fill(BLACK)

        # 绘制所有精灵
        self.all_sprites.draw(self.screen)

        # 绘制UI信息
        score_text = self.font.render(f"Score: {self.score}", True, WHITE)
        self.screen.blit(score_text, (10, 10))

        lives_text = self.font.render(f"Lives: {self.player.lives}", True, WHITE)
        self.screen.blit(lives_text, (10, 50))

        enemies_text = self.font.render(f"Enemies: {len(self.enemy_group)}/{self.max_total_enemies - self.total_enemies_spawned}", True, WHITE)
        self.screen.blit(enemies_text, (SCREEN_WIDTH - 200, 10))

        base_health_text = self.font.render(f"Base: {self.base.health}", True, WHITE)
        self.screen.blit(base_health_text, (SCREEN_WIDTH - 200, 50))

        # 游戏结束画面
        if self.game_over:
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            overlay.set_alpha(128)
            overlay.fill(BLACK)
            self.screen.blit(overlay, (0, 0))

            if self.win:
                game_over_text = self.font.render("YOU WIN!", True, GREEN)
            else:
                game_over_text = self.font.render("GAME OVER", True, RED)
            text_rect = game_over_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50))
            self.screen.blit(game_over_text, text_rect)

            final_score_text = self.font.render(f"Final Score: {self.score}", True, WHITE)
            score_rect = final_score_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
            self.screen.blit(final_score_text, score_rect)

            restart_text = self.font.render("Press R to Restart", True, YELLOW)
            restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50))
            self.screen.blit(restart_text, restart_rect)

        pygame.display.flip()

    def run(self):
        """运行游戏主循环"""
        while self.running:
            self.clock.tick(FPS)
            self.handle_events()
            self.update()
            self.draw()

        pygame.quit()
        sys.exit()

if __name__ == '__main__':
    game = Game()
    game.run()
