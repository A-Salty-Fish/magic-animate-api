import argparse
import os.path
import sys
import datetime

import yaml

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

def get_output(config_name):
    output_dirs = os.listdir('./samples')
    outputs = []
    for output_dir in output_dirs:
        if output_dir.startswith(config_name):
            directory = './samples/' + output_dir
            for root, _, files in os.walk(directory):
                for file in files:
                    if file.endswith(".mp4"):
                        outputs.append(os.path.join(root, file))
    return outputs


if __name__ == '__main__':
    print(get_output('1'))
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
