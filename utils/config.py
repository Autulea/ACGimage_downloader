import json
import os

config_path = './config.json'
test_json = './test.json'


def default_json():
    default = {
        'website': 'yande',
        'proxy': 'https://127.0.0.1:10809',
        'include_tags': '',
        'exclude_tags': '',
        'start_pages': '1',
        'end_pages': '1',
        'save_path': './pic',
        'last_search_page': '1'
    }
    return default


def read_config():
    global config_path
    if not os.path.exists(config_path):
        with open(config_path, 'w') as f:
            default_config = default_json()
            json.dump(default_config, f, indent=2)
    with open(config_path, 'r') as f:
        my_config = json.load(f)
        return my_config


def save_config(my_config: dict):
    global config_path
    if os.path.exists(config_path):
        os.remove(config_path)
        with open(config_path, 'w') as f:
            json.dump(my_config, f, indent=2)


def create_config():
    language = 'cn'
    language_input = input('请选择语言/Please select language[en/cn](default: cn):')
    if language_input:
        language = language_input
    my_config = default_json()
    if language == 'en':
        history = input('read history?[y/n](default: y):')
        if history == 'y' or history == '':
            my_config = read_config()
            print(my_config)
            return my_config
        website = input('select website[yande/gelbooru/danbooru](default: yande):')
        if website in ['yande', 'gelbooru', 'danbooru']:
            my_config['website'] = website
        proxy = input('type proxy server(default: 127.0.0.1:10809):')
        if proxy:
            my_config['proxy'] = 'proxy'
        include_tags = input('type tags you want, divided by space(default: none):')
        if include_tags:
            my_config['include_tags'] = include_tags
        exclude_tags = input('type tags you do not want, divided by space(default: none):')
        if exclude_tags:
            my_config['exclude_tags'] = exclude_tags
        start_pages = input('type start page number(default: 1):')
        if len(start_pages):
            my_config['start_pages'] = start_pages
        end_pages = input('type start page number(default: 1):')
        if len(end_pages):
            if int(my_config['start_pages']) > int(end_pages):
                end_pages = start_pages
            my_config['end_pages'] = end_pages
        save_path = input('type start page number(default: ./pic):')
        if save_path:
            my_config['save_path'] = save_path
        pass
    elif language == 'cn':
        history = input('是否使用历史记录配置?[y/n](default: y):')
        if history == 'y' or history == '':
            my_config = read_config()
            print(my_config)
            return my_config
        website = input('选择网站[yande/gelbooru/danbooru](默认: yande):')
        if website in ['yande', 'gelbooru', 'danbooru']:
            my_config['website'] = website
        proxy = input('配置代理服务器(默认: 127.0.0.1:10809):')
        if proxy:
            my_config['proxy'] = 'proxy'
        include_tags = input('输入想要的tags, 用空格分开(默认: none):')
        if include_tags:
            my_config['include_tags'] = include_tags
        exclude_tags = input('输入不想要的tags, 用空格分开(默认: none):')
        if exclude_tags:
            my_config['exclude_tags'] = exclude_tags
        start_pages = input('输入开始页码(默认: 1):')
        if len(start_pages):
            my_config['start_pages'] = start_pages
        end_pages = input('输入结束页码(默认: 1):')
        if len(end_pages):
            if int(my_config['start_pages']) > int(end_pages):
                end_pages = start_pages
            my_config['end_pages'] = end_pages
        save_path = input('输入保存路径(默认: ./pic):')
        if save_path:
            my_config['save_path'] = save_path
        pass
    else:
        print('unexpected error!')
        exit()
    print(my_config)
    save_config(my_config)
    return my_config


if __name__ == '__main__':
    pass
