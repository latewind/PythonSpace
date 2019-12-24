import os


def get_dir_size(path):
    """
    获取文件夹大小
    :param path:
    :return:
    """
    size = 0
    for root, dirs, files in os.walk(path):
        for file in files:
            try:
                size += os.path.getsize(root + "/" + file)
            except OSError:
                size += 0

    print(path, sizeof_fmt(size))
    return size


def sizeof_fmt(num, suffix='B'):
    for unit in ['', 'K', 'M', 'G', 'T', 'P', 'E', 'Z']:
        if abs(num) < 1024.0:
            return "%3.1f%s%s" % (num, unit, suffix)
        num /= 1024.0
    return "%.1f%s%s" % (num, 'Yi', suffix)


def get_child_dir(dir_path):
    dirs = []
    for _ in os.listdir(dir_path):
        if os.path.isdir(dir_path + "/" + _):
            dirs.append(dir_path + "/" + _)
    return dirs


if __name__ == '__main__':
    dir_list = get_child_dir("C:/")
    for _ in dir_list:
        get_dir_size(_)
