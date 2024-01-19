import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import os
import logging
import sys
import threading


def get_file_links(url):
    """ 爬取给定URL的网页，提取所有文件链接 """
    file_links = []
    dir_links = []
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')

        for link in soup.find_all('a'):
            href = link.get('href')
            
            if href and '.' in href:  # 检查是否为文件
                file_links.append(urljoin(url, href))
            elif href and href.endswith('/'):
                dir_links.append(urljoin(url, href))

    except requests.RequestException as e:
        print(f"Error fetching {url}: {e}")

    return file_links, dir_links

def download_file(url, folder_path):
    """ 下载单个文件到指定文件夹 """
    # try:
    #     response = requests.get(url)
    #     if response.status_code == 200:
    #         file_name = url.split('/')[-1]
    #         file_path = os.path.join(folder_path, file_name)
    #         with open(file_path, 'wb') as file:
    #             file.write(response.content)
    #         print(f"Downloaded {file_name} to {folder_path}")
    #     else:
    #         print(f"Failed to download {url}")

    # except requests.RequestException as e:
    #     print(f"Error downloading {url}: {e}")
    
    logger = loggerInit()
    try:
        # print(f"Downloading {url} to {folder_path}")
        logger.info(f"Downloading {url} to {folder_path}")
        os.system(f"wget -P {folder_path} {url}")
    except Exception as e:
        # print(f"Error downloading {url}: {e}")
        logger.error(f"Error downloading {url}: {e}")


def loggerInit():
        
    # 创建日志器logger并将其日志级别设置为DEBUG
    logger = logging.getLogger("downloader")
    logger.setLevel(logging.DEBUG)
    # 创建一个流处理器handler并将其日志级别设置为DEBUG
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(logging.DEBUG)
    # 创建一个格式化器formatter并将其添加到处理器handler中
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    handler.setFormatter(formatter)
    # 为日志器logger添加上面创建好的处理器handler
    logger.addHandler(handler)

    return logger


# def download_files_from_url(url, folder_path):
#     """ 从URL下载文件和目录 """
#     file_links, dir_links = get_file_links(url)

#     # 创建文件夹（如果不存在）
#     if not os.path.exists(folder_path):
#         os.makedirs(folder_path)

#     # 下载当前目录中的文件
#     for file_link in file_links:
#         download_file(file_link, folder_path)

#     # 递归处理子目录
#     for dir_link in dir_links:
#         dir_name = dir_link.split('/')[-2]
#         new_folder_path = os.path.join(folder_path, dir_name)
#         download_files_from_url(dir_link, new_folder_path)

def download_files_from_url(url, folder_path):
    """ 从URL下载文件和目录，使用多线程加速下载 """
    file_links, dir_links = get_file_links(url)

    # 创建文件夹（如果不存在）
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    threads = []
    # 使用线程下载当前目录中的文件
    for file_link in file_links:
        thread = threading.Thread(target=download_file, args=(file_link, folder_path))
        thread.start()
        threads.append(thread)

    # 等待所有线程完成
    for thread in threads:
        thread.join()

    # 递归处理子目录
    for dir_link in dir_links:
        dir_name = dir_link.split('/')[-2]
        new_folder_path = os.path.join(folder_path, dir_name)
        download_files_from_url(dir_link, new_folder_path)


if __name__ == "__main__":
    # from down import download_files_from_url
    # 主程序
    base_url = "http://piweb.ooirsn.uw.edu/das/"  # 更改为目标网址
    base_folder_path = "downloaded_files"  # 本地存储的根文件夹
    download_files_from_url(base_url, base_folder_path)
    
