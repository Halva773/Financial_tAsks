import pymysql
from random import randint
import pandas as panda

arr1 = {randint(0, 100) for i in range(100)}
arr2 = set()


def connect():
    db_name = input("Введите название базы данных")
    connections = pymysql.connect(
        host="localhost",
        port=3306,
        user="root",
        db=db_name,
        password="Admin1234!",
        cursorclass=pymysql.cursors.DictCursor)
    print("подключение к бд прошло успешно...")
    return connections


def create_table(db_name, table_name):
    connection = connect()
    print("OK")
    with connection.cursor() as cursor:
        sql = f"""CREATE TABLE IF NOT EXISTS {table_name} (lots_1 varchar(500), lots_2 varchar(500), lens varchar(30), 
        belonging varchar(10), common varchar(500), new_lots varchar(500));"""
        cursor.execute(sql)
        connection.commit()
        if input("Показать существующие таблицы?") == "Y":
            sql = "SHOW tables"
            print("[INFO] Count of tables: ", cursor.execute(sql),
                  f"\n[INFO] Table '{table_name.upper()}' was created")
            for tables in cursor:
                print(tables)
        connection.close()


def create_database(db_name):
    connection = connect()
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


def write_in_db(table_name, datas, bool=True):
    global arr1, arr2
    connection = connect()
    if bool:
        sql = f"""INSERT INTO {table_name.upper()} (lots_1, lots_2) VALUES(%s, %s);"""
        with connection.cursor() as cursor:
            cursor.execute(sql, (arr1, arr2))
            connection.commit()
            connection.close()
    else:
        sql = f"""INSERT INTO {table_name.upper()} (lots_1, lots_2, lens, belonging, common, new_lots) VALUES(
        %s, %s, %s, %s, %s, %s);"""
        with connection.cursor() as cursor:
            cursor.execute(sql, (arr1, arr2))
            connection.commit()
            connection.close()



def generate():
    global arr1, arr2
    arr2 = set(map(int, input().split()))
    print(arr1, "\n", arr2)
    num = input("Провести вычисления с записью в SQL?\n1. Da\n2. Net")
    if num == "1":
        operate()
    else:
        write_in_db(input("Введите название базы данных"),
                    input("Введите название таблицы"))


def operate():
    global arr1, arr2
    arr2 = set(map(int, input().split()))
    for item in arr1:
        print(item, end=" ")
    print("\n")
    for item in arr2:
        print(item, end="")
    lens = [len(arr1), len(arr2)]
    print(f"Длина первого множества - {lens[0]}. Длина второго множества - {lens[1]}")
    belonging = []
    for item in arr1:
        if item in arr2:
            belonging.append(item)
    print(f"Общие элементы: {belonging}.\nПринадлежность {len(belonging)/lens[1]*100}%")
    new_arr = [set(list(arr1)[1:-2]), set(list(arr2)[1:-2])]
    print(f"Множества с удалёнными элементами - {new_arr[0]}; {new_arr[1]}")
    write_in_db(input("Название таблицы - "), )



def excel(db_name, db_table_name):
    ex = input("введите название excel файла: ") + ".xlsx"
    connection = connect()
    df = panda.read_sql_query(f"SELECT * FROM {db_table_name}", connection)
    df.to_excel(ex, sheet_name="задание_10", index=False)
    connection.close()


def main():
    num = input("""1. Создать базу данных и таблицу в MySQL.
2. Ввести и сгенерировать множества, сохранить их и вывести из MySQL.
3. Выполнить все операции, сохранить результаты выполнения операций и вывести их из MySQL.
4. Сохранить данные из MySQL в Excel и вывести их в консоль из Excel.""")
    while num != "num":
        if num == "1":
            num = input("1. Создать базу данных.\n2. Создать таблицу\n3. Отмена действия\n>>> ")
            if num == "1":
                create_database(input("Введите названте базы данных\n>>> "))
            elif num == "2":
                create_table(input("Введите название базы данных\n>>> "), input("Введите название таблицы\n>>> "))
        elif num == "2":
            generate()
        elif num == "3":
            operate()
        elif num == "4":
            db_name = input("Название базы данных: ")
            table_name = input("Название таблицы: ")
            excel(db_name, table_name)
            print(read_from_db(db_name, table_name))
        num = input("Next command: ")


if __name__ == "__main__":
    main()