import sys
sys.path.append('..')

from util.db import DataBase


class Features:
    
    def __init__(self, link, count=None):
        self.link = link
        self.features = []
        self.count = count
    

    #creates features
    def get_features(self):
        #link length
        f1 = len(self.link)
        self.features.append(f1)

        #number of vowels
        #number of consonants
        f2 = 0
        f3 = 0
        for char in self.link:
            if char in 'aeiou':
                f2 += 1
            elif char not in [':/-.']:
                f3 += 1
        self.features.append(f2)
        self.features.append(f3)

        #ration #vowels/#consonants
        f4 = f3/f2 if f2 > 0 else 0
        self.features.append(f4)

        #domain length
        domain = self.link.split('://')[1].split('/')[0]
        f5 = len(domain)
        self.features.append(f5)

        #ratio domain length/link length
        f6 = f5/f1
        self.features.append(f6)

        #avarage int representation of domain's characters
        f7 = 0.0
        for char in domain:
            f7 += ord(char)
        f7 = f7/f5
        self.features.append(f7)

        path = self.link.split('://')[1].split('/',1)
        #number of paths
        f8 = 0
        #avg subpath char length
        f9 = 0.0
        #number of numeric symbols in the path
        f10 = 0
        if len(path) > 1:
            path = path[1].split('/')
            f8 = len(path)

            for name in path:
                f9 += len(name)
                for char in name:
                    if char.isnumeric():
                        f10 += 1
            f9 = f9/f7
        
        self.features.append(f8)
        self.features.append(f9)
        self.features.append(f10)

        return self.features


    def insert_in_db(self, db):
        db = DataBase(db)
        db.create_table_features()
        db.insert_features(self.link, self.features, self.count)
        db.close()

