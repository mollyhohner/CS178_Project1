import pymysql
import pymysql.cursors
import creds
import boto3

TABLE_NAME = "ProjectOne"
dynamodb = boto3.resource('dynamodb', region_name="us-east-1")
table = dynamodb.Table(TABLE_NAME)

# Connect to the 
def get_conn():
    conn = pymysql.connect(
        host= creds.host,
        user= creds.user,
        password = creds.password,
        db=creds.db,
        cursorclass=pymysql.cursors.DictCursor
    )
    return conn

def execute_query(query, args=()):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute(query, args)
    rows = cur.fetchall()
    cur.close()
    return rows