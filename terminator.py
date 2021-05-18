import pandas as pd
import csv
import exchangelib as ex
import subprocess
import sys
import requests
import json
import time
import datetime


# API Key for OS Ticket:  123456789ABCDEFGH
# Only valid for requests via 172.16.5.5 (fake server IP where this automation script will reside)


# Func to get connect to email acc, search inbox and write to html file for parsing/scraping
def getMail():
    credentials = ex.Credentials('mydomain\svc_terminated.emp', 'f4keP4ssw0rd')
    account = ex.Account('svc_terminated.emp@mydomain.com.au', credentials=credentials, autodiscover=True)

    # Debug/logging
    for item in account.inbox.all().order_by('-datetime_received')[:100]:
        print(item.subject, item.sender, item.datetime_received)

    # Get latest email, write HTML file and delete email
    for item in account.inbox.all().order_by('-datetime_received')[:1]:
        emailbody = item.body
        with open('email_source.html', 'w', encoding='utf-8') as fdata:
            fdata.write(emailbody)
        item.delete()

# Func to scrape site name from HTML file create by getMail() and return list
def getTerminatedSite():
    tables = pd.read_html('email_source.html')
    dataframes = tables[1]
    emp_site = dataframes[4]
    emp_site_dirt = emp_site.values.tolist()
    emp_site_list = emp_site_dirt[1:]
    print(emp_site_list)
    return emp_site_list

# Func to scrape employee title from HTML file create by getMail() and return list
def getTerminatedTitle():
    tables = pd.read_html('email_source.html')
    dataframes = tables[1]
    emp_title = dataframes[3]
    emp_title_dirt = emp_title.values.tolist()
    emp_title_list = emp_title_dirt[1:]
    print(emp_title_list)
    return emp_title_list

# Func to scrape termination date from HTML file create by getMail() and return list
def getTerminatedDate():
    tables = pd.read_html('email_source.html')
    dataframes = tables[1]
    emp_termdata = dataframes[6]
    term_date_list_dirt = emp_termdata.values.tolist()
    term_date_list = term_date_list_dirt[1:]
    print(term_date_list)
    return term_date_list

# Func to scrape employee name from HTML file create by getMail() and return list
def getTerminatedName():
    # Read Tables into Dataframe
    tables = pd.read_html('email_source.html')
    dataframes = tables[1]
    df = dataframes[1]
    df2 = dataframes[2]

    # get first name + last name into lists
    firstNames = df.values.tolist()
    unformat_surnames = df2.values.tolist()

    # Add period in front of last name for formatting before merge
    surnames = ['.' + item for item in unformat_surnames]

    # Merge List
    names = [None] * (len(firstNames) + len(surnames))
    names[::2] = firstNames
    names[1::2] = surnames

    # clean name list
    finalNames = names[2:]
    cleanNames = [i + j for i, j in zip(finalNames[0::2], finalNames[1::2])]
    print(cleanNames)
    return cleanNames

# Generates CSV of emp names to be used later for logging and/or used with other scripts (eg. runPS())
def createCSV():
    with open("terminate_emp.csv", 'w', ) as csvFile:
        writer = csv.writer(csvFile, delimiter='\n')
        writer.writerow(getTerminatedName())

# TODO : Started working on this function to check Active Directory account status.
# This function runs the PS script to check .txt of names and print out their account status
def runPS():
    subprocess.Popen(['powershell.exe', 'C:\\Terminator\\Python3\\scripts\\get_ad_status.ps1'], stdout=None)


def emailAttach():
    with open('email_source.html', 'r', encoding='utf-8') as file:
        data = file.read().replace('\n', '')
        emaildata = data.replace("’", "'")
        return emaildata

# This function generates the ticket for each employee scraped from HTML/email file
def createTicket(name, date, site, emaildata):

    # converting date formats due to difference between Aus and USA format
    fixed_date = datetime.datetime.strptime(date, '%d/%m/%y').strftime('%m/%d/%y')

    # Create data template for API post and load in variables
    data = {"email": "svc_terminated.emp@mydomain.com.au",
            "name": "Terminated Employee",
            "subject": "Terminated Employee - Automated API ticket",
            "message": "data:text/html," + emaildata,
            "priority": "3",
            "topicId": "30",
            "empname": name,
            "emploc": "Head Office",
            "empdept": "IT",
            "emplastday": fixed_date,
            "branchapi": site}

    # Load required data into variable via JSON module's dump function
    json_data = json.dumps(data)

    # Create headers for API post (API Key)
    headers = {'X-API-Key': '123456789ABCDEFGH'}


    response = requests.post("https://itsupport.mydomain.com.au/api/http.php/tickets.json", data=json_data, headers=headers)

    # Logging/debug - show each terminated employee ticket being generated in CMD window
    for r in response:
        print("Ticket Generated, Ticket Number:" + str(r))

# Main function - used to call all others
def terminator():
    getMail()
    createCSV()
    name_list = getTerminatedName()
    date_list = getTerminatedDate()
    emaildata = emailAttach()
    site_list = getTerminatedSite()

    while len(name_list) > 0:
        print("***New Loop***")
        current_name = name_list[0]
        current_date = date_list[0]
        current_site = site_list[0]

        print(date_list)
        print(current_name)
        print(current_date)
        print(current_site)

        createTicket(current_name, current_date, current_site, emaildata)

        time.sleep(5)

        name_list.pop(0)
        date_list.pop(0)
        site_list.pop(0)


# Run the main function - They won't be back :P
terminator()

