# -*- coding: utf-8 -*-
# @Time    : 2018/7/31 上午10:42
# @Author  : WangJuan
# @File    : run.py

"""
运行用例集：
    python3 run.py

# '--allure_severities=critical, blocker'
# '--allure_stories=测试模块_demo1, 测试模块_demo2'
# '--allure_features=测试features'

"""
import sys

import pytest

from Common import Log
from Common import Shell
from Conf import Config
from Common import Email

if __name__ == '__main__':

    # todo 搞清楚这些配置文件是用来干嘛的
    conf = Config.Config()
    log = Log.MyLog()
    log.info('初始化配置文件, path=' + conf.conf_path)

    # todo shell的作用是？
    # 先 生产一个shell实例，后面用
    shell = Shell.Shell()

    # 没啥用，就是取一下配置的路径
    xml_report_path = conf.xml_report_path
    html_report_path = conf.html_report_path

    # 定义测试集
    # 先定义 塞到pytest里面执行的参数
    args = ['-s', '-q', '--alluredir', xml_report_path]

    # todo  这时候为什么要请求pytest.main(args)
    pytest.main(args)

    cmd = 'allure generate %s -o %s' % (xml_report_path, html_report_path)

    try:
        shell.invoke(cmd)
    except Exception:
        log.error('执行用例失败，请检查环境配置')
        raise

    try:
        mail = Email.SendMail()
        mail.sendMail()
    except Exception as e:
        log.error('发送邮件失败，请检查邮件配置')
        raise

