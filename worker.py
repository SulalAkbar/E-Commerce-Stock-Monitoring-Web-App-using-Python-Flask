from scraper import main_scraper
import sqlite3
from sqlite3 import Error
import json
import csv
import os

db_file = 'scraping.db'

#Data Base Functions
def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)

    return conn


def adding_task(task):
    conn=create_connection(db_file)

    if conn is not None:
        sql = ''' INSERT INTO tasks(task_id,task_name,task_role,task_urls) VALUES (?,?,?,?) '''

        try:
            cur = conn.cursor()
            cur.execute(sql,task)
        except Exception as e:
            print('Error in inserting task -->',e)
    else:
        print('Error in database (create task)')

    task_id = cur.lastrowid
    conn.commit()
    conn.close()
    return task_id


##### Fetching tasks
def get_task():
    conn=create_connection(db_file)
    cur = conn.cursor()
    #cur.execute("SELECT player_name FROM players WHERE team_id=?", (team_id,))

    cur.execute("SELECT * FROM tasks where task_role == 'scrape'")


    rows = cur.fetchall()
    #print(rows)
    #print(len(rows))

    return rows

#Data Base function to get Tasks to be monitored
def get_monitor_tasks():


    conn=create_connection(db_file)
    cur = conn.cursor()
    #cur.execute("SELECT player_name FROM players WHERE team_id=?", (team_id,))

    cur.execute("SELECT * FROM tasks where task_role = 'monitor'")

    rows = cur.fetchall()
    #print(rows)
    #print(len(rows))

    return rows


# Enter fetch data into data base .
def enter_scraped_data(data):

    conn=create_connection(db_file)

    if conn is not None:

        if len(get_one_task_data(data[3])) == 0:

            sql = ''' INSERT INTO data_scraped(data_scraped_id,data_scraped_name,data_scraped_data,task_id) VALUES (?,?,?,?) '''

            try:
                cur = conn.cursor()
                cur.execute(sql,data)
            except Exception as e:
                print('Error in inserting Scraped Data --',e)

        else:

            sql = ''' UPDATE data_scraped
              SET data_scraped_data = ? WHERE task_id = ? '''

            try:
                d = (data[2],data[3]) #Updating data in data base ...
                cur = conn.cursor()
                cur.execute(sql,d)
            except Exception as e:
                print('Error in Updating Scraped Data --',e)


    else:
        print('Error in database (enter_scraped_data)')

    id = cur.lastrowid
    conn.commit()
    conn.close()
    return id

#Database function to fetch data using task_id
def get_one_task_data(task_id):

    conn=create_connection(db_file)
    cur = conn.cursor()
    #cur.execute("SELECT player_name FROM players WHERE team_id=?", (team_id,))
    try:

        cur.execute("SELECT * FROM data_scraped where task_id =?", (task_id,))


        rows = cur.fetchall()
    except Exception as e:
        print('Error in get_one_task_data() --',e)
    #print(rows)
    #print(len(rows))

    return rows

#DataBase functon to delete Tas from data base

def remove_task(task_id):
    print('Delete')
    conn=create_connection(db_file)
    cur = conn.cursor()
    #cur.execute("SELECT player_name FROM players WHERE team_id=?", (team_id,))
    try:
        cur.execute("DELETE FROM data_scraped WHERE task_id =?", (task_id,))
        cur.execute("DELETE FROM tasks WHERE task_id =?", (task_id,))
        conn.commit()

    except Exception as e:
        print('Error in delete_task() --',e)
    #print(rows)
    #print(len(rows))

######################## New Functions for New Table ################
#Function to fetch monitor status
def get_monitor_status():

    conn=create_connection(db_file)
    cur = conn.cursor()
    #cur.execute("SELECT player_name FROM players WHERE team_id=?", (team_id,))
    try:

        cur.execute("SELECT * FROM app_status where status_id =?", (1,))
        rows = cur.fetchall()
    except Exception as e:
        print('Error in get_one_task_data() --',e)
    #print(rows)
    #print(len(rows))

    return rows[0][2]

