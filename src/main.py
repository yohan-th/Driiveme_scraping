from scraping import *


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


driiveme = Driiveme()

html = driiveme.get_page('https://driiveme.com/rechercher-trajet.html')
driiveme.new_city_to_DB(html)

try:
    while 1:
        fetch_driiveme(driiveme)
        time.sleep(3*60*60)
except OSError as e:
    code = e.code if hasattr(e, 'code') else 'no_code'
    reason = e.reason if hasattr(e, 'reason') else 'no_reason'
    mail_yohan("[driiveme] Erreur python", f"{code}:{reason}")
