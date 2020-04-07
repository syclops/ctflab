from hacksport.problem import PHPApp, ProtectedFile, files_from_directory
import fileinput
import sqlite3

DB_FILE = "users.db"
WEB_ROOT = "webroot/"
PLAINTEXT_DB = "db.txt"


class Problem(PHPApp):
    files = files_from_directory(WEB_ROOT) + [ProtectedFile(DB_FILE)]
    php_root = WEB_ROOT

    def generate_flag(self, _):
        return "three_rolodexes_in_a_trenchcoat"

    def setup(self):
        conn = sqlite3.connect(DB_FILE)
        c = conn.cursor()
        c.execute("CREATE TABLE users (id INTEGER, name TEXT, password TEXT);")
        for line in fileinput.input(PLAINTEXT_DB):
            id_num, user, passwd = line.strip().split(',')
            c.execute(
                f"INSERT INTO users VALUES ({id_num}, '{user}', '{passwd}')"
            )
        conn.commit()
        conn.close()
