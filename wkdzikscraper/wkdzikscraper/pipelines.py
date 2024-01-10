# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import sqlite3

class WkdzikscraperPipeline:
    def process_item(self, item, spider):
        return item


class SaveToSQL:
    def __init__(self):
        self.con = sqlite3.connect('wkdzik.db')
        self.cur = self.con.cursor()
        
        self.cur.execute('''
            CREATE TABLE IF NOT EXISTS produkty(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nazwa_produktu TEXT,
                cena REAL
            )''')

    def process_item(self, item, spider):
        self.cur.execute('''
            INSERT INTO produkty(
                nazwa_produktu,
                cena
            ) values(?, ?)''', (item['name'], item['price']))\
                
        self.con.commit()
        return item
    
    def close_spider(self, spider):
        self.cur.close()
        self.con.close()