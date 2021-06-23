import sys
import glob

import sqlite3
import pandas as pd


class ProcessData:

    def __init__(self, base_input_file):
        self.base_input_file = base_input_file
        self.df = None

    #read all files in the base_input_file and count the occurrences of links
    def read_files(self):
        df = pd.concat([pd.read_csv(f, header=None, names=['origin','link','count']).drop_duplicates() 
                                        for f in glob.glob(f'{self.base_input_file}-*.csv')], 
                        ignore_index = True)[['link','count']]
        
        self.df = df.groupby('link', as_index=False).sum()
        
        print(self.df.head())

    #save the processed information to a LINKS table in a sqlite database
    def save_to_db(self, db):
        conn = sqlite3.connect(db)
        self.df.to_sql(name='LINKS', con=conn, if_exists='replace')
        conn.close()


if __name__ == '__main__':

    base_input_file = sys.argv[1]
    db = sys.argv[2]
    
    p = ProcessData(base_input_file)

    p.read_files()
    p.save_to_db(db)
    