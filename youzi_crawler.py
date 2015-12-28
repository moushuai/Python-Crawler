import urllib2
from time import sleep
import random
import requests
import bs4

ROOT_URL = 'http://www.youzi4.cc/'
CHANNEL = 'siwameitui/'
PAGE_PREFIX = 'list_3_'
OUTPUT = 'D:/SMU\PornDetector/download_url/prondetector_youzi_sexy_url/prondetector_youzi_siwameitui_url.txt'
# headers = {
#     "Connection" : "close",  # another way to cover tracks
#     "User-Agent" : "Mozilla/5.0"
# }
USER_AGENTS_FILE = 'user_agents.txt'


def load_user_agents(uafile=USER_AGENTS_FILE):
    uas = []
    with open(uafile, 'rb') as fh:
        for line in fh.readlines():
            if line:
                uas.append(line.strip()[1:-1-1])
    random.shuffle(uas)
    return uas


def get_page_url_list(index_url, uas):
    ua = random.choice(uas)
    headers = {"Connection": "close", "User-Agent": ua}
    sleep(random.randint(1, 3))
    print(index_url)
    content = requests.get(index_url, timeout=(20.0, 60), headers=headers)
    soup = bs4.BeautifulSoup(content.text)
    div = soup.find('div', 'pages')
    page_url_list = []
    url_end_index = div.contents.__len__() - 4
    # page_start_index = int(div.contents[url_start_index].text)
    page_end_index = int(div.contents[url_end_index].text)
    for i in range(page_end_index):
        page_url = ROOT_URL + CHANNEL + PAGE_PREFIX + str(i+1) + '.html'
        print(page_url)
        page_url_list.append(page_url)
    return page_url_list


def get_title_url_list(page_url, uas):
    ua = random.choice(uas)
    headers = {"Connection": "close", "User-Agent": ua}
    sleep(random.randint(1, 3))
    print(page_url)
    content = requests.get(page_url, timeout=(20.0, 60), headers=headers)
    soup = bs4.BeautifulSoup(content.text)
    ul = soup.find('div', 'pic-list1 clearfix').find('ul', 'clearfix')
    title_url_list = []
    print(ul.contents.__len__())
    for li in ul.children:
        if li != '\n':
            # print(li)
            href = li.find('a').get('href')
            # print(href)
            title_url = ROOT_URL + href
            print(title_url)
            title_url_list.append(title_url)
    return title_url_list


def get_image_url_list(title_url, uas):
    ua = random.choice(uas)
    headers = {"Connection": "close", "User-Agent": ua}
    sleep(random.randint(1, 3))
    print(title_url)
    content = requests.get(title_url, timeout=(20.0, 60), headers=headers)
    soup = bs4.BeautifulSoup(content.text)
    div = soup.find('div', 'pages')
    image_url_list = []
    if div.contents.__len__() < 4:
        return image_url_list.append(title_url)
    url_end_index = div.contents.__len__() - 4
    print(div.contents.__len__())
    # print(div.contents[url_end_index-1])
    page_end_index = int(div.contents[url_end_index].text)
    image_url_list.append(title_url)
    for i in range(page_end_index - 1):
        image_url = title_url.replace('.html', '_' + str(i + 2) + '.html')
        image_url_list.append(image_url)
        # print(image_url)
    return image_url_list


def get_image_download_url(image_url, uas):
    ua = random.choice(uas)
    headers = {"Connection": "close", "User-Agent": ua}
    # random.ra
    sleep(random.randint(1, 3))
    content = requests.get(image_url, timeout=(20.0, 60), headers=headers)
    soup = bs4.BeautifulSoup(content.text)
    img = soup.find('img', id='bigimg')
    # print(img)
    return img.get('data-original')


if __name__ == '__main__':
    # s = requests.session()
    uas = load_user_agents()
    with open(OUTPUT, 'w') as fh:
        title_url_list = []
        page_url_list = get_page_url_list((ROOT_URL + CHANNEL), uas)
        for page_url in page_url_list:
            try:
                page_title_url_list = get_title_url_list(page_url, uas)
                for title_url in page_title_url_list:
                    title_url_list.append(title_url)
            except Exception as e:
                print(e)
        print('fetch the title url list done!')
        image_url_list = []
        for title_url in title_url_list:
            try:
                page_image_url_list = get_image_url_list(title_url, uas)
                for image_url in page_image_url_list:
                    image_url_list.append(image_url)
            except Exception as e:
                print(e)
        print('fetch the image url list done!')
        for image_url in image_url_list:
            try:
                img = get_image_download_url(image_url, uas)
                if img is not None:
                    print img
                    fh.write(img + '\n')
            except Exception as e:
                print(e)

    fh.close()
    print('Done')

    # get_page_url_list((ROOT_URL + CHANNEL))
    # get_title_url_list((ROOT_URL + CHANNEL))
    # for page_url in page_url_list:
    # get_image_url_list('http://www.youzi4.cc//xingganmeinv/7226.html')
    # get_image_download_url('http://www.youzi4.cc/xingganmeinv/7180.html')