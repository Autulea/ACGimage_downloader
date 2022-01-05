import json
import random
import time
import urllib.request

from utils import files
from utils.config import save_config

CONVERT = 1


def proxy_urlopen(url, my_config: dict):
    """
    urlopen 的代理实现
    :param my_config: 配置文件
    :param url: URL地址
    :return: row
    """
    proxy = my_config['proxy']
    proxy_support = urllib.request.ProxyHandler({'https': proxy})
    opener = urllib.request.build_opener(proxy_support)
    urllib.request.install_opener(opener)
    result = urllib.request.urlopen(url)
    return result


def get(url: str, my_config: dict, header=None):
    """
    HTTP GET获取
    :param header:
    :param my_config: 配置文件
    :param url: URL地址
    :return: row
    """
    if header is None:
        header = {}
    header['Accept'] = 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'
    header['Accept-Language'] = 'zh-CN,zh;q=0.8,en;q=0.6'
    header[
        'User-Agent'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3790.0 Safari/537.36'
    retry_count = 4
    while retry_count:
        try:
            req = proxy_urlopen(urllib.request.Request(url, headers=header), my_config)
            return req.read()
        except:
            retry_count -= 1
            print('解析 {} 时发生异常，剩余尝试次数 {} 次'.format(url, retry_count))
            continue


def url_to_filename(url: str):
    """
    解码文件名
    :param url: 从网址中截取文件名
    :return: str
    """
    return urllib.parse.unquote(url.split('/')[-1])


def get_yande_pic_list(my_config: dict, page: int):
    """
    解码文件名
    :param my_config: 配置文件
    :param page: 页码
    :return: 解析的json
    """
    print('Reading page', page)
    include_tags = my_config['include_tags']
    my_config['last_search_page'] = str(page)
    save_config(my_config)
    include_tags = include_tags.replace(' ', '+')
    if include_tags:
        url = 'https://yande.re/post.json?tags={}&page={}'.format(include_tags, str(page))
    else:
        url = 'https://yande.re/post.json?page=' + str(page)  # JSON API
    json_data = get(url, my_config)
    if not json_data:
        print('Request' + url + 'failure.')
        exit()
    try:
        json_data = json_data.decode('utf-8')
    except:
        print(url + 'decode failure.')
        exit(500)
    return json_data


def yande_tag_judge(post, my_config):
    """
    判断待排除的tag
    :param post:
    :param my_config:
    :return:
    """
    time.sleep(1)
    exclude_tags = my_config['exclude_tags']
    if list(set(exclude_tags).intersection(set(post['tags'].strip(' ').split(' ')))):
        print(post['id'], ' has exclude tags!')
        return False
    return True


def yande_download(post, my_config):
    folder_path = my_config['save_path']
    # 获取文件名并解码
    # 没错我就是嵌套狂魔
    file_name = files.rename(url_to_filename(post['file_url']))
    # 文件是否已存在？
    # 提醒：存在已知问题
    # 如果网站上post的tags被修改，那么两次爬取的tag是不同的，id_exist只能判断是否下载过这张图片，不能更新tag到文件名。
    # ----又不是不能用.jpg
    if files.id_exists(file_name):
        print(post['id'], ' 已存在，跳过')
        time.sleep(1)
        return True
    print('{} 开始下载 {} 大小 {}M 类型 {}'.format(time.strftime('%H:%M:%S'),
                                           post['id'], "%.2f" % (post['file_size'] / 1048576), post['file_ext']))
    start_time = time.time()
    img = get(post['file_url'], my_config, {
        'Host': 'files.yande.re', 'Referer': 'https://yande.re/post/show/' + str(post['id'])})
    cost_time = time.time() - start_time
    print('{} 下载完毕，耗时 {}s，平均速度 {}k/s'.format(post['id'], "%.2f" %
                                             cost_time, "%.2f" % (post['file_size'] / 1024 / cost_time)))
    files.write(folder_path, file_name, img)
    files.append_id_pool(file_name)
    if CONVERT:
        files.convert_to_webp(folder_path, file_name, del_flag=True)
    time.sleep(random.randint(40, 60))


def yande_worker(my_config: dict):
    """
    yande.re 的爬虫函数
    :param my_config: 配置文件
    :return: None
    """
    # 程序是否运行的flag
    pic_list_exist = 1
    start_pages = my_config['start_pages']
    page = int(start_pages)
    files.create_id_pool(my_config['save_path'])
    while pic_list_exist:
        # 通过API获取图片列表
        pic_list = get_yande_pic_list(my_config, page)
        page += 1
        # 判断是否到达指定的最后一页
        if page > int(my_config['end_pages']):
            pic_list_exist = 0
        # 解析json
        pic_list = json.loads(pic_list)
        # 判断是否为空页，便于提前结束进程
        if not len(pic_list):
            pic_list_exist = 0
            print('No more image!')
        while pic_list:
            post = pic_list.pop(0)
            if yande_tag_judge(post, my_config):
                yande_download(post, my_config)


if __name__ == '__main__':
    url = 'http://123.com/hkl.gpg'
    print(url_to_filename(url))
