import os
import csv

def get_trajets_DB(file):
	all_trajet_ID = []
	if os.path.isfile(file):
		with open(file, newline='', encoding='utf-8') as DB_file:
			DB = csv.reader(DB_file, delimiter=';')
			for row in DB:
				all_trajet_ID.append(row[0])
	return all_trajet_ID

def save_trajets_DB(file, info_resa):
	DB_file = open(file, 'a+', newline='', encoding='utf-8')
	file = csv.writer(DB_file, delimiter=';')
	file.writerow(info_resa)
	DB_file.close()