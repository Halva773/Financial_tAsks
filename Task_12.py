import pymysql
import numpy as np
import pandas as panda

matrix_one = []
matrix_two = []

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


def create_table(db_name, table_name):
    connection = connect(db_name)
    print("OK")
    with connection.cursor() as cursor:
        sql = f"""CREATE TABLE IF NOT EXISTS {table_name} (matrix varchar(300));"""
        cursor.execute(sql)
        connection.commit()
        if input("Показать существующие таблицы?") == "Y":
            sql = "SHOW tables"
            print("[INFO] Count of tables: ", cursor.execute(sql),
                  f"\n[INFO] Table '{table_name.upper()}' was created")
            for tables in cursor:
                print(tables)
        connection.close()


def write_in_db(db_name, table_name, matrix):
    connection = pymysql.Connect(host="localhost",
                                 user="root",
                                 password="Admin1234!",
                                 charset='utf8mb4',
                                 db=db_name,
                                 cursorclass=pymysql.cursors.DictCursor)
    sql = f"""INSERT INTO {table_name.upper()} (matrix) VALUES(%s);"""
    with connection.cursor() as cursor:
        cursor.execute(sql, (matrix))
        connection.commit()
        connection.close()


def base_variant():
    global matrix_two, matrix_one
    if len(matrix_two) > 0 and len(matrix_one) > 0:
        matrix_one = np.array(matrix_one)
        matrix_two = np.array(matrix_two)
        print(f"Первый массив\n{matrix_one}\nВторой массив:\n{matrix_two}")
        print("Размерность первого массива: ", len(matrix_one), len(matrix_one[0]))
        print("Размерность второго массива: ", len(matrix_two), len(matrix_two[0]))
        try:
            print(f"Произведение матриц:\n{matrix_two*matrix_one}")
        except:
            print("Данные матрицы нельзя перемножить")

    else:
        print("Вы не можете выполнить это действие, так как вы не задали массив")


def reading(database, table):
    matrix = []
    colomn = int(input("Введите количество колонок> "))
    row = int(input("Введите количество рядов> "))
    for colomns in range(row):
        arr = list(map(int, input().split()))
        while len(arr) != colomn:
            print("Неверное количество столбцов, введите ещё раз\n")
            arr = list(map(int, input().split()))
        matrix.append(arr)
    matrix = np.array(matrix)
    write_in_db(database, table, str(matrix))
    return matrix


def excel(bd_name, tablename):
    ex = str(input("Придумайте название excel файлу: ")) + ".xlsx"
    connections = connect(bd_name)
    df = panda.read_sql_query(f"SELECT * FROM {tablename}", connections)
    df.to_excel(ex, sheet_name="задание_12", index=False)
    connections.close()


def main():
    num = input("""1. Создать базу данных и таблицу в MySQL.
2. Ввод данных с клавиатуры и сохранение матриц в MySQL с последующим выводом в консоль.
3. Решение базового варианта, сохранить результаты и вывести их из MySQL.
4. Сохранить данные из MySQL в Excel и вывести их в консоль из Excel.
quit - выйти из консоли\n> """)
    while num != "quit":
        if num == "1":
            num = input("1. Создать базу данных.\n2. Создать таблицу\n3. Отмена действия\n>>> ")
            if num == "1":
                create_database(input("Введите названте базы данных\n>>> "))
            elif num == "2":
                create_table(input("Введите название базы данных\n>>> "), input("Введите название таблицы\n>>> "))
        elif num == "2":
            global matrix_two, matrix_one
            database = input("Введите название базы данных, с которой хотите работать> ")
            table = input("Введите название таблицы, с которой хотите работать> ")
            print("Запись первой матрицы")
            matrix_one = reading(database, table)
            print("Запись второй матрицы\n")
            matrix_two = reading(database, table)
            print(f"{matrix_one},\n{matrix_two}")
        elif num == "3":
            base_variant()
        elif num == "4":
            database = input("Введите название базы данных, с которой хотите работать> ")
            table = input("Введите название таблицы, с которой хотите работать> ")
            excel(database, table)
        num = input("Введите следующую команду\n> ")

if __name__ == "__main__":
    main()