import pymysql
import pandas as pd


arrFirts = []
arrSecond = []


def create_table(db_name, table_name):
    connection = pymysql.Connect(host="localhost",
                                 user="root",
                                 password="root",
                                 charset='utf8mb4',
                                 db=db_name,
                                 cursorclass=pymysql.cursors.DictCursor)
    print("OK")
    with connection.cursor() as cursor:

        sql = f"""CREATE TABLE IF NOT EXISTS {table_name} (arr varchar(255) key, action varchar(255));"""
        cursor.execute(sql)
        connection.commit()
        connection.close()


def write_in_db(db_name, table_name, array, append):
    connection = pymysql.Connect(host="localhost",
                                 user="root",
                                 password="root",
                                 charset='utf8mb4',
                                 db=db_name,
                                 cursorclass=pymysql.cursors.DictCursor)
    sql = f"""INSERT INTO {table_name.upper()} (arr, action) VALUES(%s, %s)"""
    with connection.cursor() as cursor:
        cursor.execute(sql, (array, append))
        connection.commit()
        connection.close()


def read_from_db(db_name, table_name):
    connection = pymysql.Connect(host="localhost",
                                 user="root",
                                 password="root",
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
    global arrFirts, arrSecond
    num = input(("""1. Создать таблицу в MySQL.
2. Добавление одного элемента в конец первого списка, сохранение и вывод из MySQL.
3. Добавление второго списка в первый список, сохранение и вывод из MySQL.
4. Развернуть итоговый список, сохранение и вывод из MySQL.
5. Сохранить данные из MySQL в Excel и вывести на экран
6. Сброосить значения в массивах\n"""))
    while num != "quit":
        if num == "1":
            create_table(input("Введите название базы данных >>> "),
                         input("Введите название таблицы >>> "))
        elif num == "2":
            print(arrFirts)
            if len(arrFirts) < 1:
                arrFirts = input("Введите значения массива через пробел >>> ").split()
            app_num = input("Введите значение которое хотите добавить >>> ")
            arrFirts.append(app_num)
            print(arrFirts)
            write_in_db(input("Введите название базы данных >>> "),
                        input("Введите название таблицы >>> "),
                        str(arrFirts), str(app_num))
        elif num == "3":
            if len(arrFirts) < 1:
                arrFirts = input("Введите значения первого массива через пробел >>> ").split()
            if len(arrSecond) < 1:
                arrSecond = input("Введите значения второго массива через пробел >>> ").split()
            arrFirts.extend(arrSecond)
            print(arrFirts)
            write_in_db(input("Введите название базы данных >>> "),
                        input("Введите название таблицы >>> "),
                        str(arrFirts), str(arrSecond))
        elif num == "4":
            arrFirts.reverse()
            print(arrFirts)
        elif num == "5":
            base_name = input("Введите название базы данных >>> ")
            table_name = input("Введитн название таблицы >>> ")
            print(read_from_db(base_name, table_name))
            arr = []
            actions = []
            for line in read_from_db(base_name, table_name):
                arr.append(line["arr"])
                actions.append(line["action"])
            data = pd.DataFrame({
                "array": arr,
                'action': actions,
            })
            excel_name = input('Введите название таблицы: ')
            data.to_excel(f'./{excel_name}.xlsx')
            writer = pd.ExcelWriter(f"./{excel_name}.xlsx", engine='xlsxwriter')
            data.to_excel(writer)
            writer.save()
        elif num == "6":
            action = input("1. Сбрость первый список\n2. Сбросить второй список\n3. Сбросить оба списка\n4. Отмена")
            if action == "1":
                arrFirts = []
            elif action == "2":
                arrSecond = []
            elif action == "3":
                arrSecond = []
                arrFirts = []

        else:
            print("Я вас не понял")
        num = input("\n")




if __name__ == "__main__":
    main()