import pymysql
import pymysql.cursors
import creds
import boto3

TABLE_NAME = "ProjectOne"
dynamodb = boto3.resource('dynamodb', region_name="us-east-1")
table = dynamodb.Table(TABLE_NAME)

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
    rows = execute_query(""" SELECT city.name AS city_name, country.name AS country_name
                         FROM city
                         JOIN country ON city.countrycode = country.countrycode;
                         """)
'''