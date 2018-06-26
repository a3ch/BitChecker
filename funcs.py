import sqlite3


def commit_close(func):
    def func_internal(*args):
        con = sqlite3.connect("base.db")
        cur = con.cursor()
        sql = func(*args)
        try:
            cur.execute(sql)
            con.commit()
        except sqlite3.OperationalError:
            print("Error: SQL Operational Error")
        con.close()

    return func_internal


@commit_close
def db_insert(array, mode=True):
    if mode:
        return """
        INSERT INTO base(id,name, price_USD, date, time) VALUES('{}', '{}', '{}', DATE('now'), time('now'))
        """.format(*array)
    return """
    INSERT INTO base_reg(id,price_USD, date, time) VALUES('{}', '{}', DATE('now'), time('now'))
    """.format(*array)


@commit_close
def db_create(name, mode=True):
    if mode:

        return """
        CREATE TABLE {}(id INTEGER NOT NULL PRIMARY KEY,
                    name TEXT NOT NULL,
                    price_USD REAL NOT NULL,
                    date TEXT NOT NULL,
                    time TEXT NOT NULL)
        """.format(name)

    return """
    CREATE TABLE {}(id INTEGER NOT NULL,
                price_USD REAL NOT NULL,
                date TEXT NOT NULL,
                time TEXT NOT NULL,
                id_fix INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT)
    """.format(name)


@commit_close
def db_update(price, field):
    return """
    UPDATE base SET price_USD='{}', date=DATE('now'), time=TIME('now') WHERE id='{}'
    """.format(price, field)

# Única func que não recebe o decorado
# ALTEREI O FETCHALL


def db_select(data, field):
    con = sqlite3.connect("base.db")
    cur = con.cursor()
    sql = """
    SELECT * FROM base WHERE {}={}
    """.format(data, field)
    cur.execute(sql)
    data = cur.fetchone()
    con.close()

    if data is None:
        return data
    return data[0]
