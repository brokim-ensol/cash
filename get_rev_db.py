#sqlite3를 이용하여 현재 같은 폴더에 있는 pybo.db 파일을 읽는다.
#그리고 alembic_version 테이블의 version_num을 조회한다.
#이렇게 조회한 version_num을 리턴한다.
def get_rev_db():
    import sqlite3
    try:
        conn = sqlite3.connect('pybo.db')
        cur = conn.cursor()
        cur.execute('SELECT version_num FROM alembic_version')
        version_num = cur.fetchone()
        conn.close()
        return version_num[0]
    except:
        return "0"

if __name__ == '__main__':
    version_number = get_rev_db()