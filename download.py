from pa91 import *
import requests
from multiprocessing import Pool
import time
import os


def read_dl_urls():
    with open(DL_URL_TXT_FILE_with_title, 'r') as f:
        lines = [eval(i.strip('\n')) for i in f.readlines()]
        urls_num = len(lines)
        print('dl_urls : ', lines)
        print('Number of dl_urls is {}'.format(urls_num))
        print('+' * 100)
        return lines, urls_num


def download_movie(line):
    try:
        if not os.path.exists(DL_FILE_DIR):
            os.makedirs(DL_FILE_DIR)
        # s = dl_url.split('=')
        # name = DL_FILE_DIR + s[-2] + '.mp4'
        dl_url = line.get('video_url')
        name = 'movies' + line.get('video_title').strip() + '.mp4'
        if os.path.exists(name):
            print('already exists {}'.format(name))
            return
        else:
            try:
                print('begin download_movie : ', name)
                headers = {'Accept-Language': 'zh-CN,zh;q=0.9',
                           'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.106 Safari/537.36',
                           'X-Forwarded-For': random_ip(), 'referer': dl_url,
                           'Content-Type': 'multipart/form-data; session_language=cn_CN'}
                res = requests.get(dl_url, headers=headers)
                content = res.content
                with open(name, 'wb') as f:
                    f.write(content)
                print('#' * 150)
                print('finish download_movie : ', name)
                print('#' * 150)
            except Exception as e:
                print(e)
    except Exception as e:
        print(e)


def count_movie_num():
    lst = os.listdir(DL_FILE_DIR)
    num = len(lst)
    print('Download {} movies.'.format(num))
    print('-' * 150)
    return num


def main_download():
    t1 = time.time()
    now = time.ctime()
    print('start : \n')
    lines, urls_num = read_dl_urls()
    # 建立进程池
    p = Pool(2)
    try:
        # download_movie
        p.map(download_movie, lines)
        p.close()
        p.join()
        t2 = time.time()
    except Exception as e:
        print(e)
    download_movie_num = count_movie_num()
    if urls_num == download_movie_num:
        print('-' * 150)
        print('Finish download all the movies.')
        print('-' * 150)
    else:
        print('-' * 150)
        print('There have {} movies not download.'.format(urls_num - download_movie_num))
        print('-' * 150)
    print('end ', now)
    print('cost time: ', t2 - t1)


if __name__ == '__main__':
    main_download()