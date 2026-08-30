import pygame
import numpy as np
import cv2
import math
W, H = 1280, 720
FPS = 60
N = 14000
pygame.init()
screen = pygame.display.set_mode((W, H))
pygame.display.set_caption("流星旋涡")
clock = pygame.time.Clock()

user_rot_z = math.radians(20)
user_tilt_x = 0.65

dragging = False
last_mouse_pos = (0, 0)

galaxy = np.concatenate([
    np.zeros(N // 2, dtype=np.int32),
    np.ones(N - N // 2, dtype=np.int32)
])
progress = np.random.rand(N).astype(np.float32)
angle_initial = np.random.rand(N).astype(np.float32) * 2 * np.pi
offset = (np.random.randn(N) * 0.04).astype(np.float32)

pos = np.zeros((N, 2), dtype=np.float32)
radius_initial = progress * 380 + 5
pos[:, 0] = np.where(galaxy == 0, W * 0.32, W * 0.68) + radius_initial * np.cos(angle_initial)
pos[:, 1] = H * 0.5 + radius_initial * np.sin(angle_initial) * 0.65

arm_spread = 16.0
arm_width = 0.25

SPRAY_N = 150000 
spray_pos = np.zeros((SPRAY_N, 2), dtype=np.float32)
spray_vel = np.zeros((SPRAY_N, 2), dtype=np.float32)
spray_life = np.zeros(SPRAY_N, dtype=np.float32)
spray_max_life = np.zeros(SPRAY_N, dtype=np.float32)

spray_color_palette = np.array([
    [255, 80, 80],    # 红
    [255, 160, 60],   # 橙
    [255, 240, 80],   # 黄
    [80, 255, 120],   # 绿
    [80, 220, 255],   # 青
    [120, 80, 255],   # 蓝紫
    [200, 80, 255]    # 紫
], dtype=np.float32)

colors_palette = np.array([
    [150, 80, 255],  # 紫
    [255, 220, 80],  # 黄
    [80, 220, 255],  # 青
    [150, 80, 255],  # 紫
    [80, 220, 255]   # 青
], dtype=np.float32)

nebula_array = np.zeros((H, W, 3), dtype=np.uint8)
final_surface = pygame.Surface((W, H))

running = True
t = 0

while running:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            dragging = True
            last_mouse_pos = event.pos
        elif event.type == pygame.MOUSEBUTTONUP:
            dragging = False
        elif event.type == pygame.MOUSEMOTION and dragging:
            dx = event.pos[0] - last_mouse_pos[0]
            dy = event.pos[1] - last_mouse_pos[1]
            user_rot_z += dx * 0.01
            user_tilt_x -= dy * 0.01
            user_tilt_x = np.clip(user_tilt_x, 0.1, 1.4)
            last_mouse_pos = event.pos

    t += 1
    time_phase = t * 0.02
    cos_R = math.cos(user_rot_z)
    sin_R = math.sin(user_rot_z)

    progress += 0.001
    progress[progress > 1.0] = 0.0
    radius = progress * 380 + 5
    arm_phase = np.where(galaxy == 0, 0, 2.0)
    spiral_angle = arm_phase + angle_initial + progress * arm_spread
    offset_angle = spiral_angle + np.pi / 2
    offset_term = offset * radius * arm_width

    target_x = radius * np.cos(spiral_angle) + offset_term * np.cos(offset_angle)
    target_y = (radius * np.sin(spiral_angle) + offset_term * np.sin(offset_angle)) * user_tilt_x

    active_centers = np.where(galaxy == 0, W * 0.32, W * 0.68)
    target_x = active_centers + target_x
    target_y = H * 0.5 + target_y

    rel_x = target_x - active_centers
    rel_y = target_y - H * 0.5
    rotated_x = rel_x * cos_R - rel_y * sin_R
    rotated_y = rel_x * sin_R + rel_y * cos_R
    target_x = active_centers + rotated_x
    target_y = H * 0.5 + rotated_y

    
    pos[:, 0] = target_x
    pos[:, 1] = target_y
    pos[:, 0] = np.clip(pos[:, 0], 0, W - 1)
    pos[:, 1] = np.clip(pos[:, 1], 0, H - 1)

    
    new_sprays = np.random.rand(N) < 0.08  
    if np.any(new_sprays):
        spray_indices = np.where(new_sprays)[0]
        free_slots = np.where(spray_life <= 0)[0][:len(spray_indices)]
        if len(free_slots) > 0:
            actual_count = min(len(free_slots), len(spray_indices))
            free_slots = free_slots[:actual_count]
            spray_indices = spray_indices[:actual_count]

            spray_pos[free_slots, 0] = pos[spray_indices, 0]
            spray_pos[free_slots, 1] = pos[spray_indices, 1]

            outer_dir_x = target_x[spray_indices] - active_centers[spray_indices]
            outer_dir_y = target_y[spray_indices] - H * 0.5
            norm = np.sqrt(outer_dir_x**2 + outer_dir_y**2) + 1e-5

            
            speed = np.random.rand(actual_count) * 8 + 2
            spray_vel[free_slots, 0] = (outer_dir_x / norm) * speed
            spray_vel[free_slots, 1] = (outer_dir_y / norm) * speed

            spray_max_life[free_slots] = np.random.rand(actual_count) * 40 + 15
            spray_life[free_slots] = spray_max_life[free_slots]

    
    active_sprays = spray_life > 0
    if np.any(active_sprays):
        
        track_x = spray_pos[active_sprays, 0].astype(np.int32)
        track_y = spray_pos[active_sprays, 1].astype(np.int32)
        track_x = np.clip(track_x, 0, W - 1)
        track_y = np.clip(track_y, 0, H - 1)
        track_indices = np.random.randint(0, 7, np.sum(active_sprays))
        track_colors = spray_color_palette[track_indices] * 0.4
        nebula_array[track_y, track_x] = np.clip(track_colors, 0, 255).astype(np.uint8)

        spray_vel[active_sprays, 0] *= 0.95
        spray_vel[active_sprays, 1] += 0.30
        spray_pos[active_sprays, 0] += spray_vel[active_sprays, 0]
        spray_pos[active_sprays, 1] += spray_vel[active_sprays, 1]
        spray_life[active_sprays] -= 1

    prog_norm = progress * 4
    idx_low = np.clip(np.floor(prog_norm).astype(np.int32), 0, 4)
    idx_high = np.clip(idx_low + 1, 0, 4)
    frac = (prog_norm - idx_low)[:, np.newaxis]
    color_low = colors_palette[idx_low]
    color_high = colors_palette[idx_high]
    colors = (color_low + (color_high - color_low) * frac).astype(np.float32)

    wave = np.sin(progress * 20 + time_phase)
    colors += (wave * 40)[:, np.newaxis]
    brightness_boost = 0.7 + 0.6 * (1 - progress)[:, np.newaxis]
    colors *= brightness_boost
    colors = np.clip(colors, 0, 255).astype(np.uint8)

    
    spray_colors = np.zeros((SPRAY_N, 3), dtype=np.uint8)
    if np.any(active_sprays):
        spray_brightness = (spray_life[active_sprays] / (spray_max_life[active_sprays] + 1e-5))[:, np.newaxis]
        rand_indices = np.random.randint(0, 7, np.sum(active_sprays))
        base_colors = spray_color_palette[rand_indices]
        spray_colors[active_sprays] = np.clip(base_colors * (spray_brightness * 1.5 + 0.2),0,255).astype(np.uint8)

    
    nebula_array = (nebula_array * 0.90).astype(np.uint8)
    x_vals = pos[:, 0].astype(np.int32)
    y_vals = pos[:, 1].astype(np.int32)
    nebula_array[y_vals, x_vals] = colors

    
    if np.any(active_sprays):
        spray_x = np.clip(spray_pos[active_sprays, 0].astype(np.int32), 0, W - 1)
        spray_y = np.clip(spray_pos[active_sprays, 1].astype(np.int32), 0, H - 1)
        nebula_array[spray_y, spray_x] = spray_colors[active_sprays]

    blurred = cv2.GaussianBlur(nebula_array, (0, 0), sigmaX=1.8)
    nebula_array = cv2.addWeighted(nebula_array, 0.75, blurred, 0.25, 0)

    final_surface = pygame.surfarray.make_surface(nebula_array.transpose(1, 0, 2))
    screen.blit(final_surface, (0, 0))

    
    for i in range(0, N, 3):
        pygame.draw.circle(screen, tuple(colors[i].tolist()), (int(pos[i, 0]), int(pos[i, 1])), 1)

    pygame.display.flip()

pygame.quit()
