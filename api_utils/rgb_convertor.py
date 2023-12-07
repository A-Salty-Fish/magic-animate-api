from PIL import Image
import os


# 检查一个图片是否为三通道格式
def check_RGB(img_file):
    img = Image.open(img_file)
    return img.mode == 'RGB'


# 将一个图片转为三通道格式
def convert_RGB(img_file):
    img = Image.open(img_file)  # 打开图片
    img = img.convert("RGB")  # 4通道转化为rgb三通道
    img.save(img_file)
    return True


if __name__ == '__main__':
    pass
    # print(convert_RGB('C:\\Users\\13090\\Pictures\\QQ截图20231128174426.png'))
    # print(check_RGB('C:\\Users\\13090\\Pictures\\QQ截图20231128174426.png'))

    # path = "C:\\Users\\13090\\Pictures"# 原始路径
    # # save_path = './new_edge/'# 保存路径
    # all_images = os.listdir(path)
    #
    # for image in all_images:
    #     image_path = os.path.join(path, image)
    #     img = Image.open(image_path)  # 打开图片
    #     print(img.format, img.size, img.mode)#打印出原图格式
        # img = img.convert("RGB")  # 4通道转化为rgb三通道
        # img.save(save_path + image)
