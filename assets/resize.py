import cv2
import os
import glob
import sys

# 图片文件夹路径
path_to_images = sys.argv[1]
# 图片输出文件夹路径，确保该目录已经存在或者脚本里面创建它
output_folder = sys.argv[2]

# 确保输出目录存在
os.makedirs(output_folder, exist_ok=True)

# 列出所有jpg图像
images = glob.glob(os.path.join(path_to_images, '*.jpg'))

for image_file in images:
    # 读取图像
    img = cv2.imread(image_file)
    # 计算新的尺寸，resize到原大小的0.25倍
    width, height = int(img.shape[1] * 0.25), int(img.shape[0] * 0.25)
    # 使用INTER_AREA插值方法进行减小尺寸的resize操作，这是缩放时推荐的插值方式
    resized_img = cv2.resize(img, (width, height), interpolation=cv2.INTER_AREA)
    
    # 定义输出的图像文件路径
    base_name = os.path.basename(image_file)
    output_file_path = os.path.join(output_folder, base_name)
    
    # 写出缩放后的图像到输出目录
    cv2.imwrite(output_file_path, resized_img)

print("所有图片已经缩小至原始尺寸的0.25倍，并保存至指定文件夹。")

