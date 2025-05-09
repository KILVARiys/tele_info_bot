import sqlite3 as sq

# Подключаемся к базе данных
db = sq.connect('users.db')
cur = db.cursor()

# Функция для создания таблицы, если её нет
def db_start():
    cur.execute("CREATE TABLE IF NOT EXISTS profile (user_id TEXT PRIMARY KEY, username TEXT, dogname TEXT, phone TEXT, country TEXT, number_type TEXT, carrier_name TEXT, tz_info TEXT)")
    db.commit()
    #Логирование
    print("Таблица profile создана или уже существует")

# Функция для создания профиля
def create_profile(user_id, username, dogname, phone, country, number_type, carrier_name, tz_info):
    user = cur.execute("SELECT 1 FROM profile WHERE user_id = ?", (user_id,)).fetchone()
    if not user:
        cur.execute("INSERT INTO profile (user_id, username, dogname, phone, country, number_type, carrier_name, tz_info) VALUES (?, ?, ?, ?, ?, ?, ?, ?)", (user_id, username, dogname, phone, country, number_type, carrier_name, tz_info))
        db.commit()
        #Логирование
        print(f"Профиль {username} добавлен")

# Выполняем функции
db_start()