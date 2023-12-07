import yaml


def generate_config(img_name, poss_name, config_name, example_config, new_config_path):

    img_pre_path = 'inputs/applications/api_image/'
    poss_pre_path = 'inputs/applications/driving/densepose/'
    with open(example_config, 'r') as config_file:
        config = yaml.load(config_file.read(), Loader=yaml.Loader)
        config['source_image'] = [img_pre_path + img_name]
        config['video_path'] = [poss_pre_path + poss_name]
        with open(f"{new_config_path}/{config_name}.yml" , "w") as f:
            yaml.dump(config, f)
            return f'configs/prompts/{config_name}.yml'


if __name__ == '__main__':
    pass
    # generate_config('monalisa.png', 'running.mp4', 'monalisarunning', )