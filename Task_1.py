import pymysql
import uuid
import pandas as pd

dbname = str(input("Введите название базы данных: "))


def create_database(name):
    try:
        connection = pymysql.Connect(host="localhost",
                                     user="root",
                                     password="Admin1234!",
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
    finally:
        return


def create_table(table_name):
    try:
        global dbname
        connection = pymysql.Connect(host="localhost",
                                     user="root",
                                     password="Admin1234!",
                                     charset='utf8mb4',
                                     db=dbname,
                                     cursorclass=pymysql.cursors.DictCursor)
        print("[INFO] Connect to MySQL successful")
        with connection.cursor() as cursor:
            sql = f"""CREATE TABLE IF NOT EXISTS {table_name} (ID varchar(255) key, action varchar(255), result FLOAT(255, 2));"""
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


def write_in_db(action, table_name, nums):
    try:
        global dbname
        connection = pymysql.Connect(host="localhost",
                                     user="root",
                                     password="Admin1234!",
                                     charset='utf8mb4',
                                     db=dbname,
                                     cursorclass=pymysql.cursors.DictCursor)
        print("[INFO] Connect to MySQL successful")
        with connection.cursor() as cursor:
            ID = uuid.uuid4()
            action = action
            if action == "sum":
                action = nums[0] + "+" + nums[1]
                result = int(nums[0]) + int(nums[1])
            elif action == "sub":
                action = nums[0] + "-" + nums[1]
                result = int(nums[0]) - int(nums[1])
            elif action == "mult":
                action = nums[0] + "*" + nums[1]
                result = int(nums[0]) * int(nums[1])
            elif action == "division":
                action = nums[0] + "/" + nums[1]
                result = int(nums[0]) / int(nums[1])
            elif action == "div":
                action = nums[0] + "//" + nums[1]
                result = int(nums[0]) // int(nums[1])
            elif action == "mod":
                action = nums[0] + "%" + nums[1]
                result = int(nums[0]) % int(nums[1])
            elif action == "exponentiation":
                action = nums[0] + "**" + nums[1]
                result = int(nums[0]) ** int(nums[1])
            else:
                d = int(input("Введите число, на которое хотите разделить возведение в степень по модулю: "))
                result = pow((nums[0]), int(nums[1]), d)
                action = f"pow({nums[0]}, {nums[1]}, {d})"

            sql = f"INSERT INTO {table_name.upper()} (ID, action, result) VALUES(%s, %s, %s)"
            cursor.execute(sql, (ID, action, result))
            connection.commit()
            connection.close()
        print(f"[INFO] Данные сохранены в таблицу")
    except Exception as ex:
        print(f"[ERROR] Что-то пошло не так. У нас не получилось создать базу данных по причине: {ex}")
    finally:
        return


def read_db():
    try:
        global dbname
        connection = pymysql.Connect(host="localhost",
                                     user="root",
                                     password="Admin1234!",
                                     charset='utf8mb4',
                                     db=dbname,
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


def main():
    num = input("""1. Создать таблицу в MySQL.
2. Ввести числа с клавиатуры и суммировать их, результат сохранить в MySQL.
3. Ввести числа с клавиатуры и вычесть одно число из другого, результат сохранить в MySQL.
4. Ввести числа с клавиатуры и умножить их, результат сохранить в MySQL.
5. Ввести числа с клавиатуры и найти частное, результат сохранить в MySQL.
6. Ввести числа с клавиатуры и получить целую часть от деления, результат сохранить в MySQL.
7. Ввести числа с клавиатуры и получить остаток от деления, результат сохранить в MySQL.
8. Ввести число с клавиатуры и возвести его в степень, результат сохранить в MySQL.
9. Ввести число с клавиатуры и возвести его в степень с возможностью деления по модулю, результат сохранить в MySQL.
10. Все результаты вывести на экран из MySQL.
11. Сохранить все данные из MySQL в Excel.
12. Вывести все данные на экран из Excel.\n""")
    while num != "quit":
        if num == "1":
            create_table(input("Ведите название таблицы: "))
        elif num == "2":
            write_in_db("sum", input("Введите название таблицы, в которую хотите занести изменения: "),
                        input("Напишите пример без пробелов. Например 2+4\n").split("+"))
        elif num == "3":
            write_in_db("sub", input("Введите название таблицы, в которую хотите занести изменения: "),
                        input("Напишите пример без пробелов. Например 3-1\n").split("-"))
        elif num == "4":
            write_in_db("mult", input("Введите название таблицы, в которую хотите занести изменения: "),
                        input("Напишите пример без пробелов. Например 5*4\n").split("*"))
        elif num == "5":
            write_in_db("division", input("Введите название таблицы, в которую хотите занести изменения: "),
                        input("Напишите пример без пробелов. Например 3/2\n").split("/"))
        elif num == "6":
            write_in_db("div", input("Введите название таблицы, в которую хотите занести изменения: "),
                        input("Напишите пример без пробелов. Например 5//2\n").split("//"))
        elif num == "7":
            write_in_db("mod", input("Введите название таблицы, в которую хотите занести изменения: "),
                        input("Напишите пример без пробелов. Например 4%3\n").split("%"))
        elif num == "8":
            write_in_db("exponentiation", input("Введите название таблицы, в которую хотите занести изменения: "),
                        input("Напишите пример без пробелов. Например 3**1\n").split("**"))
        elif num == "9":
            write_in_db("pow", input("Введите название таблицы, в которую хотите занести изменения: "),
                        input("Напишите пример без пробелов. Например 3**1\n").split("**"))
        elif num == "10":
            for line in read_db():
                print(line)
        elif num == "11":

            ids = []
            actions = []
            results = []
            for line in read_db():

                ids.append(line["ID"])
                actions.append(line["action"])
                results.append(line['result'])
            data = pd.DataFrame({
                "ID": ids,
                'action': actions,
                'result': results
            })
            excel_name = input('Введите название таблицы: ')
            data.to_excel(f'./{excel_name}.xlsx')
            writer = pd.ExcelWriter(f"./{excel_name}.xlsx", engine='xlsxwriter')
            # Записать ваш DataFrame в файл
            data.to_excel(writer)
            # Сохраним результат
            writer.save()
        elif num == "12":
            calculates = pd.read_excel(f"./{input('Введите название таблицы: ')}.xlsx", usecols=[2, 3])
            try:
                print(calculates.head())
            except Exception as ex:
                print('[ERROR]', ex)
        else:
            print("Something wrong. Try again")
        num = input()


if __name__ == "__main__":
    main()
