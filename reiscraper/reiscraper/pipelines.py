# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import sqlite3

class ReiscraperPipeline:
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        
        item_no_str = adapter['item_no']
        item_no = int(item_no_str.replace('Item #', ''))
        adapter['item_no'] = item_no
        
        price_str = adapter['price']
        price = float(price_str.replace('$', ''))
        adapter['price'] = price
        
            
        return item


class SaveToSQL:
    def __init__(self):
        self.con = sqlite3.connect('rei_products.db')
        self.cur = self.con.cursor()
        
        self.cur.execute('''
            CREATE TABLE IF NOT EXISTS products(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                price REAL,
                item_no REAL,
                rating INTEGER
            )
            ''')
        
    def process_item(self, item, spider):
        self.cur.execute('''
            INSERT INTO products(
                name,
                price,
                item_no,
                rating
            ) values (?, ?, ?, ?)    
            ''', (
                item['name'],
                item['price'],
                item['item_no'],
                item['rating']
            ))
        self.con.commit()
        return item
    
    def close_spider(self, spider):
        self.cur.close()
        self.con.close()