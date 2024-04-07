#!./venv python
def get_rev_db():
    import sqlite3
    try:
        conn = sqlite3.connect('pybo.db')
        cur = conn.cursor()
        cur.execute('SELECT version_num FROM alembic_version')
        version_num = cur.fetchone()
        conn.close()
        print(version_num[0],end=None)
    except:
        print("0",end=None)

if __name__ == '__main__':
    get_rev_db()