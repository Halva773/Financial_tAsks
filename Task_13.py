import pymysql
import pandas as panda
import random as rnd


def connect(db_name):
    connection = pymysql.Connect(host="localhost",
                                 user="root",
                                 password="Admin1234!",
                                 charset='utf8mb4',
                                 db=db_name,
                                 cursorclass=pymysql.cursors.DictCursor)
    print("Подключение к базе данных прошло успешно")
    return connection


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


def create_table(db_name, table_name, action):
    connection = connect(db_name)
    print("OK")
    with connection.cursor() as cursor:
        if action == "1":
            sql = f"""CREATE TABLE IF NOT EXISTS {table_name} (full_name varchar(100), short_name varchar(50), lens varchar(30));"""
        elif action == "2":
            sql = f"""CREATE TABLE IF NOT EXISTS {table_name} (array varchar(700));"""
        cursor.execute(sql)
        connection.commit()
        if input("Показать существующие таблицы?") == "Y":
            sql = "SHOW tables"
            print("[INFO] Count of tables: ", cursor.execute(sql),
                  f"\n[INFO] Table '{table_name.upper()}' was created")
            for tables in cursor:
                print(tables)
        connection.close()


def write_in_db(db_name, table_name, action="1"):
    global full_name, short_name
    connection = pymysql.Connect(host="localhost",
                                 user="root",
                                 password="Admin1234!",
                                 charset='utf8mb4',
                                 db=db_name,
                                 cursorclass=pymysql.cursors.DictCursor)
    if action == "1":
        sql = f"""INSERT INTO {table_name.upper()} (full_name, short_name) VALUES(%s, %s);"""
        with connection.cursor() as cursor:
            cursor.execute(sql, (full_name, short_name))
            connection.commit()
            connection.close()
    elif action == "2":
        sql = f"""INSERT INTO {table_name.upper()} (full_name, short_name, lens) VALUES(%s, %s, %s);"""
        with connection.cursor() as cursor:
            cursor.execute(sql, (full_name, short_name, f"{len(full_name)}, {len(short_name)}"))
            connection.commit()
            connection.close()
    elif action == "3":
        sql = f"""INSERT INTO {table_name.upper()} (array) VALUES(%s);"""
        with connection.cursor() as cursor:
            cursor.execute(sql, (str(array)))
            connection.commit()
            connection.close()


def excel(bd_name, tablename):
    ex = str(input("Придумайте название excel файлу: ")) + ".xlsx"
    connections = connect(bd_name)
    df = panda.read_sql_query(f"SELECT * FROM {tablename}", connections)
    df.to_excel(ex, sheet_name="задание_13", index=False)
    connections.close()


def main():
    num = input("""1. Создать базу данных и таблицу в MySQL.
2. Решение среднего варианта, сохранить результаты и вывести их из MySQL.
3. Сохранить данные из MySQL в Excel и вывести их в консоль из Excel.
quit -  Выйти из консольного меню\n> """)
    while num != "quit":
        if num == "1":
            if num == "1":
                num = input("1. Создать базу данных.\n2. Создать таблицу\n3. Отмена действия\n>>> ")
                if num == "1":
                    create_database(input("Введите названте базы данных\n>>> "))
                elif num == "2":
                    num = input("1. Таблица для ФИО\n2. Таблица для списка\n> ")
                    create_table(input("Введите название базы данных\n>>> "), input("Введите название таблицы\n>>> "), num)
        elif num == "2":

            database = input("Введите название базы данных, с которой хотите работать> ")
            table = input("Введите название таблицы, с которой хотите работать> ")
            num = input( """1. Ввод строки с клавиатуры и вывод результата. Сохранить данные и результаты в MySQL и вывести в консоль.
2. Подсчитать и вывести длину исходной строки и получившейся строки. Сохранить результаты в MySQL и вывести в консоль.
3. Сгенерировать список со значениями от 0 до 100 и отсортировать его в обратном порядке. Сохранить данные и результаты в MySQL и вывести в консоль
quit - выйти в преведущее консольное меню""")
            while num != "quit":
                global full_name, short_name, array
                if num == "1":
                    full_name = input("Введите фио: ").split()
                    short_name = f"{full_name[0]} {full_name[1][0]}.{full_name[2][0]}."
                    print(short_name)
                    write_in_db(database, table)
                elif num == "2":
                    if len(full_name) < 1 and len(short_name) < 1:
                        print("Для начала необходимо задать строки (команда 1)")
                    else:
                        print(len(full_name), print(len(short_name)))
                        write_in_db(database, table, action="2")
                elif num == "3":
                    arr = [rnd.randint(0, 100) for i in range(30)]
                    arr.sort(reverse=True)
                    print(arr)
                    write_in_db(database, table)
                num = input("Введите новую комнаду\n> ")
        elif num == "3":
            database = input("Введите название базы данных, с которой хотите работать> ")
            table = input("Введите название таблицы, с которой хотите работать> ")
            excel(database, table)
        num = input("Введите следующую команду")

full_name = ""
short_name = ""
array = []
if __name__ == "__main__":
    main()