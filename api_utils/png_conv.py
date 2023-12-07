from PIL import Image
import os


if __name__ == '__main__':

    path = "./old_edge"# 原始路径
    save_path = './new_edge/'# 保存路径
    all_images = os.listdir(path)

    for image in all_images:
        image_path = os.path.join(path, image)
        img = Image.open(image_path)  # 打开图片
        print(img.format, img.size, img.mode)#打印出原图格式
        img = img.convert("RGB")  # 4通道转化为rgb三通道
        img.save(save_path + image)
