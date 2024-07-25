import os  
from PIL import Image  
import io  
  
def compress_image(source_path, target_path, max_size=500 * 1024):  
    """  
    压缩图片到指定大小以下，并保存到目标路径。  
    如果原图是RGBA模式，则转换为RGB模式以保存为JPEG。  
    """  
    img = Image.open(source_path)  
    # 如果图像是RGBA模式，则转换为RGB模式  
    if img.mode != 'RGB':  
        img = img.convert('RGB')  
      
    # 初始质量  
    quality = 85  
      
    # 压缩图片直到其大小小于max_size  
    while True:  
        img_byte_arr = io.BytesIO()  
        img.save(img_byte_arr, format='JPEG', quality=quality)  
        img_bytes = img_byte_arr.getvalue()  
          
        if len(img_bytes) < max_size:  
            break  
          
        # 如果图片仍然太大，降低质量  
        quality -= 5  
        if quality < 10:  
            break  # 如果质量过低，则停止降低质量  
  
    # 将压缩后的图片保存到目标路径  
    with open(target_path, 'wb') as f:  
        f.write(img_bytes)
      
def process_images(source_dir, target_dir):  
    """  
    处理指定目录下的所有图片，将它们压缩后保存到新目录。  
    """  
    if not os.path.exists(target_dir):  
        os.makedirs(target_dir)  
  
    for root, dirs, files in os.walk(source_dir):  
        relative_path = os.path.relpath(root, source_dir)  
        target_sub_dir = os.path.join(target_dir, relative_path)  
        if not os.path.exists(target_sub_dir):  
            os.makedirs(target_sub_dir)  
  
        for file in files:  
            if file.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif')):  
                source_file_path = os.path.join(root, file)  
                target_file_path = os.path.join(target_sub_dir, file)  
                compress_image(source_file_path, target_file_path)
                print(f'compress {source_file_path} Done.')  
  
# 设置源目录和目标目录  
source_dir = './img'  
target_dir = './new_img'  
  
# 处理图片  
process_images(source_dir, target_dir)