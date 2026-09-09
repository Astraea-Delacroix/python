"""
游戏地图模块
"""
import pygame
from game_objects import Wall

class GameMap:
    """游戏地图类"""
    def __init__(self, game):
        self.game = game
        self.level_data = []

    def load_level(self):
        """加载关卡地图"""
        # 定义地图布局 (0=空地, 1=砖墙, 2=钢墙, 3=水域)
        level_layout = [
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 1, 1, 0, 0, 2, 2, 0, 0, 1, 1, 0, 0, 2, 2, 0, 0, 1, 1, 0],
            [0, 1, 1, 0, 0, 2, 2, 0, 0, 1, 1, 0, 0, 2, 2, 0, 0, 1, 1, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0],
            [0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 2, 2, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 2, 2, 0],
            [0, 2, 2, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 2, 2, 0],
            [0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0],
            [0, 1, 1, 0, 0, 0, 0, 0, 0, 2, 2, 0, 0, 0, 0, 0, 0, 1, 1, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        ]

        # 创建墙壁
        for row in range(len(level_layout)):
            for col in range(len(level_layout[row])):
                tile_type = level_layout[row][col]
                if tile_type == 1:
                    wall = Wall(col * 40, row * 40, 'brick')
                    self.game.all_sprites.add(wall)
                    self.game.wall_group.add(wall)
                elif tile_type == 2:
                    wall = Wall(col * 40, row * 40, 'steel')
                    self.game.all_sprites.add(wall)
                    self.game.wall_group.add(wall)
                elif tile_type == 3:
                    wall = Wall(col * 40, row * 40, 'water')
                    self.game.all_sprites.add(wall)
                    self.game.wall_group.add(wall)

        # 在基地周围创建保护墙
        base_x = 400 // 40
        base_y = (600 - 60) // 40

        protection_walls = [
            (base_x - 1, base_y - 1), (base_x, base_y - 1), (base_x + 1, base_y - 1),
            (base_x - 1, base_y), (base_x + 1, base_y),
            (base_x - 1, base_y + 1), (base_x, base_y + 1), (base_x + 1, base_y + 1),
        ]

        for pos in protection_walls:
            if 0 <= pos[1] < 15:  # 确保在地图范围内
                wall = Wall(pos[0] * 40, pos[1] * 40, 'brick')
                self.game.all_sprites.add(wall)
                self.game.wall_group.add(wall)
