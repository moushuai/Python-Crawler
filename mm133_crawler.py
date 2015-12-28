import urllib2
from time import sleep
import random
import requests
import bs4

ROOT_URL = 'http://www.mm131.com/'
CHANNEL = 'xinggan/'
PAGE_PREFIX = 'list_6_'
OUTPUT = 'D:/SMU\PornDetector/download_url/prondetector_youzi_sexy_url/prondetector_mm131_sexy_url.txt'
headers = {
    "Connection" : "close",  # another way to cover tracks
    "User-Agent" : "Mozilla/5.0"
}
proxy = {"http": "http://username:p3ssw0rd@10.10.1.10:3128"}


def get_page_url_list(index_url):
    print(index_url)
    sleep(random.randint(1, 3))
    content = requests.get(index_url, timeout=(20.0, 60), headers=headers)
    soup = bs4.BeautifulSoup(content.text)
    div = soup.find('dd', 'page')
    page_url_list = []
    # print(div.contents)
    href = div.contents[div.contents.__len__() - 1].get('href')

    page_end_index = int(href[href.find(PAGE_PREFIX) + PAGE_PREFIX.__len__():href.find('.html')])
    # print(url_end_index)
    # # page_start_index = int(div.contents[url_start_index].text)
    # page_end_index = int(div.contents[url_end_index].text)
    page_url_list.append(index_url)
    for i in range(page_end_index - 1):
        page_url = ROOT_URL + CHANNEL + PAGE_PREFIX + str(i+2) + '.html'
        print(page_url)
        page_url_list.append(page_url)
    return page_url_list


def get_title_url_list(page_url):
    print(page_url)
    sleep(random.randint(1, 3))
    content = requests.get(page_url, timeout=(20.0, 60), headers=headers)
    soup = bs4.BeautifulSoup(content.text)
    dd_list = soup.find('dl', 'list-left public-box').find_all('dd')
    dd_list.remove(dd_list[dd_list.__len__() - 1])
    title_url_list = []
    # title_url_list.append(page_url)
    # print(ul.contents.__len__())
    for dd in dd_list:
        # print(li)
        title_url = dd.find('a').get('href')
        # print(href)
        print(title_url)
        title_url_list.append(title_url)
    return title_url_list


def get_image_url_list(title_url):
    print(title_url)
    sleep(random.randint(1, 3))
    content = requests.get(title_url, timeout=(20.0, 60), headers=headers)
    soup = bs4.BeautifulSoup(content.text)
    href_list = soup.find('div', 'content-page').find_all('a', 'page-en')
    image_url_list = []
    # image_url_list.append(title_url)
    for href in href_list:
        image_url = ROOT_URL + CHANNEL + href.get('href')
        image_url_list.append(image_url)
        print(image_url)
    return image_url_list


def get_image_download_url(image_url):
    sleep(random.randint(1, 3))
    # requests.
    content = requests.get(image_url, timeout=(20.0, 60), headers=headers)
    soup = bs4.BeautifulSoup(content.text)
    img = soup.find('div', 'content-pic').find('img')
    # print(img.get('src'))
    return img.get('src')


if __name__ == '__main__':
    s = requests.session()
    s.keep_alive = False
    with open(OUTPUT, 'w') as fh:
        title_url_list = []
        page_url_list = get_page_url_list((ROOT_URL + CHANNEL))
        for page_url in page_url_list:
            try:
                page_title_url_list = get_title_url_list(page_url)
                for title_url in page_title_url_list:
                    title_url_list.append(title_url)
            except Exception as e:
                print(e)
        print('fetch the title url list done!')
        image_url_list = []
        for title_url in title_url_list:
            try:
                page_image_url_list = get_image_url_list(title_url)
                for image_url in page_image_url_list:
                    image_url_list.append(image_url)
            except Exception as e:
                print(e)
        print('fetch the image url list done!')
        for image_url in image_url_list:
            try:
                img = get_image_download_url(image_url)
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
    # get_image_url_list('http://www.mm131.com/xinggan/2248.html')
    # get_image_download_url('http://www.mm131.com/xinggan/2248.html')