import pymysql

"""username = "lungusilviu18"
pas = "123qweasd"""


def login_info(username, pas):
    connection = pymysql.connect(host='139.162.181.85',
                                 user='yello',
                                 password='A!3a09b86cc',
                                 database='licentaDB')

    cursor = connection.cursor()
    sql = cursor.execute(("SELECT * from users where username = %s and password = %s "), (username, pas))
    data = cursor.fetchone()
    cursor.close()
    return data


def add_user_info(username):
    connection = pymysql.connect(host='139.162.181.85',
                                 user='yello',
                                 password='A!3a09b86cc',
                                 database='licentaDB')

    cursor = connection.cursor()
    sql = cursor.execute(("SELECT * from users where username = %s"), (username))
    data = cursor.fetchone()
    cursor.close()
    return data


def add_user(name, username, password, email, tip_user):
    connection = pymysql.connect(host='139.162.181.85',
                                 user='yello',
                                 password='A!3a09b86cc',
                                 database='licentaDB')

    cursor = connection.cursor()
    sql = cursor.execute(
        "INSERT INTO users (nume, username, password, email, tip_user) VALUES (%s, %s, %s, %s, %s)",
        (name, username, password, email, tip_user))
    connection.commit()
    cursor.close()


def get_users():
    connection = pymysql.connect(host='139.162.181.85',
                                 user='yello',
                                 password='A!3a09b86cc',
                                 database='licentaDB')

    cursor = connection.cursor()
    sql = cursor.execute("SELECT * from users")
    data = cursor.fetchall()
    cursor.close()
    return data


def get_single_user(id):
    connection = pymysql.connect(host='139.162.181.85',
                                 user='yello',
                                 password='A!3a09b86cc',
                                 database='licentaDB')

    cursor = connection.cursor()
    sql = cursor.execute("SELECT * from users where idUser=%s", (id))
    data = cursor.fetchone()
    cursor.close()
    return data


"""nume = "asd"
username = "asd"
password = "asd"
email = "email"
tip_user = "student"
acc_status = "activ"
idUser = "5"""""


def update_user(nume, username, password, email, tip_user, acc_status, idUser):
    connection = pymysql.connect(host='139.162.181.85',
                                 user='yello',
                                 password='A!3a09b86cc',
                                 database='licentaDB')

    cursor = connection.cursor()
    sql = cursor.execute(
        "UPDATE users SET nume=%s, username=%s, password=%s, email=%s, tip_user=%s, activ=%s WHERE idUser=%s",
        (nume, username, password, email, tip_user, acc_status, idUser))
    connection.commit()
    cursor.close()


def delete_usr(id):
    connection = pymysql.connect(host='139.162.181.85',
                                 user='yello',
                                 password='A!3a09b86cc',
                                 database='licentaDB')

    cursor = connection.cursor()
    sql = cursor.execute("DELETE FROM users WHERE idUser=%s", id)
    connection.commit()
    cursor.close()
