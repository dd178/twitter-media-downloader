'''
Author: mengzonefire
Date: 2021-09-21 09:20:19
LastEditTime: 2023-03-06 03:25:23
LastEditors: mengzonefire
Description: 命令行交互模块
'''

from task.singlePageTask import SinglePageTask
from task.searchTask import UserSearchTask
from typing import List
from common.text import *
from common.const import *
from common.tools import getUserId, saveEnv, showConfig, setProxy, setCookie, clear
from task.userFollowingTask import UserFollowingTask
from task.userLikesTask import UserLikesTask


def cmdMode(clearScreen=True):
    if clearScreen:
        clear()
    showConfig()
    print(input_ask)
    url_list = []
    while True:
        temp = input()
        if not temp:
            break
        elif temp == '0':
            return
        elif temp == '1':
            setCookie()
            showConfig()
            print(input_ask)
        elif temp == '2':
            setProxy()
            showConfig()
            print(input_ask)
        elif temp == '3':
            config()
            showConfig()
            print(input_ask)
        elif urlChecker(temp):
            url_list.append(temp)
        else:  # 输入错误, 重置
            input(input_warning)
            clear()
            showConfig()
            print(input_ask)
            url_list = []
    if url_list:
        startCrawl(url_list)
    if input(continue_ask):
        cmdMode()


def config():  # 设置菜单
    clear()
    while True:
        set = input(download_settings_ask)
        if set == '0':
            break
        elif set == '1':
            setType()
        elif set == '2':
            maxConcurrency()
        elif set == '3':
            quotedStatus()
        elif set == '4':
            retweetedStatus()
        elif set == '5':
            mediaStatus()
        else:
            input(input_num_warning)
    clear()


def setType():  # 设置下载类型
    clear()
    while True:
        only = ''.join(set(list(input(set_type_ask))))
        if only == '0':
            return
        elif set(only) <= set('1234'):
            type = []
            for i in only:
                if i == '1':
                    type.append('photo')
                elif i == '2':
                    type.append('animated_gif')
                elif i == '3':
                    type.append('video')
                elif i == '4':
                    type.append('full_text')
            setContext('type', '&'.join(type))
            saveEnv()
            break
        elif only == '5':
            type = ['photo', 'animated_gif', 'video', 'full_text']
            setContext('type', '&'.join(type))
            saveEnv()
            break
        else:
            input(input_num_warning)
    clear()


def maxConcurrency():  # 设置线程数
    clear()
    while True:
        num = input(max_concurrency_ask)
        if num == '0':
            return
        else:
            try:
                setContext('concurrency', int(num))
                clear()
                saveEnv()
                break
            except ValueError:
                input(input_num_warning)
    clear()


def mediaStatus():  # 设置非媒体
    clear()
    while True:
        set = input(media_status_ask)
        if set == '0':
            return
        elif set == '1':
            setContext('media', False)
            saveEnv()
            break
        elif set == '2':
            setContext('media', True)
            saveEnv()
            break
        else:
            input(input_num_warning)
    clear()


def quotedStatus():  # 设置引用
    clear()
    while True:
        set = input(quoted_status_ask)
        if set == '0':
            return
        elif set == '1':
            setContext('quoted', True)
            saveEnv()
            break
        elif set == '2':
            setContext('quoted', False)
            saveEnv()
            break
        else:
            input(input_num_warning)
    clear()


def retweetedStatus():  # 设置转推
    clear()
    while True:
        set = input(retweeted_status_ask)
        if set == '0':
            return
        elif set == '1':
            setContext('retweeted', True)
            saveEnv()
            break
        elif set == '2':
            setContext('retweeted', False)
            saveEnv()
            break
        else:
            input(input_num_warning)
    clear()


def startCrawl(urlList: List):
    dl_path = getContext('dl_path')
    if not os.path.exists(dl_path):
        os.mkdir(dl_path)
    for url in urlList:
        if not url:
            continue
        if urlChecker(url):
            print('\n不支持: {}'.format(url))
        else:
            print('\n正在提取: {}'.format(url))
            urlHandler(url)


def urlChecker(url: str):
    return p_twt_link.findall(url) or p_user_link.findall(url) or url[0] == '@'


def urlHandler(url: str):
    media = getContext('media')
    # singlePage
    twt_link = p_twt_link.findall(url)
    if twt_link:
        userName = twt_link[0][0]
        twtId = int(twt_link[0][1])
        SinglePageTask(userName, twtId).start()
        return

    user_link = p_user_link.findall(url)
    if user_link:
        # userHomePage
        func = url.split('/')[-1]
        userName = user_link[0]
        url = f'@{userName}'
        if func == 'media':
            # userMediaPage
            media = True
        elif func == 'likes':
            # userLikesPage
            UserLikesTask(userName, twtId, media).start()
            return
        elif func == 'following':
            # userFollowingPage
            UserFollowingTask(userName, twtId).start()
            return

    # searchPage
    if url[0] == '@':
        if 'advanced=' in url:
            advanced = url.split('&')[-1].replace('advanced=', '')
            userName = url.split('&')[0].replace('@', '')
            date = None
        elif '&' in url and len(url.split('&')) == 2:
            advanced = None
            userName = url.split('&')[0].replace('@', '')
            date = [url.split('&')[1].split('|')[0],
                    url.split('&')[1].split('|')[1]]
        elif '&' not in url:
            advanced = None
            userName = url[1:]
            date = None
        else:
            print(f'无法解析：{url}')
            return
        if userName:
            userId = getUserId(userName)
            if userId:
                UserSearchTask(userName, userId, date, advanced, media).start()
        elif advanced:
            userName = 'advanced_search'
            UserSearchTask(userName, None, date, advanced, media).start()
