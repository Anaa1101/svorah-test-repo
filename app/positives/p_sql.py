"""P-SQL | sqli | DPDP-032 | expected: fires (tainted request input reaches execute)."""


def search(req, conn):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE x = " + req.args.get("x"))
    return cursor.fetchall()
