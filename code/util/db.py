import sqlite3


class DataBase:

    def __init__(self, db):
        self.db = db
        self.__create_connection()

    
    def __create_connection(self):
        self.conn = sqlite3.connect(self.db)
    

    def get_links(self):
        cur = self.conn.cursor()
        cur.execute("SELECT * FROM LINKS")

        rows = cur.fetchall()

        return rows

    
    def create_table_features(self):
        self.conn.execute('''CREATE TABLE IF NOT EXISTS FEATURES
                            (   LINK TEXT PRIMARY KEY     NOT NULL,
                                F1           FLOAT    NOT NULL,
                                F2           FLOAT    NOT NULL,
                                F3           FLOAT    NOT NULL,
                                F4           FLOAT    NOT NULL,
                                F5           FLOAT    NOT NULL,
                                F6           FLOAT    NOT NULL,
                                F7           FLOAT    NOT NULL,
                                F8           FLOAT    NOT NULL,
                                F9           FLOAT    NOT NULL,
                                F10          FLOAT    NOT NULL,
                                APPEARENCES INT
                            );''')


    def insert_features(self, link, features, count):
        print(f"LINK: {link} - FEATURES: {features} - APPEARENCES: {count}")
        count  = count if count else 'NULL'
        query = f'''INSERT INTO FEATURES (LINK, F1, F2, F3, F4, F5,
                                        F6, F7, F8, F9, F10, APPEARENCES)
                            VALUES ('{link}',
                            {features[0]},
                            {features[1]},
                            {features[2]},
                            {features[3]},
                            {features[4]},
                            {features[5]},
                            {features[6]},
                            {features[7]},
                            {features[8]},
                            {features[9]},
                            {count})
                            ON CONFLICT(LINK) 
                            DO UPDATE SET F1={features[0]},
                            F2={features[1]},
                            F3={features[2]},
                            F4={features[3]},
                            F5={features[4]},
                            F6={features[5]},
                            F7={features[6]},
                            F8={features[7]},
                            F9={features[8]},
                            F10={features[9]};'''
        #print(query)
        self.conn.execute(query)

        self.conn.commit()
    

    def get_link_features(self, link):

        cur = self.conn.cursor()
        query = f"""SELECT
                        F1,
                        F2,
                        F3,
                        F4,
                        F5,
                        F6,
                        F7,
                        F8,
                        F9,
                        F10 FROM FEATURES WHERE LINK ='{link}'"""

        #print(query)
        cur.execute(query)

        rows = cur.fetchall()

        return rows
    

    def create_table_predictions(self):
        self.conn.execute('''CREATE TABLE IF NOT EXISTS PREDICTIONS
                            (LINK TEXT PRIMARY KEY     NOT NULL,
                            APPEARENCES           FLOAT    NOT NULL
                            );''')


    def insert_predictions(self, link, appearences):
        print(f"LINK: {link} - APPEARENCES:{appearences}")
        query = f'''INSERT INTO PREDICTIONS (LINK, APPEARENCES)
                            VALUES ('{link}', {appearences});'''
        self.conn.execute(query)

        self.conn.commit()


    def get_link_predictions(self, link):

        cur = self.conn.cursor()
        query = f"""SELECT APPEARENCES FROM PREDICTIONS WHERE LINK ='{link}'"""

        #print(query)
        cur.execute(query)

        rows = cur.fetchall()

        return rows

 
    def close(self):
        self.conn.close()
