from scraping import *
from trip_stats import *
import subprocess
import gc


def fetch_driiveme(driiveme):
    for index, row in driiveme.cities.iterrows():
        if row['updated_date'] == time.strftime("%d/%m/%Y"):
            continue
        url = 'https://www.driiveme.com/rechercher-trajet/'
        html = driiveme.get_page(
            url + 'au-depart-de-' + str(row['city']) + '.html')
        new_city_dep = driiveme.new_city_to_DB(html)
        new_trip_dep = driiveme.new_trip_to_DB(html)
        html = driiveme.get_page(
            url + 'a-destination-de-' + str(row['city']) + '.html')
        new_city_dest = driiveme.new_city_to_DB(html)
        new_trip_dest = driiveme.new_trip_to_DB(html)
        driiveme.DB.update_city(row['city'], time.strftime("%d/%m/%Y"))
        if new_city_dep > 0 or new_trip_dep > 0 or new_trip_dest > 0 or new_city_dest > 0:
            log(f'Départ: +{new_city_dep} city & +{new_trip_dep} trip - '
                f'Destination: +{new_city_dest} city & +{new_trip_dest} trip'
                f' - {row["city"]}')
            result = subprocess.check_output(['free', '-m']).split()[12].decode("utf-8")
            log(f"Memory:{result}")


driiveme = Driiveme()

html = driiveme.get_page('https://driiveme.com/rechercher-trajet.html')
driiveme.new_city_to_DB(html)
rapport_send = False
try:
    while 1:
        result_bfr = subprocess.check_output(['free', '-m']).split()[12].decode("utf-8")
        gc.collect()
        result_aftr = subprocess.check_output(['free', '-m']).split()[12].decode("utf-8")
        log(f"Free memory when gc.collect() {result_bfr} --> {result_aftr}")
        if is_end_month() and rapport_send != True:
            send_stat()
            rapport_send = True
        elif not is_end_month() and rapport_send == True:
            rapport_send = False
        fetch_driiveme(driiveme)
        time.sleep(4*60*60)
except OSError as e:
    code = e.code if hasattr(e, 'code') else 'no_code'
    reason = e.reason if hasattr(e, 'reason') else 'no_reason'
    error = str(e)
    mail_yohan("[driiveme] Erreur python", f"{code}:{reason}\n{error}")
