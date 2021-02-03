import psycopg2
connect_str = "dbname='wsbapp' user='wsb' host='localhost' " + \
                  "password='3406'"
# use our connection values to establish a connection
conn = psycopg2.connect(connect_str)