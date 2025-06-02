import pymysql

def crear_conexion():
    return pymysql.connect(
        host="localhost",
        user="root",
        password="6666",
        database="suburbia",
        cursorclass=pymysql.cursors.DictCursor
    )
