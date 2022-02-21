import sqlite3

def main():
            db = sqlite3.connect("test.db")
            cur = db.cursor()
            cur.execute("CREATE TABLE IF NOT EXISTS test(money INTEGER, name TEXT)")
            cur.execute("INSERT INTO test (money, name) VALUES (10000, \"osama\")")
            cur.execute("INSERT INTO test (money, name) VALUES (5000, \"ziad\")")
            cur.execute("INSERT INTO test (money, name) VALUES (20, \"ahmad\")")
            cur.execute("INSERT INTO test (money, name) VALUES (5000000, \"sss\")")
            cur.execute("SELECT * FROM test ORDER BY money")
            a = cur.fetchall()
            print(a)

main()