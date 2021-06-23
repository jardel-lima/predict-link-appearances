import pandas as pd
import sqlite3
import glob
import sys

class ProcessData:

    def __init__(self, base_file):
        self.base_file = base_file
        self.df = None

    
    def read_files(self):
        df = pd.concat([pd.read_csv(f, header=None, names=['origin','link','count']).drop_duplicates() 
                                        for f in glob.glob(f'{self.base_file}-*.csv')], 
                        ignore_index = True)[['link','count']]
        self.df = df.groupby('link', as_index=False).sum()


    def save_to_db(self, db):
        conn = sqlite3.connect(db)
        self.df.to_sql(name='LINKS', con=conn, if_exists='replace')
        conn.close()

if __name__ == '__main__':

    base_input = sys.argv[1]
    db = sys.argv[2]
    
    p = ProcessData(base_file)

    p.read_files()
    p.save_to_db(db)

        