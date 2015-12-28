# -*- coding: utf-8 -*-
# Author: Mou Shuai
import inspect
import ctypes
import threading
import urllib2
import sys
import random
import os
max_thread = 10
import time
# initial lock
lock = threading.RLock()
INPUT_FOLDER = 'D:/SMU/PornDetector/download_url/baidu_url'
OUTPUT_FOLDER = 'D:/SMU/PornDetector/download_image/baidu'


class Downloader(threading.Thread):
    def __init__(self, url, save_file):
        self.url = url
        self.save_file = save_file
        threading.Thread.__init__(self)

    def run(self):
        """
            test
        """
        with lock:
            print 'starting: %s' % self.getName()
        self._download()

    def _download(self):
        """
            working on it
        """
        # req = urllib2.Request(self.url)
        # add HTTP Header(RANGE) to find the data
        time.sleep(2)
        try:
            f = urllib2.urlopen(self.url)
            # initial the offset address of document object
            size = int(f.info().getheaders('Content-Length')[0])
            print(size)
            if size > 5000:
                try:
                    fw = open(self.save_file, 'wb')
                    fw.write(f.read())
                    fw.close()
                    sys.stdout.write('done.\n')
                except Exception as e:
                    print(e)
            else:
                print('invalid image')
        except Exception as e:
            print(e)


def _async_raise(tid, exctype):
    """raises the exception, performs cleanup if needed"""
    if not inspect.isclass(exctype):
        raise TypeError("Only types can be raised (not instances)")
    res = ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, ctypes.py_object(exctype))
    if res == 0:
        raise ValueError("invalid thread id")
    elif res != 1:
        # """if it returns a number greater than one, you're in trouble,
        # and you should call it again with exc=NULL to revert the effect"""
        ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, 0)
        raise SystemError("PyThreadState_SetAsyncExc failed")


def mkdir(path):
    path = path.strip()
    path = path.rstrip('\\')
    is_exists = os.path.exists(path)
    if is_exists is not True:
        print path
        os.makedirs(path)
    else:
        print('exists!')


def main(thread=8):
    thread = thread if thread <= max_thread else max_thread
    file_list = os.listdir(INPUT_FOLDER)
    for file_name in file_list:
        os_folder = os.path.join(INPUT_FOLDER, file_name)
        if os.path.isdir(os_folder) is True:
            save_folder = os.path.join(OUTPUT_FOLDER, file_name)
            mkdir(save_folder)
            for lst in os.listdir(os_folder):
                if lst.endswith('.lst'):
                    os_lst = os.path.join(os_folder, lst)
                    with open(os_lst, 'r') as fh:
                        lines = fh.readlines()
                        fobj = []
                        if lines.__len__() < thread:
                            plist = []
                            for line in lines:
                                try:
                                    url = line.split(' ')[0]

                                    img_name = url[url.rindex('/') + 1:]
                                    print(img_name)
                                    save_name = lst[: lst.index('.lst')] + '_' + img_name

                                    save_file = os.path.join(save_folder, save_name)
                                    fobj = open(save_file, 'wb')
                                    t = Downloader(url, fobj)
                                    plist.append(t)
                                except Exception as e:
                                    print(e)

                            for t in plist:
                                try:
                                    t.start()
                                except Exception as e:
                                    print(e)
                            for t in plist:
                                try:
                                    t.join()
                                except Exception as e:
                                    print(e)
                            print('Complete!')
                        else:
                            plist = []
                            for i in range(lines.__len__()):
                                try:
                                    line = lines[i]
                                    url = line.split(' ')[0]
                                    img_name = url[url.rindex('/') + 1:]
                                    print(img_name)
                                    save_name = lst[: lst.index('.lst')] + '_' + img_name
                                    save_file = os.path.join(save_folder, save_name).strip()
                                    print(url)
                                    t = Downloader(url, save_file)
                                    # fobj.close()
                                    plist.append(t)
                                except Exception as e:
                                    print(e)
                                if (i + 1) % thread == 0 or i >= lines.__len__() - 1:
                                    for t in plist:
                                        try:
                                            t.setDaemon(True)
                                            t.start()
                                        except Exception as e:
                                            print(e)
                                    for t in plist:
                                        try:
                                            t.join(1.0)
                                        except Exception as e:
                                            print(e)
                                    for t in plist:
                                        if t.isAlive():
                                            print(t.ident)
                                        os.system('kill %s' % t.ident)
                                        # _async_raise(t.ident, SystemExit)
                                        print(t.isAlive())
                                    plist = []
                                    print('Complete!')


if __name__ == '__main__':
    #url = 'http://mvvideo2.meitudata.com/53f1ede46ee2d531.mp4'
    main(thread=8)