import os
from queue import Queue
from threading import Thread

import mysql.connector


class DbManager:

    _instance = None

    def __init__(self):
        self.db_connection = mysql.connector.connect(
            host="mysql_db",
            port="3306",
            user=os.environ["MYSQL_USER"],
            password=os.environ["MYSQL_PASSWORD"],
            database="charlie_feeder"
        )
        self.cursor = self.db_connection.cursor()

        # init queue mechanism
        # in this way the db manager is shared between all the services
        self.queue = Queue()
        self.worker_thread = Thread(target=self._process_queue)
        self.worker_thread.start()

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls, *args, **kwargs)
        return cls._instance

    def _process_queue(self):
        while True:
            data_dict = self.queue.get()
            query = data_dict.get("query")
            params = data_dict.get("params")

            if params:
                self.cursor.executemany(query, params)
            else:
                self.cursor.execute(query)

            self.db_connection.commit()
            self.queue.task_done()

    def insert_data(self, rows_list):
        q = "INSERT INTO ads " \
            "(title, date, place, category, description, price, post_id, link_post, link_image, source) VALUES " \
            "(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"
        self.queue.put({"query": q, "params": rows_list})

    def truncate_table(self):
        q = f"TRUNCATE ads"
        self.queue.put({"query": q, "params": None})

    def delete_records(self, source_name):
        q = f'DELETE FROM ads WHERE source = "{source_name}"'
        self.queue.put({"query": q, "params": None})
