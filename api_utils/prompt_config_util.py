import yaml


def generate_config(img_name, poss_name, config_name):

    img_pre_path = 'inputs/applications/api_image/'
    poss_pre_path = 'inputs/applications/driving/densepose/'
    with open("../configs/prompts/1.yaml") as config_file:
        config = yaml.load(config_file.read(), Loader=yaml.Loader)
        config['source_image'] = [img_pre_path + img_name]
        config['video_path'] = [poss_pre_path + poss_name]
        with open(f"../configs/prompts/{config_name}.yml" , "w") as f:
            yaml.dump(config, f)
            return f'configs/prompts/{config_name}.yml'


if __name__ == '__main__':
    generate_config('monalisa.png', 'running.mp4', 'monalisarunning')