# Webull bot by Gareth Chaston and Samuel Miller
import json
from webull import paper_webull
import time
import numpy
import schedule as sc
import datetime
from datetime import date as dt
from datetime import timedelta as td
import pandas as pd
import yfinance as yf


tradeType = input("Welcome! Enter p for paper-trading or c for cash-trading")
if tradeType == "p":
    wb = paper_webull()
else:
    wb = webull()

# while loop until correct login info is entered
z = 1
mfaTxt = None
loginCreds = None
while z != 0:
    eml = "samueldavidulysses@gmail.com"
    pwd = "Samandgar22"

    # checking if there is a matching email and password already in the file

    try:
        mfaTxt = open("login-info.txt","r")
        loginCreds = json.load(mfaTxt)  # if the login info file is empty it will not be able to convert from json and except block is thrown
        tempdict = loginCreds
        if tempdict["email"] == eml and tempdict["password"] == pwd:
            found = True
        if found == False:
            raise Exception  # incorrect email or pword so except block below is thrown

    except:
        try:
            tempMfa = None
            tempSqa = None
            tempSqid = None
            wb.get_security(eml)  # gets security question
            print(wb.get_security(eml))
            print(wb.next_security(eml))  # This can be used to request an alternate security question
            tempSqa = input("Answer: ")
            tempSqid = input("Enter the question id that was just returned: ")
            wb.get_mfa(eml) # gets the mfa code
            tempMfa = input("Check your account email and input the 6 digit Multi-Factor Identification Code: ")
            raise Exception
        except:
            info = {"email": eml, "password": pwd, "device": "Python Bot by Gareth Chaston and Sammy Miller",
                         "mfa": tempMfa, "security_id": tempSqid, "security_ans": tempSqa}
            mfaTxt.close()
            mfaTxt = open("login-info.txt","w")
            mfaTxt.write(json.dumps(info))
            mfaTxt.close()
            mfaTxt = open("login-info.txt", "r")
            loginCreds = json.load(mfaTxt)

    try:
        tempdict = loginCreds
        if tempdict["email"] == eml and tempdict["password"] == pwd:
            try:
                ta = wb.login(eml, pwd)
            except:
                ta = wb.login(tempdict["email"], tempdict["password"], tempdict["device"], tempdict["mfa"], tempdict["security_id"], tempdict["security_ans"])
        z = 0
    except:
        print("Incorrect email and/or password, please try again.")

    mfaTxt.close()

lastMinDict = {60: None, 50: None, 40: None, 30: None, 20: None, 10: None, 0: None}
x = None
def priceUpdate(cost, tick):
    global lastMinDict
    cost = wb.get_quote(tick)
    cost = float(cost['pPrice'])
    for secs in range(60, 0, -10):
        lastMinDict[secs] = lastMinDict[secs-10]
    lastMinDict[0] = cost
def startDayTrade(tick):
    global lastMinDict
    global x
    lastMinDict[0] = float(wb.get_quote(tick)['pPrice'])
    sc.every(1).minutes.do(print, lastMinDict)
    sc.every(10).seconds.do(priceUpdate,x,tick)
    while 1:
        sc.run_pending()
        time.sleep(1)

def volatility(tick):
    dateToday = dt.today()
    lastMonth = dateToday + datetime.timedelta( days = -30)
    data = yf.download(tick, start=lastMonth, end=dateToday)['Adj Close']
    vix = round(numpy.std(data), 2)
    print(vix)




tick = input("input ticker")
startDayTrade(tick)
#sc.every(1).minutes.do(print,lastMinDict)
#wb.login("samueldavidulysses@gmail.com","Samandgar22")

#print(wb.get_account())
#wb.get_account_id()
#wb.get_trade_token('218754')

'''wb.place_order(stock='AAPL', price=90.0, quant=2)
#wb.get_trade_token('123456')
orders = wb.get_current_orders()
print(orders)'''
closing = input("press enter to close")
