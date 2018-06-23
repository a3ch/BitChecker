import sqlite3

def commit_close(func):
    def func_internal(*args):
        con = sqlite3.connect("base.db")
        cur = con.cursor()
        sql = func(*args)
        cur.execute(sql)
        con.commit()
        con.close()

    return func_internal

@commit_close
def db_insert(array):
    return """
    INSERT INTO base(name, price_USD, date, time) VALUES('{}', '{}', DATE('now'), time('now'))
    """.format(*array)

@commit_close
def db_create(name):
    return """
    CREATE TABLE {}(id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                price_USD REAL NOT NULL,
                date TEXT NOT NULL,
                time TEXT NOT NULL)
    """.format(name)

# Única func que não recebe o decorador
def db_select(data ,field):
    con = sqlite3.connect("base.db")
    cur = con.cursor()
    sql = """
    SELECT * FROM base WHERE {}={}
    """.format(data, field)
    cur.execute(sql)
    data = cur.fetchall()
    con.close()

    return data
