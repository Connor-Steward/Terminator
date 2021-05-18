# Terminator
Automation of terminated employee tickets in OS Ticket using email and Python


## Why is this needed?
In our business, we had a big problem. When employees left from one of our many sites, they wouldn't always inform the IT department (via a IT ticket) and in turn all their accounts + logons would still be active - obviously a major security risk. Terminator was created to ensure no exited employees accounts are missed if their manager doesn't inform the IT department- it's used every week on payroll day. 

## What is Terminator
The script takes the automated email report from the Payroll system, scrapes out all the required data, then generates a ticket for the IT department to then check off/close off accounts, ensure user has returned hardware, setup any email forwards etc. 

## What's used?
- Python 3
- External Python modules: Pandas, exchangelib and requests
- OS Ticket: https://osticket.com/

## See it in action
First, the automated report from payroll system that will be used.
