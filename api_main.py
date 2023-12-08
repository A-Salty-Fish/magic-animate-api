import argparse
import json
import os.path
import random
import sys
import datetime
import time

import yaml
import requests

import pika

pythonpath = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
sys.path.insert(0, pythonpath)

import magicanimate.pipelines.animation

import api_utils.prompt_config_util as prompt_config_util
import api_utils.oss_util as oss_util


def start_animate_pipe(animate_config):
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", type=str, required=False)
    parser.add_argument("--dist", action="store_true", required=False)
    parser.add_argument("--rank", type=int, default=0, required=False)
    parser.add_argument("--world_size", type=int, default=1, required=False)

    args = parser.parse_args(
        [f'--config={animate_config}']
    )
    print(f"加载Config文件目录：{animate_config}")
    print(f"开始启动流水线 {datetime.datetime.now()}")
    magicanimate.pipelines.animation.run(args)
    print(f"流水线结束 {datetime.datetime.now()}")


def load_oss_config():
    with open("configs/api/api_config.yaml") as config_file:
        config = yaml.load(config_file.read(), Loader=yaml.Loader)
        return config['oss']

def load_rabbitmq_config():
    with open("configs/api/api_config.yaml") as config_file:
        config = yaml.load(config_file.read(), Loader=yaml.Loader)
        return config['rabbitmq']


def init_rabbitmq_channel(rabbitmq_config):
    credentials = pika.PlainCredentials(rabbitmq_config['username'], rabbitmq_config['password'])
    connection = pika.BlockingConnection(pika.ConnectionParameters(rabbitmq_config['host'], rabbitmq_config['port'], '/', credentials))
    channel = connection.channel()
    print("成功初始化rabbitmq连接")
    return channel


def get_output(config_name):
    output_dirs = os.listdir('./samples')
    outputs = []
    for output_dir in output_dirs:
        if output_dir.startswith(config_name + '-'):
            directory = './samples/' + output_dir
            for root, _, files in os.walk(directory):
                for file in files:
                    if file.endswith(".mp4"):
                        outputs.append(str(os.path.join(root, file)))
    return outputs


def call_back(call_back_url, task_id, call_back_output, retrys=3):
    if retrys == 0:
        print(f"重试次数用完:{task_id}")
        return
    url = call_back_url + task_id
    response = requests.post(url, data={'imgs': str(call_back_output)})
    if response.status_code == 200:
        print(f"回调成功:{task_id}")
    else:
        print(response.content)
        print(f"回调失败，准备重试:{task_id}")
        time.sleep(5 * (4 - retrys))
        call_back(call_back_url, task_id, retrys - 1)


def consume_magic_task(task):
    print(f"magic_api任务开始：{datetime.datetime.now()}")
    print(f"获取到任务参数:{str(task)}")
    # 获取参数
    img_url = task['img_url']
    task_id = task['id']
    poss = task['poss'] + '.mp4'
    call_back_url = task['call_back_url']
    # 下载文件
    oss_util.fetch_img(img_url, oss_util.get_file_name_by_url(img_url), './inputs/applications/api_image/')
    # 创建配置
    config_file = prompt_config_util.generate_config(
        oss_util.get_file_name_by_url(img_url),
        poss,
        task_id,
        "configs/prompts/1.yaml",
        "configs/prompts",
    )
    # 开始执行
    start_animate_pipe(config_file)
    # 获取输出
    outputs = get_output(task_id)
    oss_config = load_oss_config()
    auth = oss_util.init_auth(oss_config['access_key_id'], oss_config['access_key_secret'])
    call_back_output = []
    for output in outputs:
        if output.find('grid.mp4') != -1:
            filename = str(task_id) + '_' + output.split('/')[-1]
        else:
            filename = str(task_id) + '_' + output.split('/')[-1]
        oss_util.upload_file(auth, oss_config['end_point'], oss_config['bucket_name'],
                             output, "magic_api_result/" + filename)
        call_back_output.append("magic_api_result/" + filename)
    print(f"输出上传完成:{str(outputs)}")
    # call_back
    if call_back_url is not None:
        call_back(call_back_url, task_id, call_back_output)
    print(f"magic_api任务结束：{datetime.datetime.now()}")



# 消费成功的回调函数
def rabbitmq_callback(ch, method, properties, body):
    task = json.loads(body)
    print(f"rabbitMQ开始消费:{datetime.datetime.now()}")
    print(str(task))
    try:
        consume_magic_task(task)
        print(f"rabbitMQ消费成功:{datetime.datetime.now()}")
    except Exception as e:
        print(e)
        print(f"rabbitMQ消费中出现错误:{datetime.datetime.now()}")


if __name__ == '__main__':

    channel = init_rabbitmq_channel(load_rabbitmq_config())
    channel.basic_consume(queue='magic_api_task', on_message_callback=rabbitmq_callback, auto_ack=True)
    channel.start_consuming()  # 启动消费

    # pos_array = ['dancing2', 'demo4', 'multi_dancing', 'running', 'running2']
    # for i in range(4, 10):
    #     test_task = {
    #         'id': str(i),
    #         'img_url': 'https://dzy-test-model-bucket.oss-rg-china-mainland.aliyuncs.com/human/ybg.jpg',
    #         'poss': pos_array[random.randint(0, len(pos_array) - 1)],
    #     }
    #     consume_magic_task(test_task)

    # print(get_output('1'))
    # oss_config = load_oss_config()
    # auth = oss_util.init_auth(oss_config['access_key_id'], oss_config['access_key_secret'])
    # print(oss_util.upload_file(auth, oss_config['end_point'] , oss_config['bucket_name'], "./inputs/applications/api_image/monalisa.png", "magic_api_result/monalisa.png"))
    # config_file = prompt_config_util.generate_config("monalisa.png",
    #                                                  "running.mp4",
    #                                                  "monalisatest",
    #                                                  "configs/prompts/1.yaml",
    #                                                  "configs/prompts",
    #                                                  )
    # start_animate_pipe(config_file)
    # start_animate_pipe('configs/prompts/1.yaml')
