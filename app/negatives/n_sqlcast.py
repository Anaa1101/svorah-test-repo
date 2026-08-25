"""N-SQLCAST | SQL barrier (int cast) | pairs P-SQL | expected: 0 findings.
Casting the request value to int removes the injection taint before execute."""


def search(req, conn):
    cursor = conn.cursor()
    user_id = int(req.args.get("id"))
    cursor.execute("SELECT * FROM users WHERE id = " + str(user_id))
    return cursor.fetchall()
