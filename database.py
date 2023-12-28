import sqlite3


class Connection:
    def __enter__(self):
        self.connect = sqlite3.connect("databases/database.db")
        return self.connect.cursor()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.connect.commit()
        self.connect.close()


class DB:
    @staticmethod
    def create_comics(comics_name: str, file_ids: list[str]):
        with Connection() as c:
            c.execute(F"CREATE TABLE {comics_name} (file_id TEXT)")

            for file_id in file_ids:
                c.execute(F"INSERT INTO {comics_name} VALUES ('{file_id}')")

    @staticmethod
    def delete_comics(comics_name: str):
        with Connection() as c:
            c.execute(F"DROP TABLE {comics_name}")

    @staticmethod
    def get_comics_len(comics_name: str):
        with Connection() as c:
            result = c.execute(F"SELECT COUNT(rowid) FROM {comics_name}").fetchone()
        return result[0]

    @staticmethod
    def get_page_by_number(comics_name: str, page: int):
        with Connection() as c:
            result = c.execute(F"SELECT file_id FROM {comics_name} WHERE rowid = '{page}'").fetchone()
        return result[0]

    @staticmethod
    def get_comics_all_names():
        with Connection() as c:
            result = c.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()
        return list(map(lambda element: element[0], result)) if result else []
