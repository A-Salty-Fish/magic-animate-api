
import requests

import yaml

def load_oss_config():
    with open("../config/api_config.yaml") as config_file:
        config = yaml.load(config_file.read(), Loader=yaml.Loader)
        return config['oss']


# 下载url对应的图片文件到文件夹，命名自定
def fetch_img(url, filename, path):
    try:
        response = requests.get(url)
        with open(path + filename, "wb") as f:
            f.write(response.content)
        return True
    except Exception as e:
        print(e)
        print("下载文件失败")
        return False


# 根据url获取文件名
def get_file_name_by_url(url):
    return url.split('/')[-1]


# 根据url直接下载文件到配置目录中
def fetch_img_by_url(url):
    oss_config = load_oss_config()
    return fetch_img(url, get_file_name_by_url(url), oss_config['img_path'])


if __name__ == '__main__':
    pass
