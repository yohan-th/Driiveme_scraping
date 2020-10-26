import os
import csv
import pandas as pd


def get_DB(file):
    if os.path.isfile(file):
        DB = pd.read_csv(file, index_col=False)
    else:
        DB = pd.DataFrame()
    return DB

def save_list_DB(file, value):
    DB_file = open(file, 'a+', newline='', encoding='utf-8')
    file = csv.writer(DB_file, delimiter=',')
    for val in value:
        file.writerow(val)
    DB_file.close()

def save_DB(file, value):
    DB_file = open(file, 'a+', newline='', encoding='utf-8')
    file = csv.writer(DB_file, delimiter=',')
    file.writerow(value)
    DB_file.close()

def update_val_DB(file, old_val, new_val):
    with open(file, 'r', newline='', encoding='utf-8') as DB_file:
        r = csv.reader(DB_file)  # Here your csv file
        lines = list(r)
        i = 0
        for line in lines:
            if line == old_val:
                lines[i] = new_val
                break
            i += 1
    with open(file, 'w', newline='', encoding='utf-8') as DB_file:
        writer = csv.writer(DB_file)
        writer.writerows(lines)
