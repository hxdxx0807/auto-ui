import pytest
from common.sql import MysqlAuto
from settings import DBSql
from selenium.webdriver.chrome.service import Service
from selenium import webdriver

from common.log import log  #从common软件包的log文件中导入log属性

# 替代传统的setup_class/teardown_class方法
@pytest.fixture(scope='class')   #类级别：每个测试类执行前初始化一次‌，并在类中所有测试方法执行完毕后执行清理操作
def login():
    #前置条件语句
    service = Service(executable_path=r"D:\Downloads\chromedriver_win32\chromedriver.exe")  # 指定驱动路径，r"路径"防止被转义
    driver = webdriver.Chrome(service=service)  # 获取chrome实例，打开浏览器
    log.debug("打开浏览器")   #以debug级别打印日志
    driver.get("http://127.0.0.1:8000/")  # 访问被测系统地址
    log.debug("最大化窗口")   #以debug级别打印日志
    driver.maximize_window()  # 最大化窗口
    driver.implicitly_wait(10)  # 全局隐式等待
    MysqlAuto().execute(DBSql.sql_list)   #前置条件中先执行sql初始化环境的语句
    yield driver   #yield生成器函数，执行到这里暂停，并将driver作为返回值
    log.debug("关闭浏览器")   #以debug级别打印日志
    #后置条件语句
    driver.quit()  #关闭浏览器