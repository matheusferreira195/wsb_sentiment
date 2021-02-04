import psycopg2

class db:
    def __init__(self):
        connect_str = "dbname='wsbapp' user='wsb' host='localhost' " + \
                        "password='3406'"
        # use our connection values to establish a connection
        self.conn = psycopg2.connect(connect_str)
        
