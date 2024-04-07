def remove_not_valid_record():
    import sqlite3

    conn = sqlite3.connect("pybo.db")
    cur = conn.cursor()
    # delete the records if repayment_id is NULL from balance table
    cur.execute("DELETE FROM balance WHERE repayment_id IS NULL")
    conn.commit()
    conn.close()


if __name__ == "__main__":
    remove_not_valid_record()
