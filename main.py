'''
Author: mengzonefire
Date: 2021-09-21 15:48:35
LastEditTime: 2021-09-22 10:04:07
LastEditors: mengzonefire
Description: 程序主函数入口
'''
from const import *
from text import *
from common.exceptHandler import except_handler
from common.inital import inital
import sys
import os


def main():
    inital()


if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        except_handler(e)
        if input(reset_ask):
            if sys.platform in ['win32', 'win64']:  # 判断是否为win平台
                os.system('cls')
            else:
                os.system('clear')
            main()