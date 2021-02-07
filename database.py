import psycopg2
import psycopg2.extras

class Db:
    def __init__(self):
        connect_str = "dbname='wsbapp' user='wsb' host='localhost' " + \
                        "password='3406'"
        # use our connection values to establish a connection
        self.conn = psycopg2.connect(connect_str)
        
    def insert_wsb_comment(self, data):
        cursor =  self.conn.cursor()
        query = f"""INSERT INTO data.wsb_comments (id, body, post, rddt_user, upvotes, downvotes, sentiment, subjectivity, created_at) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
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
        
        cursor.execute(f"""SELECT AVG(sentiment) as sentiment_avg, (current_timestamp - INTERVAL '{period} minutes') as timestamp FROM data.wsb_comments WHERE 1=1 AND created_at >= current_timestamp - INTERVAL '{period} minutes'""")
        data = cursor.fetchall()
        self.conn.commit()
        cursor.close()
        
        return data
