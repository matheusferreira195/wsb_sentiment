import psycopg2
import psycopg2.extras
import pandas as pd

class Db:
    def __init__(self):
        connect_str = "dbname='postgres' user='postgres' host='localhost' " + \
                        "password='34064031'"
        # use our connection values to establish a connection
        self.conn = psycopg2.connect(connect_str)
        
    def insert_wsb_comment(self, data):
        cursor =  self.conn.cursor()
        query = f"""INSERT INTO wsb_comments (id, body, post, rddt_user, upvotes, downvotes, sentiment, subjectivity, created_at) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
        cursor.execute(query,(
            data.id,
            data.body,
            data.post,
            data.rddt_user,
            data.upvotes,
            data.downvotes,
            data.sentiment,
            data.subjectivity,
            data.created_at
        ))
        self.conn.commit()
        cursor.close()
    
    def query_wsb(self, period=1):
        cursor = self.conn.cursor(cursor_factory = psycopg2.extras.DictCursor)
        
        cursor.execute(f"""SELECT AVG(sentiment) as sentiment_avg, (current_timestamp - INTERVAL '{period} minutes') as timestamp FROM wsb_comments WHERE 1=1 AND created_at >= current_timestamp - INTERVAL '{period} minutes'""")
        data = cursor.fetchall()
        self.conn.commit()
        cursor.close()
        
        return data
    def query_wsb_table(self, period=1):
        query = f"""SELECT TRIM(body) as body,sentiment as polarity,subjectivity,created_at FROM wsb_comments WHERE 1=1 AND created_at >= current_timestamp - INTERVAL '{period} minutes' ORDER BY created_at DESC"""

        data = pd.read_sql_query(query, self.conn)

        return data