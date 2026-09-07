from PIL import Image

# 定义像素猫的帧
frames = []

# 像素猫的像素数据（挥手动画）
cat_frames = [
    # 帧0：手在左边
    [
        "  ██████████  ",
        "  ████████    ",
        " ██████████   ",
        " ██████████   ",
        "████████████  ",
        "████████████  ",
        "████████████  ",
        "████████████  ",
        " ██████████   ",
        " ██████████   ",
        "  ████████    ",
        "  ████  ████  ",
        "  ████  ████  ",
        "   ██    ██   ",
        "   ██    ██   ",
        "    ██████    ",
        "   ████  ████ ",
        " ████      ████",
        "██          ██ ",
        " ████████████  ",
    ],
    # 帧1：手在中间
    [
        "  ██████████  ",
        "  ████████    ",
        " ██████████   ",
        " ██████████   ",
        "████████████  ",
        "████████████  ",
        "████████████  ",
        "████████████  ",
        " ██████████   ",
        " ██████████   ",
        "  ████████    ",
        "  ████  ████  ",
        "  ████  ████  ",
        "   ██    ██   ",
        "   ██    ██   ",
        "    ██████    ",
        "     ████████ ",
        "      ████████",
        "        ████  ",
        " ████████████  ",
    ],
    # 帧2：手在右边
    [
        "  ██████████  ",
        "  ████████    ",
        " ██████████   ",
        " ██████████   ",
        "████████████  ",
        "████████████  ",
        "████████████  ",
        "████████████  ",
        " ██████████   ",
        " ██████████   ",
        "  ████████    ",
        "  ████  ████  ",
        "  ████  ████  ",
        "   ██    ██   ",
        "   ██    ██   ",
        "    ██████    ",
        " ████  ████   ",
        "███      ████ ",
        " ██          ██",
        "  ████████████",
    ],
    # 帧3：手在中间
    [
        "  ██████████  ",
        "  ████████    ",
        " ██████████   ",
        " ██████████   ",
        "████████████  ",
        "████████████  ",
        "████████████  ",
        "████████████  ",
        " ██████████   ",
        " ██████████   ",
        "  ████████    ",
        "  ████  ████  ",
        "  ████  ████  ",
        "   ██    ██   ",
        "   ██    ██   ",
        "    ██████    ",
        "     ████████ ",
        "      ████████",
        "        ████  ",
        " ████████████  ",
    ],
]

# 颜色定义
WHITE = (255, 255, 255, 0)      # 透明
BEIGE = (255, 228, 181, 255)    # 米色
BROWN = (139, 69, 19, 255)      # 棕色
BLUE = (135, 206, 250, 255)     # 蓝色

def create_frame(pixel_data, scale=4):
    """创建单个帧"""
    height = len(pixel_data)
    width = max(len(row) for row in pixel_data)
    
    img = Image.new('RGBA', (width * scale, height * scale), WHITE)
    
    for y, row in enumerate(pixel_data):
        for x, char in enumerate(row):
            if char == '█':
                for dy in range(scale):
                    for dx in range(scale):
                        # 根据位置决定颜色
                        if y < 4 or (y >= 10 and y <= 12):
                            img.putpixel((x * scale + dx, y * scale + dy), BEIGE)
                        elif y == 4 or y == 5:
                            # 眼睛区域
                            if (x >= 3 and x <= 4) or (x >= 6 and x <= 7):
                                img.putpixel((x * scale + dx, y * scale + dy), BROWN)
                            else:
                                img.putpixel((x * scale + dx, y * scale + dy), BEIGE)
                        elif y >= 13 and y <= 14:
                            img.putpixel((x * scale + dx, y * scale + dy), BLUE)
                        else:
                            img.putpixel((x * scale + dx, y * scale + dy), BEIGE)
    
    return img

# 创建所有帧
for frame_data in cat_frames:
    frame = create_frame(frame_data, scale=8)
    frames.append(frame)

# 保存为GIF
frames[0].save('pixel_cat.gif', save_all=True, append_images=frames[1:], 
               duration=150, loop=0, transparency=0)

print('✅ 像素猫挥手动画已保存为: pixel_cat.gif')
