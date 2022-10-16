import pymysql
import pandas as pd
import uuid
from math import pi


r = 0

def create_database(db_name):
    connection = pymysql.Connect(host="localhost",
                                 user="root",
                                 password="Admin1234!",
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)
    with connection.cursor() as cursor:
        sql = f"""CREATE DATABASE IF NOT EXISTS {db_name}"""
        cursor.execute(sql)
        connection.commit()
        if input("Показать существующие базы данных? ") == "Y":
            sql = "SHOW DATABASES"
            print("Count of Databases: ", cursor.execute(sql), f"\nDatabase {db_name} was created")
            for db in cursor:
                print(db)
        connection.close()


def create_table(db_name, table_name):
    connection = pymysql.Connect(host="localhost",
                                 user="root",
                                 password="Admin1234!",
                                 charset='utf8mb4',
                                 db=db_name,
                                 cursorclass=pymysql.cursors.DictCursor)
    print("OK")
    with connection.cursor() as cursor:
        sql = f"""CREATE TABLE IF NOT EXISTS {table_name} (ID varchar(100) key, radius varchar(30), sqare varchar(
        30), diameter varchar(30), len varchar(30));"""
        cursor.execute(sql)
        connection.commit()
        if input("Показать существующие таблицы?") == "Y":
            sql = "SHOW tables"
            print("[INFO] Count of tables: ", cursor.execute(sql),
                  f"\n[INFO] Table '{table_name.upper()}' was created")
            for tables in cursor:
                print(tables)
        connection.close()


def write_in_db(db_name, table_name, count_all, r):
    connection = pymysql.Connect(host="localhost",
                                 user="root",
                                 password="Admin1234!",
                                 charset='utf8mb4',
                                 db=db_name,
                                 cursorclass=pymysql.cursors.DictCursor)
    sql = f"""INSERT INTO {table_name.upper()} (ID, radius, sqare, diameter, len) VALUES(%s, %s, %s, %s, %s)"""
    with connection.cursor() as cursor:
        if count_all:
            cursor.execute(sql, (uuid.uuid4(), str(r), str(pi*r*r), str(2*r), str(2*pi*r)))
        else:
            cursor.execute(sql, (uuid.uuid4(), str(r), "None", "None", "None"))
        connection.commit()
        connection.close()


def read_from_db(db_name, table_name):
    connection = pymysql.Connect(host="localhost",
                                 user="root",
                                 password="Admin1234!",
                                 charset='utf8mb4',
                                 db=db_name,
                                 cursorclass=pymysql.cursors.DictCursor)
    sql = f"""SELECT * FROM {table_name}"""
    with connection.cursor() as cursor:
        cursor.execute(sql)

    datas = []
    for data in cursor.fetchall():
        datas.append(data)
    connection.close()
    return datas


def main():
    global r
    num = input("""1. Создать базу данных и таблицу в MySQL.
2. Задать значения для вычислений с клавиатуры, сохранить их и вывести из MySQL.
3. Вычислить площадь круга, длину окружности, диаметр и радиус. Результаты сохранить в MySQL.
4. Сохранить данные из MySQL в Excel и вывести на экран.\n>>> """)
    while num != "quit":
        if num == "1":
            if num == "1":
                num = input("1. Создать базу данных.\n2. Создать таблицу\n3. Отмена действия\n>>> ")
                if num == "1":
                    create_database(input("Введите названте базы данных\n>>> "))
                elif num == "2":
                    create_table(input("Введите название базы данных\n>>> "), input("Введите название таблицы\n>>> "))
        elif num == "2":
            r = input("Введите радиус")
            write_in_db(input("Введите название базы данных >>> "),
                        input("Введите название таблицы >>> "),
                        False, r)
        elif num == "3":
            if r != 0:
                write_in_db(input("Введите название базы данных >>> "),
                            input("Введите название таблицы >>> "),
                            True, int(r))
            else:
                write_in_db(input("Введите название базы данных >>> "),
                            input("Введите название таблицы >>> "),
                            True, int(input("Введите значение радиуса")))
        elif num == "4":
            base_name = input("Введите название базы данных >>> ")
            table_name = input("Введитн название таблицы >>> ")
            print(read_from_db(base_name, table_name))
            id = []
            radius = []
            sqare = []
            diameter = []
            len = []
            for line in read_from_db(base_name, table_name):
                id.append(line["ID"])
                radius.append(line["radius"])
                sqare.append(line["sqare"])
                diameter.append(line["diameter"])
                len.append(line["len"])
            data = pd.DataFrame({
                "ID": id,
                'radius': radius,
                'sqare': sqare,
                'diameter': diameter,
                'len': len
            })
            excel_name = input('Введите название таблицы: ')
            data.to_excel(f'./{excel_name}.xlsx')
            writer = pd.ExcelWriter(f"./{excel_name}.xlsx", engine='xlsxwriter')
            data.to_excel(writer)
            writer.save()
        num = input("Введите следующую команду: ")




if __name__ == "__main__":
    main()