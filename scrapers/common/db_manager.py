import os
import mysql.connector


class DbManager:

    def __init__(self):
        self.db_connection = mysql.connector.connect(
            host="mysql_db",
            port="3306",
            user=os.environ["MYSQL_USER"],
            password=os.environ["MYSQL_PASSWORD"],
            database="charlie_feeder"
        )
        self.cursor = self.db_connection.cursor()

    def insert_data(self, table_name, rows_list):
        q = "INSERT INTO {} " \
            "(title, date, place, category, description, post_id, link_post, link_image) VALUES " \
            "(%s, %s, %s, %s, %s, %s, %s, %s);".format(table_name)

        self.cursor.executemany(q, rows_list)
        self.db_connection.commit()

    def truncate_table(self, table_name):
        q = f"TRUNCATE {table_name}"
        self.cursor.execute(q)
        self.db_connection.commit()

    def clean_and_insert_data(self, table_name, rows_list):
        self.truncate_table(table_name)
        self.insert_data(table_name, rows_list)

    def run_store_procedure(self, sp_name):
        self.cursor.callproc(sp_name)
        self.db_connection.commit()
