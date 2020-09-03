from worker import get_task,get_monitor_tasks,adding_task,enter_scraped_data,get_one_task_data,remove_task,check_stock,get_current_interval,update_interval_time,making_csv,get_monitor_status,update_monitor_status
from apscheduler.schedulers.background import BackgroundScheduler
from flask import Flask,redirect, url_for
from flask_executor import Executor
from flask import render_template
from send_email import send_email,send_email_2
from scraper import main_scraper
from flask import send_file
from flask import request

import json
import time
import csv
import os

#################################
app = Flask(__name__)
executor = Executor(app)

####Global Code#################
chk = []    #
MONITOR = True
caution = None  ###Global variable for sending response notification

def start_monitor():
    monitor.submit(monitor_stocks,5)

count = 0
def sensor():
    """ Function for test purposes. """
    global count

    msg = 'I am running this time  '+ str(count)
    sub = 'Scheduler'

    #send_email(sub,msg)

    print("Scheduler is alive!",count)

    count = count + 1


###############################################################
@app.route("/")
def home():
    return render_template("base.html",on_off=get_monitor_status())

@app.route("/start_task")
def start_task():
    return render_template("task.html")

@app.route("/tasks", methods=["GET", "POST"])
def create_task():

    task = None
    if request.form:
        try:
            sites=int(request.form.get("sites"))
            sites = [i for i in range(sites)]
            return render_template("task.html",sites = sites)

        except Exception as e:
            print('Error in 1st block--',e)

        try:
            print('2nd block')
            sites_list = request.form.getlist("no_of_sites")
            no_of_products = request.form.getlist("no_of_products")

            data = {}
            for i in range(len(sites_list)):
                data[sites_list[i]] = int(no_of_products[i])
            global chk #List to identify sites and their urls

            chk = []
            print('Data to make chk list --',data)
            for i in data:
                for j in range(data[i]):
                    print(i)
                    chk.append(i)
            print('Check List  ',chk)
            return render_template("task.html",data = data)
        except Exception as e:
            print('Error in 2nd block--',e)
    return render_template("task.html")




#Function scrape for one time and saving tasks in data base
@app.route("/scrape", methods=["GET", "POST"])
def scrape():
    global chk
    #print('Chk List in Scrape()',chk)
    if request.form:
        try:
            print('Scrape Task')
            urls = request.form.getlist('url')
            stocks = request.form.getlist('stock')
            identifier = request.form.getlist('identifier')
            #print(urls,' ',stocks,' ',identifier)

            task_urls = []

            for i in range(len(chk)):

                if chk[i] == identifier[i]:
                    task_urls.append({
                        chk[i]:{
                            'url':urls[i],
                            'stock':stocks[i].split(',')
                        }
                        })

            #print(task_urls)

            distinct_sites = {}
            for i in chk:
                distinct_sites[i] = []

            #print('distinct_sites -- ',distinct_sites)

            for i in range(len(chk)):
                distinct_sites[chk[i]].append(task_urls[i][chk[i]])

            #print('Merging sites data :',distinct_sites)
            task_req = []
            for i in distinct_sites:
                task_req.append({
                    'site':i,
                    'products':distinct_sites[i]
                })
            print('Complete Formatted --',task_req)

            ###### Saving Task in data Base #######

            task_name = request.form.get('task_name')
            task_type = request.form.get('option')

            t = (None,task_name,task_type,json.dumps(task_req))

            print('Creating Task')

            try:
                task_id=adding_task(t)
                print('Task Saved')
            except Exception as e:
                print('Error adding task',e)


            #######################################
            executor.submit(long_running_job,task_req,task_id,task_name) #Submitting task to Scraper
            #long_running_job(task_req,task_id,task_name)


            return render_template("submit.html")

        except Exception as e:
            print('Error in Scrape()  ,',e)

    return render_template("task.html")

@app.route("/view_tasks")
def view_one_time_tasks():
    rows = get_task()
    monitor_rows = get_monitor_tasks()
    return render_template("tasks_submitted.html",rows = rows,monitor_rows = monitor_rows)

#Showing Scraped Result of Tasks
@app.route("/scraped_tasks")
def scraped_tasks():

    task_id = request.args.get('task')

    task=get_one_task_data(task_id)

    if task:
        task_name  = task[0][1]

        task_data = json.loads(task[0][2])

    else:
        task_data = None
        task_name = None



    return render_template('scraped_tasks.html',task_data=task_data,task_name=task_name)


