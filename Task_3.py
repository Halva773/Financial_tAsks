import pymysql
import pandas as pd


def create_db(name):
    try:
        connection = pymysql.Connect(host="localhost",
                                     user="root",
                                     password="root",
                                     charset='utf8mb4',
                                     cursorclass=pymysql.cursors.DictCursor)
        print("[INFO] Connect to MySQL successful")
        with connection.cursor() as cursor:

            sql = f"""CREATE DATABASE {name}"""
            cursor.execute(sql)
            connection.commit()

            sql1 = "SHOW DATABASES"

            print("Count of Databases: ", cursor.execute(sql1), f"\nDatabase {name} was created")
            for db in cursor:
                print(db)
            connection.close()
    except Exception as ex:
        print(f"[ERROR] Что-то пошло не так. У нас не получилось создать базу данных по причине: {ex}")
        pass
    finally:
        return


def write_in_db(database_name, table_name, key, value):
    try:
        connection = pymysql.Connect(host="localhost",
                                     user="root",
                                     password="Admin1234!",
                                     charset='utf8mb4',
                                     db=database_name,
                                     cursorclass=pymysql.cursors.DictCursor)
        with connection.cursor() as cursor:
            sql = f"INSERT INTO {table_name.upper()} (ID, VALUE) VALUES(%s, %s)"
            cursor.execute(sql, (key, value))
            connection.commit()
            connection.close()
    except Exception as ex:
        print(f"[ERROR] --- {ex}")
    finally:
        pass


def create_table(database_name, table_name):
    try:
        connection = pymysql.Connect(host="localhost",
                                     user="root",
                                     password="Admin1234!",
                                     charset='utf8mb4',
                                     db=database_name,
                                     cursorclass=pymysql.cursors.DictCursor)
        print("[INFO] Connect to MySQL successful")
        with connection.cursor() as cursor:
            sql = f"""CREATE TABLE IF NOT EXISTS {table_name} (ID varchar(255) key, VALUE varchar(255));"""
            cursor.execute(sql)
            connection.commit()

            sql1 = "SHOW tables"

            print("[INFO] Count of tables: ", cursor.execute(sql1),
                  f"\n[INFO] Table '{table_name.upper()}' was created")
            for tables in cursor:
                print(tables)
            connection.close()
    except Exception as ex:
        print(f"[ERROR] Что-то пошло не так. У нас не получилось создать базу данных по причине: {ex}")
    finally:
        pass


def read_db(database_name):
    try:
        connection = pymysql.Connect(host="localhost",
                                     user="root",
                                     password="Admin1234!",
                                     charset='utf8mb4',
                                     db=database_name,
                                     cursorclass=pymysql.cursors.DictCursor)
        print("[INFO] Connect to MySQL successful")
        with connection.cursor() as cursor:
            sql = f"""SELECT * FROM {input('Введите название таблицы, данные которой хотите увидеть:')}"""
            print(f"Количество записей в таблице: {cursor.execute(sql)}")
            datas = []
            for data in cursor.fetchall():
                datas.append(data)
            connection.close()
        return datas
    except Exception as ex:
        print(f"[ERROR] Что-то пошло не так. У нас не получилось считать данные по причине: {ex}")
    finally:
        pass


def create_list_one(database_name, table_name, action="none"):  # Фунция создания таблицы ключ - значения
    try:
        create_table(database_name, table_name)  # Создание Таблицы, для записи значений
        if action == "list_one":  # Если необходимо созать список первого типа, то в функцию нужно передать action=list_one
            keys = input(
                "Введите значение ключей через пробел\n>>> ").split()  # Спрашиваю, какие ключи и хначения нужно записать пользователю
            values = input("Введите значения через пробел\n>>> ").split()

        else:  # Иначе мы формируем списки второго типа
            keys = [x for x in range(1, 11)]
            values = [x ** 3 for x in range(1, 11)]

        for i in range(len(keys)):  # Записываем все значение полученные выше
            write_in_db(database_name, table_name, keys[i], values[i])

    except Exception as ex:
        print(f"[ERROR] --- {ex}")
    finally:
        pass


def create_list_two(database_name, table_name):
    try:
        create_table(database_name, table_name)  # Создание Таблицы, для записи значений

        keys = input(
            "Введите значение ключей через пробел\n>>> ").split()  # Спрашиваю, какие ключи и хначения нужно записать пользователю
        values = input("Введите значения через пробел\n>>> ").split()

        for i in range(len(keys)):  # Записываем все значение полученные выше
            write_in_db(database_name, table_name, keys[i], values[i])
    except Exception as ex:
        print(f"[ERROR] ---{ex}")
    pass


def save_to_xl():
    ids = []
    value = []
    for line in read_db(database_name=input("Введите название базы данных, из которой хотите получить данные:\n>>> ")):
        ids.append(line["ID"])
        value.append(line["VALUE"])
    data = pd.DataFrame({
        "ID": ids,
        'VALUE': value
    })
    excel_name = input('Введите название таблицы: ')
    data.to_excel(f'./{excel_name}.xlsx')
    writer = pd.ExcelWriter(f"./{excel_name}.xlsx", engine='xlsxwriter')
    # Записать ваш DataFrame в файл
    data.to_excel(writer)
    # Сохраним результат
    writer.save()
    print(f"[INFO] --- Данные сохранены в таблицу с названием {excel_name}")

def main():
    num = input("""1. Создать базы данных в MySQL.
2. Создать первый словарь из двух списков и сохранить результаты в MySQL.
3. Создать второй словарь из двух списков и сохранить результаты в MySQL.
4. Все результаты вывести на экран из MySQL.
5. Все результаты сохранить в Excel.
6. Все результаты вывести на экран (в консоль) через Excel.\n>>> """)
    while num != "quit":
        if num == "1":
            create_db(input("Введите название базы данных, которую хотите создать\n>>> "))
        elif num == "2":
            create_list_one(input("Введите название базы данных, в которую хотите добавить таблицу\n>>> "),
                            input("Введитн название таблицы, которую хотите создать\n>>> "), action="list_one")
        elif num == "3":
            create_list_one(input("Введите название базы данных, в которую хотите добавить таблицу\n>>> "),
                            input("Введитн название таблицы, которую хотите создать\n>>> "))
        elif num == "4":
            for line in read_db(input("Введите название базы данных, из которой хотите получить данные:\n>>> ")):
                print(line)
        elif num == "5":
            save_to_xl()
        else:
            calculates = pd.read_excel(f"./{input('Введите название таблицы: ')}.xlsx", usecols=[1, 2])
            try:
                print(calculates.head())
            except Exception as ex:
                print('[ERROR]', ex)
        num = input(">>> ")


if __name__ == "__main__":
    main()
