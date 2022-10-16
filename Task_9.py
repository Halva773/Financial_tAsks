import pandas as pd
import pymysql
import uuid


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
        sql = f"""CREATE TABLE IF NOT EXISTS {table_name} (ID varchar(70) key, specialization varchar(70), name varchar(50), studentnumber varchar(10), groupnmb varchar(30));"""
        cursor.execute(sql)
        connection.commit()
        if input("Показать существующие таблицы?") == "Y":
            sql = "SHOW tables"
            print("[INFO] Count of tables: ", cursor.execute(sql),
                  f"\n[INFO] Table '{table_name.upper()}' was created")
            for tables in cursor:
                print(tables)
        connection.close()


def write_in_db(db_name, table_name, specialization, name, studentID, group):
    connection = pymysql.Connect(host="localhost",
                                 user="root",
                                 password="Admin1234!",
                                 charset='utf8mb4',
                                 db=db_name,
                                 cursorclass=pymysql.cursors.DictCursor)
    sql = f"""INSERT INTO {table_name.upper()} (ID, specialization, name, studentnumber, groupnmb) VALUES(%s, %s, %s, %s, %s);"""
    with connection.cursor() as cursor:
        cursor.execute(sql, (uuid.uuid4(), specialization, name, studentID, group))
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
    num = input("""1. Создать базу данных и таблицу в MySQL.
2. Ввести необходимые данные (ID, Направление подготовки, ФИО, номер студенческого билета, группу),
сохранить их и вывести из MySQL в виде таблицы.
3. Сохранить данные из MySQL в Excel и вывести на экран в виде таблицы.\n>>> """)
    while num != "quit":
        if num == "1":
            num = input("1. Создать базу данных.\n2. Создать таблицу\n3. Отмена действия\n>>> ")
            if num == "1":
                create_database(input("Введите названте базы данных\n>>> "))
            elif num == "2":
                create_table(input("Введите название базы данных\n>>> "), input("Введите название таблицы\n>>> "))
        elif num == "2":
            write_in_db(input("Название базы данных -> "),
                        input("Название таблицы -> "),
                        input("Направление подготовки -> "),
                        input("ФИО -> "),
                        input("Номер студенческого билета -> "),
                        input("Группу -> "))
        elif num == "3":
            base_name = input("Введите название базы данных >>> ")
            table_name = input("Введите название таблицы >>> ")
            print(read_from_db(base_name, table_name))
            id = []
            specialization = []
            name = []
            studentnumber = []
            groupnmb = []
            # ID, specialization, name, studentnumber, groupnmb
            for line in read_from_db(base_name, table_name):
                id.append(line["ID"])
                specialization.append(line["specialization"])
                name.append(line["name"])
                studentnumber.append(line["studentnumber"])
                groupnmb.append(line["groupnmb"])
                data = pd.DataFrame({
                    "ID": id,
                    'specialization': specialization,
                    'name': name,
                    'studentnumber': studentnumber,
                    'groupnmb': groupnmb
                })
            excel_name = input('Введите название таблицы: ')
            data.to_excel(f'./{excel_name}.xlsx')
            writer = pd.ExcelWriter(f"./{excel_name}.xlsx", engine='xlsxwriter')
            data.to_excel(writer)
            writer.save()
        num = input("Введите команду -> ")


if __name__ == "__main__":
    main()