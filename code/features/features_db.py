import sys
sys.path.append('..')

from features import Features
from util.db import DataBase

class FeatureDB:

    def __init__(self, db):
        self.db = db


    #reads links info from database, creates features and save it back to the database
    def create_and_insert_features(self):
        dbc = DataBase(self.db)
        links = dbc.get_links()

        for item in links:

            f = Features(item[1],item[2])
            f.get_features()
            print(f"{item[1]} - {f.features}")
            f.insert_in_db(self.db)
        
        dbc.close()


if __name__ == '__main__':

    db = sys.argv[1]
    fdb = FeatureDB(db)

    fdb.create_and_insert_features()
