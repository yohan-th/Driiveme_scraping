import time
import os
import sys
from subprocess import run
from datetime import datetime, timedelta

def mail_yohan(sujet, message, log=True):
    if log == True:
        logfile = open('mail.log', "a+", encoding='utf-8')
        clean_msg = message.replace('\n', '')
        logfile.write('['+time.strftime("%d/%m/%Y-%H:%M")+f'] {sujet}-{clean_msg}\n')
        logfile.close()
    try:
        run(["bash", "send_mail.sh", sujet, message])
    except OSError as e:
        time.sleep(10)
        run(["bash", "send_mail.sh", 'Error send mail', str(e)])
        time.sleep(10) 
        run(["bash", "send_mail.sh", sujet, message])

def log(txt:str):
    #print(txt)
    logfile = open('file.log', "a+")
    logfile.write('['+time.strftime("%d/%m/%Y-%H:%M")+']'+txt+'\n')
    logfile.close()

def is_end_month():
    tdy = datetime.now()
    if (tdy + timedelta(days=1)).strftime('%m') != tdy.strftime('%m'):
        return True
    else:
        return False

from urllib.request import Request, urlopen

def get_html(url:str, max_attempt:int=3):
    attempt = 1
    header = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.2704.84 Safari/537.36'

    while (attempt <= max_attempt):
        try:
            req = Request(url, headers={'User-Agent': header})
            with urlopen(req) as response:
                html = response.read().decode('utf-8')
                return html
        except OSError as e:
            code = e.code if hasattr(e, 'code') else 'no_code'
            reason = e.reason if hasattr(e, 'reason') else 'no_reason'

            log(f"Error {code} {attempt}/{max_attempt} {reason} : {url} - {e}")
            if attempt == max_attempt:
                mail_yohan("[driiveme] Erreur get_html", f"{code}:{reason}\n{e}\n{url}\nattempt {attempt}/{max_attempt}")
            if code == 503 or code == 500:
                time.sleep(1 * 60 * 60)
            time.sleep(10 * 60)
            attempt += 1
    return -1
