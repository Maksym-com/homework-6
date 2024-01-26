import sqlite3


def add_question(question, answers, correct):
    msg = ""
    with sqlite3.connect("app.db") as conn:
        try:
            cr = conn.cursor()
            cr.execute("INSERT INTO test (question, answers, correct) VALUES (?, ?, ?)",
                       (question, answers, correct))
            conn.commit()
            msg = "Record success added"
        except Exception as e:
            conn.rollback()
            print(e)
            msg = "Error in insert operation"
    return msg


def get_questions():
    res = None
    with sqlite3.connect("app.db") as conn:
        conn.row_factory = sqlite3.Row
        cr = conn.cursor()
        cr.execute("SELECT * FROM test")
        res = cr.fetchall()
        for row in res:
            print(row['question'], row['answers'], row['correct'])
    return res

def get_correct(question):
    cor = None
    with sqlite3.connect("app.db") as conn:
        cr = conn.cursor()
        cr.execute("SELECT correct FROM test WHERE question=?", (question, ))
        cor = cr.fetchone()
        print(cor)
    return cor[0]



