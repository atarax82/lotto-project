import re
from bs4 import BeautifulSoup
from selenium import webdriver
from datetime import datetime, date
from project.apps.lotto.models import Ticket


def check_tickets_numbers(win_numbers, date=None, ignore_checked=False):
    ''' Checks if any of the tickets that are in the system has the winning
        combination of numbers, send emails to the winning users and updates the
        tickets automatically.
        
        Arguments:
            win_mumbers - List of 6 winning numbers.
            date - date of the winning ticket, default - today.
            ignore_checked - for debugging. If True, will check already
                checked tickets and send emails in case of victory again.
    '''
    print('Winning numbers: %s' % str(win_numbers))
    if not date:
        date = datetime.now().date()
        
    tickets = Ticket.objects.filter(date=date)
    if not ignore_checked:
        tickets = tickets.filter(checked=False)
    
    win_tickets = []
    for ticket in tickets:
        if ticket.check_numbers(win_numbers):
            win_tickets.append(ticket)
    
    return win_tickets
        

def check_tickets():
    url = "https://www.lotto.de/de/ergebnisse/lotto-6aus49/archiv.html"
    current_6of49 = []
    
    try:
        driver = webdriver.PhantomJS(
            executable_path="/root/phantom/phantomjs-2.0.0/bin/phantomjs")
        driver.get(url)
        soup = BeautifulSoup(driver.page_source,"html5lib")
        d = soup.find('div', {'class': 'zq_select'}).findAll('select')[1] \
            .find('option').text.split(',')[-1].strip();
        d = date(int(d[-4:]), int(d[3:5]), int(d[:2])) 
        
        for ul in soup.findAll("div", {"class": "balls"}):
            for i in re.findall(r'(?<=zahl\([1-6]\)">)\d{1,2}|(?<="last">)\d',
                    str(ul)):
                current_6of49.append(int(i))
    finally:
        try:
            driver.quite()
        except:
            pass
    
    return check_tickets_numbers(current_6of49, ignore_checked=False, date=d)

