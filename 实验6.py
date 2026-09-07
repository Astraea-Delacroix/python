import numpy as np
from PIL import Image
def process_image(image_path):
     img = Image.open(image_path)
     print("原始图片：")
     img.show()
     gray_img = img.convert("L")
     print("灰度化图片：")
     gray_img.show()
     flipped_img = img.transpose(Image.FLIP_TOP_BOTTOM)
     print("上下翻转后的图片：")
     flipped_img.show()
     img_array = np.array(img)
     print(f"图片的Numpy数组形状:{img_array.shape}")
if __name__ == "__main__":
     image_path = r"D:\python\campus.jpg"
     process_image(image_path)