class ENV:
    #被测环境地址
    url = "http://127.0.0.1:8000/"

class DBSql:
    """
    初始化时清除数据库sql语句
    清空：用户、购物车、订单信息
    并插入：测试用户test1
    """
    sql_file = rf'D:\daily_fresh\daily_fresh_demo-master\db.sqlite3'   #r作用是防止\转义
    sql_list = [
        'DELETE FROM df_order_orderdetailinfo',
        'delete from df_order_orderinfo',
        'delete from df_user_userinfo',
        'delete from df_cart_cartinfo',
        "insert into 'df_user_userinfo' VALUES ('46', 'test1', 'b444ac06613fc8d63795be9ad0beaf55011936ac', '898787869@qq.com', '', '', '', '')"

    ]