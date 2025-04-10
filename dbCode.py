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
'''
def get_list_of_dictionaries(category):
    rows = execute_query(""" SELECT *
                         FROM 
                         
                         """)
'''