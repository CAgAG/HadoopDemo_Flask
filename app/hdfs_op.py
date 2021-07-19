import os

"""
需要安装 pyhdfs 库
命令: pip3 install pyhdfs
"""
import pyhdfs


def show_path(path):
    """
    :param path: hadoop 路径
    :return: 打印路径内容
    """
    print('当前目录: ', path)
    for f in client.listdir(path):
        print(f, end=' ')
    print()


if __name__ == '__main__':
    # 连接hadoop
    # hosts: hadoop连接
    # username: 主机用户名
    client = pyhdfs.HdfsClient(hosts='192.168.174.10:50070', user_name='root')

    # 浏览目录: 浏览根目录
    path = '/'
    file_list = client.listdir(path)
    print(file_list)

    # 创建文件夹: 在根目录创建 input2 文件夹
    dirname = '/input2'
    client.mkdirs(dirname)
    show_path('/')

    # 上传文件: 在 /input2 目录上传 LICENSE.txt 文件
    local_path = 'D:/py_work/hadoop_demo/app/media/input/LICENSE.txt'
    hadoop_path = '/input2/LICENSE.txt'
    client.copy_from_local(localsrc=local_path, dest=hadoop_path)
    show_path(os.path.dirname(hadoop_path))

    # 下载文件: 将 /input2/LICENSE.txt 文件下载到本地 D:/py_work/hadoop_demo/app/media/input/LICENSE2.txt
    local_path = 'D:/py_work/hadoop_demo/app/media/input/LICENSE2.txt'
    hadoop_path = '/input2/LICENSE.txt'
    client.copy_to_local(src=hadoop_path, localdest=local_path)

    # 删除文件: 删除 /input2/LICENSE.txt 文件
    hadoop_path = '/input2/LICENSE.txt'
    client.delete(hadoop_path)
    show_path(os.path.dirname(hadoop_path))

    """
    终端输出结果: 
    ['input']
    当前目录:  /
    input input2 
    当前目录:  /input2
    LICENSE.txt 
    当前目录:  /input2
    """