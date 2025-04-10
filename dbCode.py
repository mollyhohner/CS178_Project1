import pymysql
import pymysql.cursors
import creds
import boto3

#Lab 13
# Section 1: MySQL

def get_conn():
    conn = pymysql.connect(
        host= creds.host,
        user= creds.user,
        password = creds.password,
        db=creds.db,
    )
    return conn

def execute_query(query, args=()):
    cur = get_conn.cursor(pymysql.cursors.DictCursor)
    cur.execute(query, args)
    rows = cur.fetchall()
    cur.close()
    return rows