import requests
import random
from lxml import etree
from multiprocessing import Pool
import time

SEARCH_URL = 'http://91porn.com/search_result.php?search_id=%{}&search_type=search_videos&page=21'
URL = 'http://91porn.com/v.php?next=watch&page={}'
PAGE_NUM = 4306
START = 70
END = 80
FIlE_MIDDLE_NAME = 'page ' + str(START) + ' to ' + str(END)
DL_URL_TXT_FILE = 'urls_file/txt/' + FIlE_MIDDLE_NAME + '.txt'
DL_URL_TXT_FILE_with_title = 'urls_file/txt/' + FIlE_MIDDLE_NAME + ' with title' + '.txt'
DL_HTML_FILE = 'urls_file/html/' + FIlE_MIDDLE_NAME + '.html'
DL_FILE_DIR = 'movies/' + FIlE_MIDDLE_NAME + '/'
POOL_NUM = 30

def random_ip():
    a=random.randint(1,255)
    b=random.randint(1,255)
    c=random.randint(1,255)
    d=random.randint(1,255)
    return(str(a)+'.'+str(b)+'.'+str(c)+'.'+str(d))

def get_all_page_urls():
    all_urls = [URL.format(i) for i in range(1, PAGE_NUM+1)]
    print('all_urls: ', all_urls)
    print('+'*100)
    return all_urls

def get_page_item_urls(page_url):
    headers = {'Accept-Language': 'zh-CN,zh;q=0.9',
               'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.106 Safari/537.36',
               'X-Forwarded-For': random_ip(), 'referer': page_url,
               'Content-Type': 'multipart/form-data; session_language=cn_CN'}
    res = requests.get(page_url, headers=headers).text
    html = etree.HTML(res)
    find_urls = html.xpath('//*[@class="listchannel"]/div/a/@href')
    print('find_urls : ', find_urls)
    print('-'*100)
    return find_urls

def get_dl_video(item_url):
    headers = {'Accept-Language': 'zh-CN,zh;q=0.9',
               'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.106 Safari/537.36',
               'X-Forwarded-For': random_ip(), 'referer': item_url,
               'Content-Type': 'multipart/form-data; session_language=cn_CN'}
    res = requests.get(item_url, headers=headers).text
    html = etree.HTML(res)
    try:
        video_url = html.xpath('//video[@id="vid"]/source/@src')
        video_title = html.xpath('//div[@id="viewvideo-title"]/text()')[0]
        video_title = video_title.strip(' ').strip('\t').strip('\n')
        if len(video_url) != 0 and video_title is not None:
            video_url = video_url[0]
            print('video_url : ', video_url)
            print('*'*100)
            dict_data = {'video_title': video_title, 'video_url': video_url}
            with open(DL_URL_TXT_FILE_with_title, 'a') as f:
                f.write(str(dict_data)+'\n')
            with open(DL_URL_TXT_FILE, 'a') as f:
                f.write(video_url + '\n')
            with open(DL_HTML_FILE, 'a') as f:
                f.write('<p align="center"><a href="{}" target="_Blank">{}</a></p>'.format(video_url, video_title))
                # f.write('''
                # <p>{}</p>
                # <video width="640" height="320" controls><source src="{}"  type="video/mp4"><source src="movie.ogg"  type="video/ogg">
                # </video><br><br>'''.format(video_title, video_url))
            return video_url
        print('list is null.')
    except Exception as e:
        print(e)


def count_url_num():
    with open(DL_URL_TXT_FILE, 'r') as f:
        all = f.readlines()
    num = len(all)
    print('Crawled {} movie urls.'.format(num))
    print('-'*150)
    return num

def read_text_to_dict():
    with open(DL_URL_TXT_FILE_with_title, 'r') as f:
        a = f.readlines()
        dicts = [eval(i.strip('\n')) for i in a]
        print(dicts)
        print('#'*150)
        return dicts


def send_to_wechat():
    import itchat
    itchat.auto_login()
    itchat.send_file(DL_HTML_FILE, 'filehelper')
    print('success send P{} to wechat.'.format(DL_HTML_FILE))


def test(search):
    #bad
    from urllib import parse
    format_search = parse.quote(search)
    search_url = SEARCH_URL.format(format_search)
    headers = {'Accept-Language': 'zh-CN,zh;q=0.9',
               'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.106 Safari/537.36',
               'X-Forwarded-For': random_ip(), 'referer': search_url,
               'Content-Type': 'multipart/form-data; session_language=cn_CN'}
    res = requests.get(search_url, headers=headers).text
    print(res)

if __name__ == '__main__':
    t1 = time.time()
    now = time.ctime()
    print('start : \n')

    #即将爬的页数,自己设置
    some_page_urls = get_all_page_urls()[START:END+1]
    #获取所有item_url
    all_item_urls = []
    for page_url in some_page_urls:
        lst = get_page_item_urls(page_url)
        for i in lst:
            all_item_urls.append(i)
    print('all_item_urls : ', all_item_urls)
    print('='*100)
    time.sleep(1)
    # 建立进程池，自己设置数量
    p = Pool(POOL_NUM)
    #获取所有dl——url并保存再txt文档
    try:
        p.map(get_dl_video, all_item_urls)
        p.close()
        p.join()
    except Exception as e:
        print('$' * 150)
        print(e)
        print('$'*150)
    finally:
        count_url_num()
        t2 = time.time()
        print('end ', now)
        print('cost time: ', t2-t1)
        send_to_wechat()

#this is for test function
# if __name__ == '__main__':
#     test(search='广州')

