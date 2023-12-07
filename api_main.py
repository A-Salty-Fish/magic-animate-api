import argparse
import os.path
import sys
import datetime

pythonpath = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
sys.path.insert(0, pythonpath)

import magicanimate.pipelines.animation

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

if __name__ == '__main__':

    start_animate_pipe('configs/prompts/1.yaml')
