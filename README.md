# Terminator
Automation of terminated employee tickets in OS Ticket using email and Python

<br/><br/>
## What is Terminator
The script takes the automated email report from the Payroll system, scrapes out all the required data, then generates a ticket for the IT department to then check off/close off accounts, ensure user has returned hardware, setup any email forwards etc. 

## Why is this needed?
In our business, we had a big problem. When employees left from one of our many sites, they wouldn't always inform the IT department (via a IT ticket) and in turn all their accounts + logons would still be active - obviously a major security risk. Terminator was created to ensure no exited employees accounts are missed if their manager doesn't inform the IT department- it's used every week on payroll day. 

## What's used?
- Python 3
- External Python modules: Pandas, exchangelib and requests
- OS Ticket: https://osticket.com/

## See it in action
The automated report from payroll system that will be used.

![Optional Text](/README-IMAGES/email.PNG)

Run the script and watch the employees get TERMINATED!

![Optional Text](/README-IMAGES/terminator-CMD.gif)

Tickets are created and ready to be actioned in the ticketing system

![Optional Text](/README-IMAGES/os1.PNG)

All information is populated as per original email

![Optional Text](/README-IMAGES/os2.png)
