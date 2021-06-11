import pymysql
from datetime import date, time, datetime, timedelta
import locale


def login_info(username):
    connection = pymysql.connect(host='139.162.181.85',
                                 user='yello',
                                 password='A!3a09b86cc',
                                 database='licentaDB')

    cursor = connection.cursor()
    sql = cursor.execute("SELECT * from users where username = %s", username)
    data = cursor.fetchone()
    cursor.close()
    return data


def add_user_info(username):
    connection = pymysql.connect(host='139.162.181.85',
                                 user='yello',
                                 password='A!3a09b86cc',
                                 database='licentaDB')

    cursor = connection.cursor()
    sql = cursor.execute("SELECT * from users where username = %s", username)
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


def get_active_users():
    connection = pymysql.connect(host='139.162.181.85',
                                 user='yello',
                                 password='A!3a09b86cc',
                                 database='licentaDB')

    cursor = connection.cursor()
    sql = cursor.execute("SELECT * from users where stare_cont='activ'")
    data = cursor.fetchall()
    cursor.close()
    return data


def get_inactive_users():
    connection = pymysql.connect(host='139.162.181.85',
                                 user='yello',
                                 password='A!3a09b86cc',
                                 database='licentaDB')

    cursor = connection.cursor()
    sql = cursor.execute("SELECT * from users where stare_cont='inactiv'")
    data = cursor.fetchall()
    cursor.close()
    return data


def get_single_user(id):
    connection = pymysql.connect(host='139.162.181.85',
                                 user='yello',
                                 password='A!3a09b86cc',
                                 database='licentaDB')

    cursor = connection.cursor()
    sql = cursor.execute("SELECT nume, email, tip_user from users where idUser=%s", id)
    data = cursor.fetchone()
    cursor.close()
    return data


def disable_acc(idUser):
    connection = pymysql.connect(host='139.162.181.85',
                                 user='yello',
                                 password='A!3a09b86cc',
                                 database='licentaDB')

    cursor = connection.cursor()
    sql = cursor.execute("UPDATE users set stare_cont='inactiv' where idUser=%s", idUser)
    connection.commit()
    cursor.close()


def activate_acc(idUser):
    connection = pymysql.connect(host='139.162.181.85',
                                 user='yello',
                                 password='A!3a09b86cc',
                                 database='licentaDB')

    cursor = connection.cursor()
    sql = cursor.execute("UPDATE users set stare_cont='activ' where idUser=%s", idUser)
    connection.commit()
    cursor.close()


def change_password(username, password):
    connection = pymysql.connect(host='139.162.181.85',
                                 user='yello',
                                 password='A!3a09b86cc',
                                 database='licentaDB')

    cursor = connection.cursor()
    sql = cursor.execute("UPDATE users set password=%s where username=%s", (password, username))
    connection.commit()
    cursor.close()


def update_user(nume, email, tip_user, idUser):
    connection = pymysql.connect(host='139.162.181.85',
                                 user='yello',
                                 password='A!3a09b86cc',
                                 database='licentaDB')

    cursor = connection.cursor()
    sql = cursor.execute(
        "UPDATE users SET nume=%s, email=%s, tip_user=%s WHERE idUser=%s",
        (nume, email, tip_user, idUser))
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


def get_acces():
    connection = pymysql.connect(host='139.162.181.85',
                                 user='yello',
                                 password='A!3a09b86cc',
                                 database='licentaDB')

    cursor = connection.cursor()
    sql = cursor.execute(
        "select a.nume, a.idUser, c.nume_sala, b.idSala from users a RIGHT OUTER JOIN accesSali b  ON a.idUser=b.idUser LEFT OUTER JOIN sali c ON b.idSala=c.idSala")
    data = cursor.fetchall()
    cursor.close()
    return data


def delete_access(idUser):
    connection = pymysql.connect(host='139.162.181.85',
                                 user='yello',
                                 password='A!3a09b86cc',
                                 database='licentaDB')

    cursor = connection.cursor()
    sql = cursor.execute("DELETE FROM accesSali WHERE idUser=%s", idUser)
    connection.commit()
    cursor.close()


def delete_responsabil(idUser):
    connection = pymysql.connect(host='139.162.181.85',
                                 user='yello',
                                 password='A!3a09b86cc',
                                 database='licentaDB')

    cursor = connection.cursor()
    sql = cursor.execute("UPDATE sali set responsabil = NULL where responsabil=%s", idUser)
    connection.commit()
    cursor.close()


def get_acces_info(idUser, idSala, zile, timpStart, timpEnd):
    connection = pymysql.connect(host='139.162.181.85',
                                 user='yello',
                                 password='A!3a09b86cc',
                                 database='licentaDB')

    cursor = connection.cursor()
    sql = cursor.execute("SELECT * FROM accesSali where iduser=%s and idSala=%s and zile=%s and timpStart=%s and timpEnd=%s", (idUser, idSala, zile, timpStart, timpEnd))
    data = cursor.fetchone()
    cursor.close()
    return data




def add_acces(idUser, idSala, zile, timpStart, timpEnd):
    connection = pymysql.connect(host='139.162.181.85',
                                 user='yello',
                                 password='A!3a09b86cc',
                                 database='licentaDB')

    cursor = connection.cursor()
    sql = cursor.execute("insert into accesSali(idUser, idSala, zile, timpStart, timpEnd) values (%s,%s,%s,%s,%s)",
                         (idUser, idSala, zile, timpStart, timpEnd))
    connection.commit()
    cursor.close()


