from utils.config import create_config
from utils.yande_web import yande_worker
from utils.gelbooru_web import gelbooru_worker
from utils.danbooru_web import danbooru_worker
from utils.files import archive
from sys import version_info

if version_info.minor >= 10:
    import ssl

    ssl._create_default_https_context = ssl._create_unverified_context

if __name__ == '__main__':
    my_config = create_config()

    if my_config['website'] == 'yande':
        yande_worker(my_config)
    elif my_config['website'] == 'gelbooru':
        gelbooru_worker(my_config)
    elif my_config['website'] == 'danbooru':
        danbooru_worker(my_config)
    
    archive(my_config['save_path'])
