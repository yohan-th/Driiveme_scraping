import time
import os
import sys
from subprocess import run, PIPE

def mail_yohan(sujet, message):
    logfile = open('mail.log', "a+", encoding='utf-8')
    logfile.write(f'{sujet}-{message}\n')
    logfile.close()
    #run(["sendmail", "-v", "contact@e.mail"], stdout=PIPE,
    #    input=f"Subject: {sujet} \n\n {message}", encoding='utf-8')

def log(txt:str):
    print(txt)
    logfile = open('file.log', "a+")
    logfile.write('['+time.strftime("%d/%m/%Y-%H:%M")+']'+txt+'\n')
    logfile.close()


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
                mail_yohan("[driiveme] Erreur get_html", f"{code}:{reason}\n{url}\nattempt {attempt}/{max_attempt}")
            if code == 503 or code == 500:
                time.sleep(10 * 60)
            time.sleep(60)
            attempt += 1
    return -1
