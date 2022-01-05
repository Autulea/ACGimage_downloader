import os
import os.path
import re
import shutil

from PIL import Image

ID_POOL = []


def create_id_pool(folder_path: str):
    """
    为提高检索效率，首次调用将对 folder_path 文件夹已存在的图片进行 id 提取，存储于一个列表中
    运行时再次调用可以强制刷新id池
    :param folder_path: 检索目标路径文件夹路径
    """
    global ID_POOL
    if ID_POOL:
        ID_POOL = []
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            file_path, file_name_and_ext = os.path.split(file)
            parts = re.split(' ', file_name_and_ext)
            if len(parts) >= 3:
                ID_POOL.append(parts[1])
    print('ID 池已更新, ID数量：', len(ID_POOL))


def append_id_pool(file_name: str):
    global ID_POOL
    parts = re.split(' ', file_name)
    if len(parts) >= 3:
        ID_POOL.append(parts[1])
        print('ID {} 已添加, ID数量：'.format(parts[1]), len(ID_POOL))
    else:
        print('文件名未知，请检查代码')


def convert_to_webp(folder_path: str, file_name: str, root: bool = False, del_flag: bool = 0):
    """
    将文件转换成 WebP 格式
    :param folder_path: 文件夹路径
    :param file_name: 文件名
    :param root: 是否写到程序根目录
    :param del_flag: 转换后是否删除
    :return: None
    """
    file_name = file_name if root else folder_path + '/' + file_name  # 类似三元运算符
    try:
        img = Image.open(file_name)
        save_name = os.path.splitext(file_name)[0] + '.webp'
        img.save(save_name)
        if del_flag:
            os.remove(file_name)
    except:
        print('save WebP error!')


def id_exists(file_name):
    """
    提取文件 ID ，确认图片是否存在，首次使用请调用 create_id_pool() 初始化 id 池
    方法确实高效，但缺点是不能更新图片的tag
    【又不是不能用。jpg】
    :param folder_path: 文件夹路径
    :param file_name: 文件名
    :return: bool
    """
    global ID_POOL
    id = re.split(' ', file_name)[1]
    if id in ID_POOL:
        return True
    return False


def rename(file_name):
    """
    去除非法字符
    :type file_name: str
    :return: str
    """
    chr_list = ('?', '\\', r'/', '*', ':', '<', '>', '|', '"')
    for chr in chr_list:
        file_name = file_name.replace(chr, '')
    return file_name


def write(folder_path: str, file_name: str, data, root: bool = False):
    """
    写出文件
    :param folder_path: 文件夹路径
    :param file_name: 文件名
    :param data: 文件数据
    :param root: 是否写到程序根目录
    :return: None
    """
    file_name = file_name if root else folder_path + '/' + file_name  # 类似三元运算符
    file = open(file_name, 'wb')
    if isinstance(data, int) or isinstance(data, str):
        data = str(data).encode()
    try:
        file.write(data)
    except:
        pass
    file.close()


def archive(save_path: str):
    print('archiving pictures...')
    for root, dirs, files in os.walk(save_path):
        if root == save_path:
            for file in files:
                parts = re.split(' ', file)
                if parts[0] in ['gelbooru', 'danbooru', 'yande.re']:
                    __dir = str(int(int(parts[1]) / 10000))
                    if os.path.exists(save_path + '/' + __dir):
                        shutil.move(os.path.join(root, file), os.path.join(save_path + '/' + __dir, file))
                    else:
                        os.mkdir(save_path + '/' + __dir)
                        shutil.move(os.path.join(root, file), os.path.join(save_path + '/' + __dir, file))


def archive_init(save_path: str):
    print('archiving pictures...')
    for root, dirs, files in os.walk(save_path):
        for file in files:
            parts = re.split(' ', file)
            if parts[0] in ['gelbooru', 'danbooru', 'yande.re']:
                __dir = str(int(int(parts[1])/10000))
                if os.path.exists(save_path+'/'+__dir):
                    shutil.move(os.path.join(root, file), os.path.join(save_path+'/'+__dir, file))
                else:
                    os.mkdir(save_path+'/'+__dir)
                    shutil.move(os.path.join(root, file), os.path.join(save_path+'/'+__dir, file))

