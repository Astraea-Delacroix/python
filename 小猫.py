from PIL import Image, ImageDraw
import math

def create_cat_emoji():
    frames = []
    width, height = 200, 200
    
    for frame in range(10):
        img = Image.new('RGBA', (width, height), (255, 215, 0, 255))
        draw = ImageDraw.Draw(img)
        
        center_x, center_y = width // 2, height // 2
        
        draw.ellipse([center_x - 70, center_y - 60, center_x + 70, center_y + 80], 
                     fill=(255, 228, 181, 255), outline=(210, 105, 30, 255), width=3)
        
        draw.polygon([(center_x - 50, center_y - 55), (center_x - 70, center_y - 90), (center_x - 30, center_y - 65)],
                     fill=(255, 228, 181, 255), outline=(210, 105, 30, 255), width=2)
        draw.polygon([(center_x + 50, center_y - 55), (center_x + 70, center_y - 90), (center_x + 30, center_y - 65)],
                     fill=(255, 228, 181, 255), outline=(210, 105, 30, 255), width=2)
        
        draw.ellipse([center_x - 28, center_y - 30, center_x - 8, center_y - 10], fill=(255, 255, 255, 255))
        draw.ellipse([center_x + 8, center_y - 30, center_x + 28, center_y - 10], fill=(255, 255, 255, 255))
        draw.ellipse([center_x - 25, center_y - 27, center_x - 11, center_y - 13], fill=(0, 0, 0, 255))
        draw.ellipse([center_x + 11, center_y - 27, center_x + 25, center_y - 13], fill=(0, 0, 0, 255))
        
        draw.ellipse([center_x - 6, center_y, center_x + 6, center_y + 12], fill=(255, 153, 153, 255))
        
        hand_offset = math.sin(frame * 0.8) * 25
        hand_y = center_y + 5
        if frame < 5:
            draw.ellipse([center_x - 60 + hand_offset, hand_y - 15, center_x + hand_offset, hand_y + 25],
                         fill=(255, 228, 181, 255), outline=(210, 105, 30, 255), width=2)
        else:
            draw.ellipse([center_x - 60, hand_y - 15 + hand_offset, center_x, hand_y + 25 + hand_offset],
                         fill=(255, 228, 181, 255), outline=(210, 105, 30, 255), width=2)
        
        for i in range(4):
            wave_angle = frame * 35 + i * 80
            wave_x = center_x + 80 + int(math.cos(math.radians(wave_angle)) * 25)
            wave_y = center_y + int(math.sin(math.radians(wave_angle)) * 15)
            draw.text((wave_x, wave_y), '✧', fill=(150, 150, 150, 200), align='center')
        
        frames.append(img)
    
    frames[0].save('cat_emoji.gif', save_all=True, append_images=frames[1:], duration=150, loop=0)
    print('✅ 表情包已保存为: cat_emoji.gif')

if __name__ == '__main__':
    try:
        create_cat_emoji()
    except ImportError:
        print('请先安装Pillow库: pip install Pillow')
