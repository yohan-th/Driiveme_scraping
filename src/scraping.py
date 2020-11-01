from infos_resa import *
from tools import *
import pandas as pd
from trip_threading import *
from database import *


class Driiveme():

    def __init__(self):

        self.bgn_url_city = 'https://www.driiveme.com/rechercher-trajet/au-depart-de-'
        self.DB = Database('driiveme.db')
        self.cities = pd.read_sql_query("SELECT * FROM cities", self.DB.conn)
        self.new_trips = []

    def get_page(self, url):
        html = get_html(url, 3)
        if html == -1:
            mail_yohan("[driiveme] Erreur fatal get_html - EXIT",
                       "Can't reach rechercher-trajet.html. EXIT")
            sys.exit(1)
        return html

    def new_city_to_DB(self, html):
        nb_new_city = 0
        html_cities = []
        if re.search('Suggestion de départs', html):
            html_cities = re.findall('.*au-depart-de-(.*?)(?:-et-a-|(?:\.html)).*', html)
        elif re.search('Suggestion de destinations', html):
            html_cities = re.findall('.*a-destination-de-(.*?).html.*', html)
        for city in html_cities:
            if not hasattr(self, 'cities') or not city in self.cities['city'].unique():
                nb_new_city += 1
                country = re.search(city+'.*?alt="(.*?)"', html, re.MULTILINE|re.DOTALL).group(1)
                self.DB.new_city((city, country, time.strftime("%d/%m/%Y"), 0))
                self.cities = pd.read_sql_query("SELECT * FROM cities", self.DB.conn)
        return nb_new_city

    def new_trip_to_DB(self, html):
        self.new_trips.clear()
        threadList = []
        trajets = re.findall('.*btn-rounded" href="(.*?)">.*', html)
        for trajet in trajets:
            ID = re.search('details-(\d+)\.', trajet).group(1)
            if not int(ID) in self.DB.get_trips_id():
                newthread = GetTripInfo_Thread('https://driiveme.com' + trajet, self.new_trips)
                newthread.start()
                threadList.append(newthread)
            while (threading.active_count() > 3):
                time.sleep(1)

        for curThread in threadList:
            curThread.join()

        for trip in self.new_trips:
            self.DB.new_trip(trip)

        return len(self.new_trips)
