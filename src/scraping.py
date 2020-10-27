from infos_resa import *
from tools import *
from database import *
from trip_threading import *


class Driiveme():

    def __init__(self):
        self.bgn_url_city = 'https://www.driiveme.com/rechercher-trajet/au-depart-de-'
        self.DB_cities = 'cities.csv'
        self.cities = self.init_cities()
        self.DB_trips = 'trips.csv'
        self.trips = self.init_trips() #non mis à jour
        self.new_trips = []

    def init_cities(self):
        if not os.path.isfile(self.DB_cities):
            with open(self.DB_cities, 'w') as f:
                f.write('CITY,DATE,UPDATED\n')
            html = self.get_page('https://driiveme.com/rechercher-trajet.html')
            self.new_city_to_DB(html)
        return (get_DB('cities.csv'))

    def init_trips(self):
        if not os.path.isfile(self.DB_trips):
            with open(self.DB_trips, 'w') as f:
                f.write(str(infos_trips()))
        return (get_DB('trips.csv'))

    def get_page(self, url):
        html = get_html(url, 3)
        if html == -1:
            mail_yohan("[driiveme] Erreur fatal get_html - EXIT",
                       "Can't reach rechercher-trajet.html. EXIT")
            sys.exit(1)
        return html

    def new_city_to_DB(self, html):
        new_city = 0
        html_cities = []
        if re.search('Suggestion de départs', html):
            html_cities = re.findall('.*au-depart-de-(.*?)(?:-et-a-|(?:\.html)).*', html)
        elif re.search('Suggestion de destinations', html):
            html_cities = re.findall('.*a-destination-de-(.*?).html.*', html)
        for city in html_cities:
            if not hasattr(self, 'cities') or not city in self.cities['CITY'].unique():
                new_city += 1
                save_DB('cities.csv', (city, time.strftime("%d/%m/%Y"), 0))
                self.cities = get_DB('cities.csv')
        return new_city

    def new_trip_to_DB(self, html):
        self.new_trips.clear()
        threadList = []
        trajets = re.findall('.*btn-rounded" href="(.*?)">.*', html)
        for trajet in trajets:
            ID = re.search('details-(\d+)\.', trajet).group(1)
            if not int(ID) in self.trips['ID'].unique():
                newthread = GetTripInfo_Thread('https://driiveme.com' + trajet, self.new_trips)
                newthread.start()
                threadList.append(newthread)
            while (threading.active_count() > 3):
                time.sleep(1)

        for curThread in threadList:
            curThread.join()

        save_list_DB('trips.csv', self.new_trips)
        self.trips = get_DB('trips.csv')
        return len(self.new_trips)

driiveme = Driiveme()

html = driiveme.get_page('https://driiveme.com/rechercher-trajet.html')
driiveme.new_city_to_DB(html)

while 1:
    for index, row in driiveme.cities.iterrows():
        if row['UPDATED'] == time.strftime("%d/%m/%Y"):
            continue
        url = 'https://www.driiveme.com/rechercher-trajet/'
        html = driiveme.get_page(url + 'au-depart-de-' + str(row['CITY']) + '.html')
        new_city_dep = driiveme.new_city_to_DB(html)
        new_trip_dep = driiveme.new_trip_to_DB(html)
        html = driiveme.get_page(url + 'a-destination-de-' + str(row['CITY']) + '.html')
        new_city_dest = driiveme.new_city_to_DB(html)
        new_trip_dest = driiveme.new_trip_to_DB(html)
        update_val_DB('cities.csv',
                      [row['CITY'], row['DATE'], str(row['UPDATED'])],
                      [row['CITY'], row['DATE'], time.strftime("%d/%m/%Y")])
        print(f'Départ: +{new_city_dep} city & +{new_trip_dep} trip - '
              f'Destination: +{new_city_dest} city & {new_trip_dest} trip'
              f' - {row["CITY"]}')