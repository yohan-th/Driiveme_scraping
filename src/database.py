import re
import sqlite3 as sql

class Database():

    def __init__(self, dbname):
        self.sql_create_cities_table = """CREATE TABLE IF NOT EXISTS cities (
                                        id integer PRIMARY KEY,
                                        city text NOT NULL,
                                        country text NOT NULL,
                                        add_date text NOT NULL,
                                        updated_date text NOT NULL
                                    );"""

        self.sql_create_trips_table = """CREATE TABLE IF NOT EXISTS trips (
                                        id integer PRIMARY KEY,
                                        url text,
                                        trip_id integer,
                                        date text,
                                        brand text,
                                        dep_lieu text,
                                        dep_address text,
                                        dep_CP text,
                                        dep_gps_latitude text,
                                        dep_gps_longitude text,
                                        dest_lieu text,
                                        dest_address text,
                                        dest_cp text,
                                        dest_gps_latitude text,
                                        dest_gps_longitude text,
                                        date_debut_resa text,
                                        date_fin_resa text,
                                        cat_voiture text,
                                        modele text,
                                        nbr_place text,
                                        distance_trajet text,
                                        pre_reservation integer
                                    );"""
        self.conn = self.init_db(dbname)
        self.trips_id = self.get_trips_id()


    def init_db(self, db_file):
        conn = sql.connect(db_file)
        c = conn.cursor()
        c.execute(self.sql_create_trips_table)
        c.execute(self.sql_create_cities_table)
        return conn

    def new_trip(self, trip):
        sql = ''' INSERT INTO trips(url,trip_id,date,brand,dep_lieu,dep_address,
                                    dep_CP,dep_gps_latitude,dep_gps_longitude,
                                    dest_lieu,dest_address,dest_cp,dest_gps_latitude,
                                    dest_gps_longitude,date_debut_resa,date_fin_resa,
                                    cat_voiture,modele,nbr_place,distance_trajet,pre_reservation)
                  VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?) '''
        cur = self.conn.cursor()
        cur.execute(sql, trip)
        self.conn.commit()
        return cur.lastrowid

    def new_city(self, city):
        sql = ''' INSERT INTO cities(city,country,add_date,updated_date)
                  VALUES(?,?,?,?) '''
        cur = self.conn.cursor()
        cur.execute(sql, city)
        self.conn.commit()
        return cur.lastrowid

    def get_trips_id(self):
        cur = self.conn.cursor()
        ids = cur.execute('SELECT trip_id FROM trips').fetchall()
        ret = [x[0] for x in ids]
        return ret

    def get_cities(self):
        cur = self.conn.cursor()
        all_city = cur.execute('SELECT city FROM cities').fetchall()
        ret = [x[0] for x in all_city]
        return ret

    def update_city(self, city, new_value):
        sql = f''' UPDATE cities
                      SET updated_date = ?
                      WHERE city REGEXP "^{city}$"'''
        self.conn.create_function('regexp', 2, lambda x, y: 1 if re.search(x, y) else 0)
        cur = self.conn.cursor()
        cur.execute(sql, (new_value,))
        self.conn.commit()

