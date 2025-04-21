import allure
from selenium.webdriver import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


class BasePage:
    def __init__(self, driver):
        self.driver = driver
        self.actions = ActionChains(driver)

    @allure.step("等待元素可见：{locator}")
    def wait_until_visible(self, locator, timeout=10):
        try:
            return WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located(locator)
            )
        except TimeoutException:
            allure.attach(self.driver.get_screenshot_as_png(), "元素不可见截图", allure.attachment_type.PNG)
            raise Exception(f"元素 {locator} 在 {timeout} 秒内未可见")

    @allure.step("等待元素可点击：{locator}")
    def wait_until_clickable(self, locator, timeout=10):
        try:
            return WebDriverWait(self.driver, timeout).until(
                EC.element_to_be_clickable(locator)
            )
        except TimeoutException:
            allure.attach(self.driver.get_screenshot_as_png(), "元素不可点击截图", allure.attachment_type.PNG)
            raise Exception(f"元素 {locator} 在 {timeout} 秒内不可点击")

    @allure.step("鼠标左键点击元素：{locator}")
    def click_element(self, locator):
        element = self.wait_until_clickable(locator)
        self.actions.click(element).perform()
        allure.attach(self.driver.get_screenshot_as_png(), "点击后截图", allure.attachment_type.PNG)

    @allure.step("在元素 {locator} 输入内容：{text}")
    def input_text(self, locator, text):
        element = self.wait_until_visible(locator)
        element.clear()
        element.send_keys(text)
        allure.attach(self.driver.get_screenshot_as_png(), "输入后截图", allure.attachment_type.PNG)