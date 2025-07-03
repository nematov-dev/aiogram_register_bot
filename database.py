import psycopg2
from decouple import config

conn = psycopg2.connect(
    dbname=config("dbname"),
    user=config("user"),
    password=config("password"),
    host=config("host"),
    port=config("port")
)

cursor = conn.cursor()

#Create table
def create_users_table():
    try:
        sql = """
        CREATE TABLE IF NOT EXISTS users (
        id SERIAL PRIMARY KEY,
        telegram_id BIGINT NOT NULL,
        name VARCHAR(50) NOT NULL,
        surname VARCHAR(50) NOT NULL,
        phone VARCHAR(20) NOT NULL,
        username VARCHAR(50),
        created_at TIMESTAMP DEFAULT now(),
        UNIQUE(telegram_id)
        )"""
        cursor.execute(sql)
        conn.commit()

    except Exception as e:
        print(f"Xatolik mavjud: {e}")

#Add user
def add_user(telegram_id: int,name:str,surname: str,phone:str,username: str):
    try:
        sql = """
        INSERT INTO users (telegram_id,name,surname,phone,username)
        VALUES (%s,%s,%s,%s,%s)"""
        cursor.execute(sql,(telegram_id,name,surname,phone,username))
        conn.commit()
        return True
    
    except Exception as e:
        print(f"Xatolik mavjud: {e}")
        return False

#Check id
def check_id(telegram_id: int):
    try:
        sql = """
        SELECT * FROM users WHERE telegram_id = %s"""
        cursor.execute(sql,(telegram_id,))
        return cursor.fetchone()
    
    except Exception as e:
        print(f"Xatolik mavjud: {e}")
        return False