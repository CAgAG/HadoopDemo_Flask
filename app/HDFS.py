import os
from app import client


def list_path(path):
    file_list = client.listdir(path)
    return file_list


def file_property_length(file_path):
    """
    if file_path is a dir
    return 0;
    """
    file = client.get_file_status(file_path)
    return file.length


def create_dir(pdir: str, dirname: str):
    client.mkdirs(f'{pdir}/{dirname}'.replace('//', '/'))


def delete_file(pdir: str, filename: str):
    print('delete', f'{pdir}/{filename}'.replace('//', '/'))
    client.delete(f'{pdir}/{filename}'.replace('//', '/'))


def upload_file(pdir: str, local_path: str):
    with open(local_path, 'rb') as f:
        client.create(pdir, f.read())


def download_file(h_path: str, local_path: str):
    print('download file', h_path, 'to', local_path)
    client.copy_to_local(src=h_path, localdest=local_path)


def path_exist(path):
    while not client.exists(path):
        path = os.path.dirname(path)
    return path


if __name__ == '__main__':
    client.copy_from_local('D:\\py_work\\hadoop_demo\\app\\media\\2021-07-09-11\\info.txt', '/input/info.txt')
