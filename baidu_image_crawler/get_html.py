#coding=utf-8
from selenium import webdriver
from selenium.webdriver import ActionChains
import bs4
import time
import os

URL = 'http://image.baidu.com/search/index?ct=201326592&cl=2&lm=-1&nc=1&ipn=r&tn=baiduimage&rps=3&pv=&word=%E6%AC%A7%E7%BE%8E%E6%80%A7%E6%84%9F%E7%94%B7%E6%98%9F&ofr=%E7%94%B7%E6%98%9F%E6%80%A7%E6%84%9F%E7%85%A7&ie=utf-8&istype=2&z=0&fm=rs6'
PAGE_NUM = 7
OUTPUT = unicode('D:/SMU\PornDetector/download_url/baidu_url/欧美性感男星/欧美性感男星.lst', 'utf-8')
OUTPUT_HTML = unicode('D:/SMU\PornDetector/download_url/baidu_url/欧美性感男星/欧美性感男星.html', 'utf-8')


def get_html(url, page):
    driver = webdriver.Chrome('D:/Program Files (x86)/chromedriver_win32/chromedriver.exe')
    driver.set_window_size(1920, 1080)

    # 关键词：性感男人 by URL编码
    driver.get(url)

    time.sleep(5)
    # 通过Xpath找到More button
    load_more = driver.find_element_by_xpath('//*[@id="pageMore"]')#baidupic
    print('gggggggg')
    a = 0
    stop = False;
    while(True):
        scroll_num = 0
        while (load_more.get_attribute('style')!="visibility: visible;"):
            driver.execute_script("scrollTo(0,document.body.scrollHeight);")
            sleep_time = 5
            time.sleep(sleep_time)
            scroll_num += 1
            if scroll_num > 10:
                stop = True
                break
        # print('start')
        # 模拟用户行为点击加载更多按键
        if stop:
            break
        actions = ActionChains(driver)
        actions.move_to_element(load_more)
        actions.click(load_more)
        actions.perform()

        driver.execute_script("scrollTo(0,document.body.scrollHeight);")
        sleep_time = 5
        print(sleep_time)
        time.sleep(sleep_time)
        print(load_more.get_attribute('style'))
        a += 1
        print(a)

    html = driver.execute_script("return document.getElementsByTagName('body')[0].innerHTML")
    driver.close()
    html = html.encode('UTF-8')
    print(html)
    # 将爬到的html写入文件
    mkdir(os.path.dirname(OUTPUT_HTML))
    with open(OUTPUT_HTML, 'w') as fw:
        fw.write(html)
        fw.close
    print("end")
    return html


def mkdir(path):
    path = path.strip()
    path = path.rstrip('\\')
    is_exists = os.path.exists(path)
    if is_exists is not True:
        print path
        os.makedirs(path)
    else:
        print('exists!')


if __name__ == '__main__':
    # f = open('test.html', 'r')
    # html = f.read()
    # f.close()
    try:
        html = get_html(URL, PAGE_NUM)
    except Exception as e:
        print(e)
    soup = bs4.BeautifulSoup(html)
    div = soup.find('div', id='imgid')
    li_ist = div.findAll('li', 'imgitem')
    mkdir(os.path.dirname(OUTPUT))
    with open(OUTPUT, 'w') as fw:
        for li in li_ist:
            try:
                img_url = li.get('data-objurl')
                fw.write(img_url + '\n')
            except Exception as e:
                print(e)
        fw.close()
        # print(img_url)

    # print(div)