def get_idUser(numeUser):
    connection = pymysql.connect(host='139.162.181.85',
                                 user='yello',
                                 password='A!3a09b86cc',
                                 database='licentaDB')

    cursor = connection.cursor()
    sql = cursor.execute("select idUser from users where nume=%s", numeUser)
    data = cursor.fetchone()
    cursor.close()
    return data[0]


def get_acces_for_button(idUser):
    connection = pymysql.connect(host='139.162.181.85',
                                 user='yello',
                                 password='A!3a09b86cc',
                                 database='licentaDB')

    cursor = connection.cursor()
    sql = cursor.execute("SELECT idSala, zile, timpStart, timpEnd FROM accesSali where idUser=%s", idUser)
    data = cursor.fetchall()
    cursor.close()

    return data




def get_acces_for_button1(idUser):
    connection = pymysql.connect(host='139.162.181.85',
                                 user='yello',
                                 password='A!3a09b86cc',
                                 database='licentaDB')

    cursor = connection.cursor()
    sql = cursor.execute("SELECT idSala FROM accesSali where idUser=%s", idUser)
    data = cursor.fetchall()
    cursor.close()

    return data


def adauga_unitate_unitateSala(numeUnitate, idSala):
    connection = pymysql.connect(host='139.162.181.85',
                                 user='yello',
                                 password='A!3a09b86cc',
                                 database='licentaDB')
    verificare_status = ""
    cursor = connection.cursor()
    sql_ver = cursor.execute("select * from unitati where nume_unitate=%s", numeUnitate)
    data = cursor.fetchone()
    if data is None:
        verificare_status = "OK"
        sql = cursor.execute("insert into unitati(nume_unitate) values (%s)", numeUnitate)
        connection.commit()
        sql_ins = cursor.execute("select idUnitate from unitati where nume_unitate=%s", numeUnitate)
        data2 = cursor.fetchone()
        idUnitate = data2[0]
        dataInstalare = get_date()
        sql2 = cursor.execute("insert into unitatiSali(idSala, idUnitate, dataInstalare) values (%s,%s,%s)",
                              (idSala, idUnitate, dataInstalare))
        connection.commit()
        cursor.close()
    else:
        verificare_status = "Exista deja o unitate cu acest nume!"
        cursor.close()
    return verificare_status


"""def test():
    connection = pymysql.connect(host='139.162.181.85',
                                 user='yello',
                                 password='A!3a09b86cc',
                                 database='licentaDB')
    cursor = connection.cursor()
    sql_ins = cursor.execute("select idUser from users where idUser=10")
    data2 = cursor.fetchone()
    print(data2[0])"""


def get_sali_notInUnitatiSali():
    connection = pymysql.connect(host='139.162.181.85',
                                 user='yello',
                                 password='A!3a09b86cc',
                                 database='licentaDB')
    cursor = connection.cursor()
    sql = cursor.execute(
        "select a.idSala, a.nume_sala from sali a LEFT OUTER JOIN unitatiSali b using(idSala) where b.idSala IS NULL")
    data = cursor.fetchall()
    cursor.close()
    return data


def get_responsabili():
    connection = pymysql.connect(host='139.162.181.85',
                                 user='yello',
                                 password='A!3a09b86cc',
                                 database='licentaDB')

    cursor = connection.cursor()
    sql = cursor.execute("select idUser, nume from users where tip_user='profesor'")
    data = cursor.fetchall()
    cursor.close()
    return data


def adauga_sala(nume_sala, cladire, responsabil, numar_locuri, tip_sala):
    connection = pymysql.connect(host='139.162.181.85',
                                 user='yello',
                                 password='A!3a09b86cc',
                                 database='licentaDB')
    verificare_status = ""
    cursor = connection.cursor()
    sql_ver = cursor.execute("select * from sali where nume_sala=%s", nume_sala)
    data = cursor.fetchone()
    if data is None:
        verificare_status = "OK"
        sql = cursor.execute(
            "insert into sali(nume_sala, cladire, responsabil, numar_locuri, tip_sala) values(%s,%s,%s,%s,%s)",
            (nume_sala, cladire, responsabil, numar_locuri, tip_sala))
        connection.commit()
        cursor.close()
    else:
        verificare_status = "Exista deja aceasta sala!"
        cursor.close()
    return verificare_status


# -------------functii timp & data----------------------
def get_date():
    now = datetime.now()
    locale.setlocale(locale.LC_ALL, 'ro')
    data_ro = now.strftime("%A")
    return data_ro


def get_time():
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    return current_time


def time_conversion(time_str):
    time_obj = datetime.strptime(time_str, '%H:%M')
    return time_obj.time()


def time_in_range(start, end):
    now = datetime.now()
    x = str(now.strftime("%H:%M"))
    start = str(time_conversion(start))
    end = str(time_conversion(end))
    if start <= end:
        return start <= x <= end
    else:
        return start <= x or x <= end


"""now = datetime.now()
start_time = str(time_conversion('23:30'))
print(start_time)

end_time = str(time_conversion('01:35'))
print(end_time)
current_time = str(now.strftime("%H:%M"))
print(now.strftime("%H:%M"))
a = time_in_range(start_time, end_time, current_time)
print(a)"""

"""curr = datetime.now()
seq1 = []
for x in range(10):
    curr = curr + timedelta(minutes = 15)
    seq1.append(curr.strftime("%H:%M"))"""
