# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import sqlite3

from itemadapter import ItemAdapter


class SqlitePipeline:
    def __init__(self):
        ## Create/Connect to database
        self.con = sqlite3.connect('vnexpress.db')

        ## Create cursor, used to execute commands
        self.cur = self.con.cursor()

        ## Create PLDS table if none exists
        self.cur.execute("""
        CREATE TABLE IF NOT EXISTS bai_bao(
            title TEXT,
            date_vn TEXT,
            content TEXT,
            url TEXT
        )
        """)

    def process_item(self, item, spider):
        ## Define insert statement
        self.cur.execute("""
                    INSERT INTO bai_bao (title, date_vn, content, url) VALUES (?, ?, ?, ?)
                """,
                         (
                             item['title'],
                             str(item['date']),
                             item['content'],
                             item['url'],
                         ))

        ## Execute insert of data into database
        self.con.commit()
        return item
