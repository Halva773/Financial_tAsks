import pymysql
import pandas as pd
import random
import uuid

arr = ""

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
        sql = f"""CREATE TABLE IF NOT EXISTS {table_name} (ID varchar(100) key, arr varchar(721), len varchar(100), 
        sum varchar(255), middle varchar(255)); """
        cursor.execute(sql)
        connection.commit()
        if input("Показать существующие таблицы?") == "Y":
            sql = "SHOW tables"
            print("[INFO] Count of tables: ", cursor.execute(sql),
                  f"\n[INFO] Table '{table_name.upper()}' was created")
            for tables in cursor:
                print(tables)
        connection.close()


def write_in_db(db_name, table_name, array):
    connection = pymysql.Connect(host="localhost",
                                 user="root",
                                 password="Admin1234!",
                                 charset='utf8mb4',
                                 db=db_name,
                                 cursorclass=pymysql.cursors.DictCursor)
    list = array.split(", ")
    sum = 0
    for item in list:
        sum += int(item)
    sql = f"""INSERT INTO {table_name.upper()} (ID, arr, len, sum, middle) VALUES(%s, %s, %s, %s, %s)"""
    with connection.cursor() as cursor:
        cursor.execute(sql, (uuid.uuid4(), array, str(len(list)), str(sum), str(sum//len(list))))
        connection.commit()
        connection.close()


def list_generate():
    global arr
    arr = ""
    for i in range(120):
        arr += f"{random.randint(0, 1000)}, "
    return arr[:-2]


def calculate_list():
    list = list_generate()
    print(list)
    write_in_db(input("Введите название базы данных >>> "),
                input("Введите название таблицы >>> "),
                list)


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
    num = input("""1. Создать базу данных и таблицу в MySQL.
2. Сгенерировать список, найти длину списка, сумму элементов списка и среднее арифметическое, все результаты сохранить в MySQL
и вывести в консоль.
3. Сохранить данные из MySQL в Excel и вывести на экран.
4. Вывести все данные из MySQL\n>>> """)
    while num != "quit":
        if num == "1":
            num = input("1. Создать базу данных.\n2. Создать таблицу\n3. Отмена действия\n>>> ")
            if num == "1":
                create_database(input("Введите названте базы данных\n>>> "))
            elif num == "2":
                create_table(input("Введите название базы данных\n>>> "), input("Введите название таблицы\n>>> "))
        elif num == "2":
            calculate_list()
        elif num == "3":
            base_name = input("Введите название базы данных >>> ")
            table_name = input("Введитн название таблицы >>> ")
            print(read_from_db(base_name, table_name))
            id = []
            arr = []
            len = []
            sum = []
            middle = []
            for line in read_from_db(base_name, table_name):
                id.append(line["ID"])
                arr.append(line["arr"])
                len.append(line["len"])
                sum.append(line["sum"])
                middle.append(line["middle"])
            data = pd.DataFrame({
                "ID": id,
                'arr': arr,
                'len': len,
                'sum': sum,
                'middle': middle
            })
            excel_name = input('Введите название таблицы: ')
            data.to_excel(f'./{excel_name}.xlsx')
            writer = pd.ExcelWriter(f"./{excel_name}.xlsx", engine='xlsxwriter')
            data.to_excel(writer)
            writer.save()
        elif num == "4":
            print(read_from_db(input("Введите название базы данных >>> "),
                         input("Введите название таблицы >>> ")))
        num = input()


if __name__ == "__main__":
    main()
