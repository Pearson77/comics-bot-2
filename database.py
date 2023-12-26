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
