import os
from queue import Queue
from threading import Thread

import mysql.connector


class DbManager:
    """This class is a database wrapper.
    Since it is shared between all the scrapers, it was designed as singleton.
    Each scraper use this class to truncate table, delete or insert records in the ads table.
    To avoid conflicts during the execution of the queries, everything is consumed in a queue by a thread.
    """

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
        # in this way the db manager is shared between all the services without conflicts
        self.queue = Queue()
        self.worker_thread = Thread(target=self._process_queue)
        self.worker_thread.start()

    def __new__(cls, *args, **kwargs):
        """Manage singleton feature"""
        if not cls._instance:
            cls._instance = super().__new__(cls, *args, **kwargs)
        return cls._instance

    def _process_queue(self):
        """Aim of this function is to consume the queue with all the queries.
        Each element of the queue contains a dict with the following structure:
        {"query": <query_string>, "params": None|list}

        A separated thread (see init of the class) execute the query and remove the task from the queue.
        Since we don't want errors, if something during the query execution fails, simply skip the record.
        """
        while True:
            data_dict = self.queue.get()
            query = data_dict.get("query")
            params = data_dict.get("params")

            try:
                if params:
                    self.cursor.executemany(query, params)
                else:
                    self.cursor.execute(query)
                self.db_connection.commit()
            except Exception as e:
                print(f"An error occurred saving data: {e}")

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
