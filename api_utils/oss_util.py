
import requests

import yaml

import oss2

def load_oss_config():
    with open("../configs/api_config.yaml") as config_file:
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


def init_auth(access_key_id, access_key_secret):
    auth = oss2.Auth(access_key_id, access_key_secret)
    return auth

def upload_file(auth, end_point, bucket_name, file_path, file_name):
    # 填写Bucket所在地域对应的Endpoint。以华东1（杭州）为例，Endpoint填写为https://oss-cn-hangzhou.aliyuncs.com。
    # yourBucketName填写存储空间名称。
    bucket = oss2.Bucket(auth, end_point, bucket_name)

    # 上传文件到OSS。
    # yourObjectName由包含文件后缀，不包含Bucket名称组成的Object完整路径，例如abc/efg/123.jpg。
    # yourLocalFile由本地文件路径加文件名包括后缀组成，例如/users/local/myfile.txt。
    try:
        bucket.put_object_from_file(file_name, file_path)
        print(f"上传成功{file_name}")
        return True
    except Exception as e:
        print(e)
        return False


if __name__ == '__main__':
    pass
