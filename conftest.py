import sys, os
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

import pytest
from selenium.webdriver.chrome.service import Service
from selenium import webdriver

# 替代传统的setup_class/teardown_class方法
@pytest.fixture(scope='class')   #类级别：每个测试类执行前初始化一次‌，并在类中所有测试方法执行完毕后执行清理操作
def login():
    #前置条件语句
    service = Service(executable_path=r"D:\Downloads\chromedriver_win32\chromedriver.exe")  # 指定驱动路径，r"路径"防止被转义
    driver = webdriver.Chrome(service=service)  # 获取chrome实例，打开浏览器
    driver.get("http://127.0.0.1:8000/")  # 访问被测系统地址
    driver.maximize_window()  # 最大化窗口
    driver.implicitly_wait(10)  # 全局隐式等待
    yield driver   #yield生成器函数，执行到这里暂停，并将driver作为返回值
    #后置条件语句
    driver.quit()  #关闭浏览器