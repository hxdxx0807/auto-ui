"""
存放项目涉及到目录结构
"""

import os

BASE_DIR = os.path.dirname(os.path.dirname(__file__))   #获取项目所在路径，如果实际项目路径发生变化，这里也会获取新路径
LOG_DIR = os.path.join(BASE_DIR,"log")   #日志存放路径，join方法是在第一个参数（目录）下拼接一个目录,不自动创建目录
if not os.path.exists(LOG_DIR):   #判断是否存在目录，不存在就创建
    os.makedirs(LOG_DIR)
ALLURE_IMG_DIR = os.path.join(LOG_DIR,"image_allure")   #allure报告截图目录   join不会自动创建目录，只做拼接
if not os.path.exists(ALLURE_IMG_DIR):   #判断是否存在目录，不存在就创建
    os.makedirs(ALLURE_IMG_DIR)
if __name__ == "__main__":
    print(BASE_DIR)
    print(LOG_DIR)
    print(ALLURE_IMG_DIR)