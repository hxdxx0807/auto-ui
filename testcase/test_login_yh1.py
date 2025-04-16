"""
优化版本1：
前置条件：
1）当前登录模块类都要用到打开浏览器->访问被测地址->最大化窗口->全局隐式等待
2）定义类的前置条件 setup_class,将上述1中的公用步骤作为前置条件统一执行，即调用类时会首先执行前置条件语句
执行步骤：
1）正确的用户名密码，预期为页面特定位置出现”欢迎您“字样（做assert断言），并退出登录，否则下一条用例无法找到登录入口
2）用户名不存在，预期为出现”用户名错误“（做assert断言）
3）密码错误，预期为出现”密码错误“（做assert断言）

！！！当前版本从运行角度来看可行，但还可以通过pytest框架来优化
"""
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium import webdriver
import time

class Test_Login:   #声明登录模块的类

    def setup_class(self):   #pytest框架对于类级别的前置条件，即执行类下的用例（其他方法）前会先执行这里
        self.service = Service(executable_path="D:\Downloads\chromedriver_win32\chromedriver.exe")  # 指定驱动路径
        self.driver = webdriver.Chrome(service=self.service)  # 获取chrome实例，打开浏览器
        self.driver.get("http://127.0.0.1:8000/")  #访问被测系统地址
        self.driver.maximize_window()  #最大化窗口
        self.driver.implicitly_wait(10)  #全局隐式等待

    def teardown_class(self):  #pytest框架对于类级别的后置条件，即执行完类下的所有用例才会执行这里
        self.driver.quit()  #关闭浏览器

    def test_shoping_mall_001(self):
        self.driver.find_element(By.XPATH,"//a[contains(text(),'登录')]").click()  #点击登录
        rember_user = self.driver.find_element(By.XPATH,"//input[@name='jizhu']")  #获取记住用户名复选框状态
        if rember_user.is_selected():  #如果复选框被选中
            rember_user.click()  #就点击复选框，使其不被选中
        else:
            pass
        self.driver.find_element(By.XPATH,"//input[@placeholder='请输入用户名']").send_keys("test1")  #输入用户名
        self.driver.find_element(By.XPATH,"//input[@placeholder='请输入密码']").send_keys("test1") #输入密码
        self.driver.find_element(By.XPATH,"//input[@value='登录']").click() #点击登录
        text = self.driver.find_element(By.XPATH,"//div[@class='login_btn fl']").text  #获取登录成功后特定位置的文本
        self.driver.find_element(By.XPATH,"//a[contains(text(),'退出')]").click()
        assert text == "欢迎您：test1 | 退出"  #断言特定位置的文本是否等于字样，等于认为通过，不等于就失败

    def test_shoping_mall_002(self):
        self.driver.find_element(By.XPATH,"//a[contains(text(),'登录')]").click()  #点击登录
        self.driver.find_element(By.XPATH, "//input[@placeholder='请输入用户名']").send_keys("daixiuxiu")  # 输入用户名
        self.driver.find_element(By.XPATH, "//input[@placeholder='请输入密码']").send_keys("test1")  # 输入密码
        self.driver.find_element(By.XPATH, "//input[@value='登录']").click()  # 点击登录
        text = self.driver.find_element(By.XPATH,"//div[@class='user_error']").text  #获取用户名错误后的提示信息
        assert text == "用户名错误"   #断言用户名错误后的提示信息是否为xxx

    def test_shoping_mall_003(self):
        # self.driver.find_element(By.XPATH,"//a[contains(text(),'登录')]").click()  #点击登录
        self.driver.find_element(By.XPATH, "//input[@placeholder='请输入用户名']").send_keys("test1")  # 输入用户名
        self.driver.find_element(By.XPATH, "//input[@placeholder='请输入密码']").send_keys("123456")  # 输入密码
        self.driver.find_element(By.XPATH, "//input[@value='登录']").click()  # 点击登录
        text = self.driver.find_element(By.XPATH,"//div[@class='pwd_error']").text  #获取密码错误后的提示信息
        assert text == "密码错误"  #断言密码错误后的提示信息是否为xxx