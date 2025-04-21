import sqlite3
from common.log import log   #从common软件包的log文件中导入log属性
from settings import DBSql  #从settings文件中导入DBSql类

class MysqlAuto:
    def __init__(self):    #类的初始化方法，每次实例化对象调用类都会自动先执行这个方法
        """连接sqlite数据库"""
        self.con = sqlite3.connect(DBSql.sql_file)
        #创建一个cursor游标并作为属性，用于后续执行sql命令
        self.cursor = self.con.cursor()
        log.info(f'Connected to database:{DBSql.sql_file}')

    def __del__(self):
        """对象资源被释放时触发"""
        try:
            self.cursor.close()   #关闭游标
            self.con.close()   #关闭连接
            log.info('Database connection closed')
        except Exception:
            pass  # 静默处理所有异常

    #显示释放资源，只有明确调用才会触发
    # def close(self):
    #     self.cursor.close()
    #     self.con.close()
    #     log.info("数据库连接已关闭")

    def execute(self,sql_list):    #此处定义的形参sql_list为列表，接收实例方法被调用时传的实参，即sql语句列表
        """执行sql语句,支持字符串或列表"""
        try:   #尝试执行，即能正常执行就走这里的代码块
            for sql in sql_list:   #循环遍历sql语句列表
                log.info(f'sql:{sql}')   #打印info级别日志
                self.cursor.execute(sql)   #通过连接数据库时的游标去执行列表中的每一条sql语句
                log.debug(self.cursor.fetchall())  #将sql语句执行结果作为debug级别日志进行打印
            self.con.commit()   #提交sql语句修改
            return self.cursor.fetchall()   #将sql执行结果作为方法返回值
        except Exception as e:    #不能执行就走这里的处理，Exception为异常的统称，将其重命名为e
            log.error(f'执行sql出现错误，异常为{e}')
            raise e   #抛出异常信息

if __name__ == "__main__":
    # MysqlAuto.execute(['select * from df_user_userinfo'])  #不能直接用类名来调用实例方法，否则实例方法中的第一个self参数会接收到传的实参
    MysqlAuto().execute(["select * from df_user_userinfo"]) #这种方式也可以，因为MysqlAuto()相当于已经调用了类并实例化对象，只是没赋值给变量
    # db = MysqlAuto()   #通过调用类，先实例化对象，把实例对象的内存地址作为实参传递给实例方法的self
    # db.execute(["select * from df_user_userinfo"])   #再通过  实例名.方法(实参)  调用实例方法，并将实参传递给实例方法中第二个形参开始接收
    # # db.close()
    # # db.execute(DBSql.sql_list)