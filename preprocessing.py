
#connection
import psycopg2
import json
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from selenium import webdriver
from selenium.webdriver.common.by import By

def authenticate_connect(username, password, database_name):
    connection1 = None
    try:
        connection1 = psycopg2.connect(database=database_name, user=username, password=password)
        connection1.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        info = {
            "username" : username,
            "password" : password,
            "database" : database_name
        }
        verify = True
        json_object = json.dumps(info, indent=4)
        with open("logininfo.json", "w") as outputfile:
            outputfile.write(json_object)
    except (Exception, psycopg2.DatabaseError) as error:
        verify = False
    return verify


def connect():
    """ Connect to the PostgreSQL database server """
    connection1 = None
    f = open('logininfo.json', "r")
    data = json.load(f)
    username = data['username']
    pwd = data['password']
    database_name = data['database']
    try:
        # read connection parameters

        connection1 = psycopg2.connect(database=database_name, user=username, password=pwd)
        connection1.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        # create a cursor
        cur = connection1.cursor()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        return cur

# to obtain QEP using the default settings in postgreSQL
def runQuery(text):
    sql_string = "EXPLAIN (analyze, verbose, costs, format JSON) " + text

    try:
        cursor = connect()
        cursor.execute(sql_string)
        queryOutput = cursor.fetchall()
        queryExecuted = True
    except(Exception, psycopg2.DatabaseError) as error:
        queryOutput = "Please check your sql statement: \n" + text
        queryExecuted = False
    finally:
        cursor.close()

    # open text file
    with open('actual_queryplans/queryplan.json', 'w') as f:
        json.dump(queryOutput, f, ensure_ascii=False, indent=2)

    # to obtain the 3 different AQPs
    getAQP(text)
    return queryExecuted

def getAQP(text):
    # default setting 
    sql_string = "EXPLAIN (analyze, verbose, costs, format JSON) " + text
    # holds the 3 different settings to generate 3 different query plan base on individual settings
    setting_list = [

        [
            ["ENABLE_NESTLOOP","OFF"],
            ["ENABLE_SEQSCAN","OFF"]
        ],

        [
            ["ENABLE_HASHJOIN","OFF"],
            ["ENABLE_BITMAPSCAN","OFF"]
        ],

        [
            ["ENABLE_INDEXSCAN","OFF"],
            ["ENABLE_MERGEJOIN","OFF"],
        ]
    ]
    # limit the number of AQP generated to 3
    num_of_AQP = 3
    for i in range(num_of_AQP):
        setting_string = ''
        for setting in setting_list[i]:
            setting_string += f'SET {setting[0]} to {setting[1]};'
        changed_query = setting_string + sql_string
        try:
            cursor = connect()
            cursor.execute(changed_query)
            queryOutput = cursor.fetchall()
            queryExecuted = True
        except(Exception, psycopg2.DatabaseError) as error:
            queryOutput = "Please check your sql statement: \n" + text
            queryExecuted = False
        finally:
            cursor.close()

        # open text file
        with open(f'actual_queryplans/altqueryplan{i}.json', 'w') as f:
            json.dump(queryOutput, f, ensure_ascii=False, indent=2)
    return queryExecuted


# function to create the QEP Tree Diagram
# Uses a website to help generate QEP TREE
def createQEPTreeDiagram():

    with open('actual_queryplans/queryplan.json') as json_file:
        data = json.load(json_file)
    dict_plan_inner = data[0][0]


    webBrowser = webdriver.EdgeOptions()
    webBrowser.add_experimental_option("detach", True)

    # Open Chrome
    driver = webdriver.Edge(options=webBrowser, executable_path='msedgedriver.exe')

    # Webpage settings
    driver.maximize_window()
    driver.get("https://tatiyants.com/pev/#/plans/new")
    driver.implicitly_wait(5)
    
    driver.find_element(By.CLASS_NAME, "input-box-lg").send_keys(json.dumps(dict_plan_inner))
    driver.implicitly_wait(5)

    driver.find_element(By.CLASS_NAME, "btn-default").click()

# function to create the first AQP Tree Diagram
def createFirstAQPTreeDiagram():

    with open('actual_queryplans/altqueryplan0.json') as json_file:
        data = json.load(json_file)
    dict_plan_inner = data[0][0]


    webBrowser = webdriver.EdgeOptions()
    webBrowser.add_experimental_option("detach", True)

    # Open Chrome
    driver = webdriver.Edge(options=webBrowser, executable_path='msedgedriver.exe')

    # Webpage settings
    driver.maximize_window()
    driver.get("https://tatiyants.com/pev/#/plans/new")
    driver.implicitly_wait(5)

    driver.find_element(By.CLASS_NAME, "input-box-lg").send_keys(json.dumps(dict_plan_inner))
    driver.implicitly_wait(5)

    driver.find_element(By.CLASS_NAME, "btn-default").click()

# function to create the second AQP Tree Diagram

def createSecondAQPTreeDiagram():
    with open('actual_queryplans/altqueryplan1.json') as json_file:
        data = json.load(json_file)
    dict_plan_inner = data[0][0]

    webBrowser = webdriver.EdgeOptions()
    webBrowser.add_experimental_option("detach", True)

    # Open Chrome
    driver = webdriver.Edge(options=webBrowser, executable_path='msedgedriver.exe')

    # Webpage settings
    driver.maximize_window()
    driver.get("https://tatiyants.com/pev/#/plans/new")
    driver.implicitly_wait(5)

    driver.find_element(By.CLASS_NAME, "input-box-lg").send_keys(json.dumps(dict_plan_inner))
    driver.implicitly_wait(5)

    driver.find_element(By.CLASS_NAME, "btn-default").click()

# function to create the third AQP Tree Diagram

def createThirdAQPTreeDiagram():
    with open('actual_queryplans/altqueryplan2.json') as json_file:
        data = json.load(json_file)
    dict_plan_inner = data[0][0]


    webBrowser = webdriver.EdgeOptions()
    webBrowser.add_experimental_option("detach", True)

    # Open Chrome
    driver = webdriver.Edge(options=webBrowser, executable_path='msedgedriver.exe')

    # Webpage settings
    driver.maximize_window()
    driver.get("https://tatiyants.com/pev/#/plans/new")
    driver.implicitly_wait(5)

    driver.find_element(By.CLASS_NAME, "input-box-lg").send_keys(json.dumps(dict_plan_inner))
    driver.implicitly_wait(5)

    driver.find_element(By.CLASS_NAME, "btn-default").click()



