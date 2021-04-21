import pymysql
em = "freelinew1996@gmail.com"
pas = "123qweasd"
def login_info(em, pas):
    connection = pymysql.connect(host='139.162.181.85',
                                 user='yello',
                                 password='A!3a09b86cc',
                                 database='licentaDB')

    cursor = connection.cursor()
    sql = cursor.execute(("SELECT * from testTable where email = %s and password = %s "), (em, pas))
    data = cursor.fetchone()
    return data
print(login_info(em, pas))