@app.route("/delete_task", methods=["GET", "POST"])
def delete_task():

    if request.form:
        task_id=request.form.get('id')

        try:
            remove_task(task_id)
        except Exception as e:

            print('Error in delete_task()')

        print(task_id)

    return redirect(url_for('view_one_time_tasks'))
##################### NEW ROUTES ############################
#Code for Interval
#Function for setting monitoring interval
@app.route("/set_interval", methods=["GET", "POST"])
def set_interval():

    if request.form:
        interval = request.form.get('interval')

        update_interval_time(int(interval))

        reschedule()

    return render_template('set_monitor_interval.html',current_interval = get_current_interval())


#Function To Download Task data in CSV
@app.route("/download_csv", methods=["GET", "POST"])
def download_csv():

    if request.form:
        task_id = request.form.get('id')

        task=get_one_task_data(task_id)

        if task:
            task_name  = task[0][1]
            task_data = json.loads(task[0][2])

        else:

            task_data = None
            task_name = None

        #Creating csv file of task data and saving it in csv-folders
        making_csv(task_name,task_data)

        here = os.path.dirname(os.path.realpath(__file__))
        filepath = os.path.join(here,'csv-files', task_name+'.csv')

        return send_file(filepath, as_attachment=True)

        #return 'File Created'





###############################################################################
#Function to reschedule Interval
def reschedule():
    global sched
    sched.reschedule_job('my_job_id', trigger='interval',seconds= int(get_current_interval()))
    print('Rescheduled')

# Function to scrape one time ....
def long_running_job(task_req,task_id,data_name):
    #some long running processing her

    global caution

    print('Scraping Started ..')
    response = main_scraper(task_req)
    print('Scraping Finished ..')
    print(response)

    d = (None,data_name,json.dumps(response),task_id)
    try:
        enter_scraped_data(d)
        caution = True
    except Exception as e:

        print('Error adding Response data to database ...',e)

    print('Task Scraped and Saved into Data Base ...')


#Function for monitoring tasks Scraping
def long_running_monitoring_job(task_req,task_id,data_name):
    #some long running processing her

    global caution

    print('Scraping Started ..')
    print('Task Req -->',task_req)
    response = main_scraper(task_req)
    print('Scraping Finished ..')

    #Now Checking Stock Details

    msg=check_stock(task_req,response)
    sub = data_name
    send_email(sub,msg)

    send_email_2(sub,msg)

    print(response)

    d = (None,data_name,json.dumps(response),task_id)
    try:
        enter_scraped_data(d) # Saving Scraped Data in Data Base
        caution = True
    except Exception as e:

        print('Error Updating DataBase ...',e)

    print('Task Scraped and Saved into Data Base ...')

def monitor_stocks():

    print('Monitor Stocks Start')

    rows = get_monitor_tasks()
    for row in rows:

        long_running_monitoring_job(json.loads(row[3]),row[0],row[1])
        time.sleep(600)
    print('Monitor Stocks Ends Now Sleeping')
    #time.sleep(60)

#######################   Supporting Functions   ####################################
sched = None
MONITOR_BUTTON = None

print(sched)
if sched == None:

    print('Starting Proces ...')
    sched = BackgroundScheduler(daemon=True)
    sched.add_job(sensor,'interval',seconds = int(get_current_interval()),id='my_job_id')
    sched.start()
    sched.pause()
    #sched.resume()
    #MONITOR_BUTTON = 'Start'

    if get_monitor_status() == 'stop':
        sched.resume()

else:
    print('Process already created ...')


@app.route("/on_off")
def on_off():

    global MONITOR_BUTTON

    if get_monitor_status() == 'start':
        start()
        update_monitor_status('stop')
    else:
        stop()
        update_monitor_status('start')


    return render_template("base.html",on_off=get_monitor_status())

#@app.route("/start")
def start():
    global sched

    sched.resume()
#    return 'Process started'

#@app.route("/stop")
def stop():
    global sched
    sched.pause()
 #   return 'Process Stopped'


####Function to send Notification about Task Completion
@app.route("/check_response")
def check_response():

    global caution

    if caution == True:
        status = "On"
        print('\n\n\nCaution Task Completed\n\n\n')

        caution = None

    else:
        status = "jdbjdbdjf"
        caution = None

    return status


print('Hi')
#sched.start()
#time.sleep(60)
if __name__ == "__main__":
    app.run()


