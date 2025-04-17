"""
在第2版优化的基础上再继续优化：
在项目根目录下新建文件conftest.py（固定名称），将前置条件和后置条件放进该文件中
"""

import pytest
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium import webdriver
import time

class Test_Login:
    # #前置条件  调用类时先执行前置条件
    # def setup_class(self):
    #     self.service = Service(executable_path="D:\Downloads\chromedriver_win32\chromedriver.exe")  # 指定驱动路径
    #     self.driver = webdriver.Chrome(service=self.service)  # 获取chrome实例，打开浏览器
    #     self.driver.get("http://127.0.0.1:8000/")  # 访问被测系统地址
    #     self.driver.maximize_window()  # 最大化窗口
    #     self.driver.implicitly_wait(10)  # 全局隐式等待
    # #后置条件   类中用例执行完后再执行后置条件
    # def teardown_class(self):
    #     self.driver.quit()

    # 定义参数集，一般为类下用例的公共参数，本例中如'username,password,result'
    #创建数据集，每条数据集代表一条用例的传参
    # 每1个元组代表1条用例的传参,依次获取
    @pytest.mark.parametrize('username,password,result',[
        ('test1','test1','欢迎您：test1 | 退出'),
        ('dxx','test1','用户名错误'),
        ('test1',123456,'密码错误')
    ],
    #定义依次执行的用例名称
    ids=(
            'test_shoping_mall_001',
            'test_shoping_mall_002',
            'test_shoping_mall_003'
    ))
    def test_shoping_mall(self,username,password,result,login):   #login参数接收conftest文件中login的返回值driver
        #登录模块用例的部分公共操作步骤，只是传参不同
        driver = login
        driver.get("http://127.0.0.1:8000/")  # 访问被测系统地址
        driver.find_element(By.XPATH,"//a[contains(text(),'登录')]").click()
        driver.find_element(By.XPATH,"//input[@placeholder='请输入用户名']").send_keys(username) #获取xpath地址，输入用户名
        driver.find_element(By.XPATH,"//input[@placeholder='请输入密码']").send_keys(password)  #获取xpath地址，输入密码
        rember_user = driver.find_element(By.XPATH,"//input[@name='jizhu']")  #获取“记住用户名”复选框状态
        if rember_user.is_selected():  #如果被选中
            rember_user.click()  #就点击一次取消选中
        else:  #没被选中就继续往下执行
            pass
        time.sleep(2)
        driver.find_element(By.XPATH,"//input[@value='登录']").click()  #点击登录

        #登录模块用例的不同操作步骤，用if判断来确定执行
        #登录成功用例的断言操作：
        if '欢迎您' in result:
            text = driver.find_element(By.XPATH,"//div[@class='login_btn fl']").text
            driver.find_element(By.XPATH,"//a[contains(text(),'退出')]").click()
            assert text == result
        #用户名错误用例的断言操作：
        elif '用户名错误' in result:
            text = driver.find_element(By.XPATH,"//div[@class='user_error']").text
            assert text == result
        #密码错误用例的断言操作
        elif '密码错误' in result:
            text = driver.find_element(By.XPATH,"//div[@class='pwd_error']").text
            assert text == result