"""登录模块用自己所学知识编写思路：
前置条件：
1)登录模块都需要打开浏览器实例，所以将浏览器打开实例作为类的属性，后续可以用 类名.实例名  调用
2)由于后续操作每条用例都涉及到隐式等待-->访问被测系统地址-->最大化窗口-->点击登录按钮-->判断是否记住了用户名
3)所以考虑将上述2中的公用步骤放置于类中的__init__方法中，即每实例化一次，程序都会自动调用一次__init__方法
用例步骤：
1）正确的用户名密码，预期为页面特定位置出现”欢迎您“字样（做assert断言）
2）用户名不存在，预期为出现”用户名错误“（做assert断言）
3）密码错误，预期为出现”密码错误“（做assert断言）
用例编写好后，通过实例对象调用类，然后调用类方法（实际就是用例），并传递对应的实参

！！！以上方式也可实现登录模块的用例编写，但是到调用步骤后，无法串联起依次调用，不够灵活，不易维护
！！！且要想结合pytest+allure的用例执行+结果查看，就得使用对应框架
！！！需要注意的是pytest框架的类中不支持__init__方法
！！！且测试用例方法、测试用例.py文件一定要是test开头，类名一定要为Test开头，否则无法识别
"""
# 低版本selenium的适配方式：
# 导入webdriver库的前提是下载了chromedriver驱动
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium import webdriver
import time
class Test_Login:
    #类属性
    service = Service(executable_path="D:\Downloads\chromedriver_win32\chromedriver.exe")  # 指定驱动路径
    driver = webdriver.Chrome(service=service)  # 获取chrome实例，打开浏览器
    #初始化方法
    def __init__(self):
        #用到此前所学的  类名.属性 可以使用类属性
        Test_Login.driver.implicitly_wait(15)  # 全局隐式等待,只需在初始化浏览器时设置一次，后续有页面跳转或重新加载都生效
        Test_Login.driver.get('http://127.0.0.1:8000/') #访问浏览器地址
        Test_Login.driver.maximize_window()   #最大化窗口
        Test_Login.driver.find_element(By.XPATH,"//a[contains(text(),'登录')]").click()  #找到页面的登录按钮的xpath地址并点击
        rem_user = Test_Login.driver.find_element(By.XPATH,"//input[@name='jizhu']") #将“记住用户名”复选框点击状态赋值给变量
        if rem_user.is_selected():  #判断复选框是否被点击,如果被选中则点击复选框，如果没被点击则继续往下
            rem_user.click()
        else:
            pass
    def test_shoping_mall_001(self,*args): #*args形参接收方法调用时的实参
        Test_Login.driver.find_element(By.XPATH,"//input[@placeholder='请输入用户名']").send_keys(args[0]) #输入用户名
        Test_Login.driver.find_element(By.XPATH,"//input[@placeholder='请输入密码']").send_keys(args[1]) #输入密码
        # print(args[0],args[1])
        Test_Login.driver.find_element(By.XPATH, "//input[@value='登录']").click()  #点击登录按钮
        text = Test_Login.driver.find_element(By.XPATH,"//div[@class='login_btn fl']").text #获取登录成功位置的文本值
        # print(actual_text)
        assert "欢迎您" in text, f"预期文本未出现，实际内容：{text}"   #断言“欢迎您”是否出现在文本中，出现即通过
        # input("按回车键退出...")  # 阻塞主线程，手动控制退出
        Test_Login.driver.quit()  #退出浏览器
    def test_shoping_mall_002(self,*args):
        Test_Login.driver.find_element(By.XPATH, "//input[@placeholder='请输入用户名']").send_keys(args[0])  # 输入用户名
        Test_Login.driver.find_element(By.XPATH, "//input[@placeholder='请输入密码']").send_keys(args[1])  # 输入密码
        Test_Login.driver.find_element(By.XPATH, "//input[@value='登录']").click()  # 点击登录按钮
        text = Test_Login.driver.find_element(By.XPATH,"//div[@class='user_error']").text #获取用户名错误的文本
        assert text == '用户名错误'  #断言提示信息是否为“用户名错误”
    def test_shoping_mall_003(self,*args):
        Test_Login.driver.find_element(By.XPATH,"//input[@placeholder='请输入用户名']").send_keys(args[0]) #输入用户名
        Test_Login.driver.find_element(By.XPATH,"//input[@placeholder='请输入密码']").send_keys(args[1]) #输入密码
        Test_Login.driver.find_element(By.XPATH, "//input[@value='登录']").click()  # 点击登录按钮
        text = Test_Login.driver.find_element(By.XPATH,"//div[@class='pwd_error']").text #获取密码错误的文本
        assert text == "密码错误"  #断言提示信息是否为“密码错误”
# case_001 = Test_Login()
# case_001.test_shoping_mall_001('test1','test1')
# time.sleep(5)  #执行2条用例，中间设置等待还是不行？
# case_002 = Test_Login()
# case_002.test_shoping_mall_002('root',123456)
# case_003 = Test_Login()
# case_003.test_shoping_mall_003('test1',123456)