#Function to update monitor status in data base
def update_monitor_status(status):
    conn=create_connection(db_file)
    cur = conn.cursor()
    #cur.execute("SELECT player_name FROM players WHERE team_id=?", (team_id,))
    try:
        sql=''' UPDATE app_status
              SET monitor = ? WHERE status_id = ? '''
        rows=cur.execute(sql, (status,1))

        conn.commit()
        print('Updated')



    except Exception as e:
        print('Error in updating app_status --',e)
    #print(rows)
    #print(len(rows))


#DB Function to get Current Interval of Monitoring
def get_current_interval():

    conn=create_connection(db_file)
    cur = conn.cursor()
    #cur.execute("SELECT player_name FROM players WHERE team_id=?", (team_id,))
    try:

        cur.execute("SELECT * FROM app_status where status_id =?", (1,))
        rows = cur.fetchall()
    except Exception as e:
        print('Error in get_one_task_data() --',e)
    #print(rows)
    #print(len(rows))

    return rows[0][1]

#Function to update Interval
def update_interval_time(interval):
    conn=create_connection(db_file)
    cur = conn.cursor()
    #cur.execute("SELECT player_name FROM players WHERE team_id=?", (team_id,))
    try:
        sql=''' UPDATE app_status
              SET interval_time = ? WHERE status_id = ? '''
        rows=cur.execute(sql, (interval,1))
        conn.commit()
        print('Updated')


    except Exception as e:
        print('Error in updating Interval Time --',e)


###CSV MAKING FUNCTION
def making_csv(task_name,task_data):
    d = task_data

    here = os.path.dirname(os.path.realpath(__file__))
    filepath = os.path.join(here,'csv-files', task_name+'.csv')
    #file = task_name+'.csv'
    csv_file = open(filepath, 'a', newline="")
    writer = csv.writer(csv_file)
    for i in d:
        writer.writerow([i])
        for j in d[i]:
            writer.writerow([j,d[i][j]['name'],d[i][j]['price'],d[i][j]['stock']])

    csv_file.close()



###################################################################
#Function to check status of stocks
def check_stock(request,response):

    print('Checking Stock Availability ')

    m = ''
    s = '{x}'

    for i in request:
        for j in i['products']:
            print(j['stock'])
            m=m + s.format(x=j['stock']) + '\n'
            print(response[i['site']][j['url']]['stock'])

            m=m + s.format(x=response[i['site']][j['url']]['stock']) + '\n'
            for x in j['stock']:
                if x not in response[i['site']][j['url']]['stock']:
                    print(x,' Out of stock ',response[i['site']][j['url']]['name'])
                    m = m + s.format(x=(x,' Out of stock ',response[i['site']][j['url']]['name']+' '+j['url'])) +'\n'
    return m

#####################################################################################
"""
task_urls = [

    {   'site':'adidas',
        'products':[
                    {
                    'url':'https://www.adidas.co.uk/solarboost-19-shoes/EF1413.html',
                    'stock':['6']
                    },
                    {
                    'url':'https://www.adidas.co.uk/copa-gloro-19.2-soft-ground-boots/F36080.html',
                    'stock':['6']
                    },
                ]
    },

]


t3 = (None,'jogging','scrape',json.dumps(task_urls))

print('Creating Task')

try:
    create_task(t3)
except Exception as e:

    print('Error adding task',e)
print('Ok')


##########  Now Code for , Fetching tasks from data base ##########

"""

#rows=get_task()

#print(rows)
#print(json.loads(rows[0][3]))

"""

print('\n')
for i in json.loads(rows[0][3]):
    print(i)
    print('******')"""

#req = json.loads(rows[0][3])
#response = main_scraper(json.loads(rows[0][3]))


#task_id=rows[8][0]
#data_name = rows[8][1]
#data = response

#d1 = (None,data_name,json.dumps(data),task_id)
#enter_scraped_data(d1)

######### Testing get_monitor_tasks() #################


#rows=get_monitor_tasks()

#print(type(json.loads(rows[0][3])))

#print(delete_task(3))

#print(len(get_one_task_data(5)))
#################################

#rows = update_monitor_status('start')

#print(rows)

#update_interval_time(5)





