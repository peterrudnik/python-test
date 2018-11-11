'''
Created on 19.02.2017

@author: prudnik
'''

import sqlite3
import dataset


def sample_without_dataset():
    try:
        # open connection and get a cursor
        conn = sqlite3.connect(':memory:')
        c = conn.cursor()
        
        # create schema for a new table
        c.execute('CREATE TABLE IF NOT EXISTS sometable (name, age INTEGER)')
        conn.commit()
        
        # insert a new row
        c.execute('INSERT INTO sometable values (?, ?) ', ('John Doe', 37))
        conn.commit()
        
        # extend schema during runtime
        c.execute('ALTER TABLE sometable ADD COLUMN gender TEXT')
        conn.commit()
        
        # add another row
        c.execute('INSERT INTO sometable values (?, ?, ?) ', ('Jane Doe', 34, 'female'))
        conn.commit()
        
        # get a single row
        c.execute('SELECT name, age FROM sometable WHERE name = ?', ('John Doe', ))
        row = list(c)[0]
        john = dict(name=row[0], age=row[1])
    except Exception as e:
        print (str(e))    


def sample_with_dataset():
    try:
        #db = dataset.connect('sqlite:///:memory:')
        db = dataset.connect('sqlite:///example.db')
        table = db['sometable']
        table.insert(dict(name='John Doe', age=37))
        table.insert(dict(name='Jane Doe', age=34, gender='female'))
        
        john = table.find_one(name='John Doe')
    except Exception as e:
        print (str(e))    

def run():
    sample_with_dataset()
    #sample_without_dataset()

if __name__ == '__main__':
    run()

