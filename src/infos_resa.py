import re
import time
import pandas as pd


def infos_trips():
    ret = """URL,
           ID,
           Date,
           Brand,
           Dep_lieu,
           Dep_address,
           Dep_CP,
           Dep_GPS_latitude,
           Dep_GPS_longitude,
           Dest_lieu,
           Dest_address,
           Dest_CP,
           Dest_GPS_latitude,
           Dest_GPS_longitude,
           Date_debut_resa,
           Date_fin_resa,
           Cat_vehicule,
           Modele,
           Nbr_place,
           Distance_trajet,
           Pre_reservation"""
    return ret.replace("\n", "").replace(' ', '')

def init_trips():
    columns = ['URL',
               'ID',
               'Date',
               'Brand',
               'Depart_lieu',
               'Depart_address',
               'Depart_CP',
               'Depart_GPS_latitude',
               'Depart_GPS_longitude',
               'Dest_lieu',
               'Dest_address',
               'Dest_CP',
               'Dest_GPS_latitude',
               'Dest_GPS_longitude',
               'Date_debut resa',
               'Date fin resa',
               'Categorie vehicule',
               'Modele',
               'Nbr place',
               'Distance trajet',
               'Pré-réservation'
               ]
    ret = pd.DataFrame(columns=columns)
    return (ret)

def get_infos_resa(data:str):
    info_resa = []
    info_resa.append(re.search('rel="canonical" href="(.*)"', data).group(1))
    info_resa.append(re.search('details-(.*?)\.', info_resa[-1]).group(1))
    info_resa.append(time.strftime("%d/%m/%Y %H:%M"))
    info_resa.append(re.search('Cette location est proposée par (.*)">',data).group(1))  #brand
    info_resa.append(re.search('Trajet.*?(?:grayLight\">.*?){1}(.*?)<',data, re.MULTILINE|re.DOTALL).group(1))#departlieu
    info_resa.append(re.search('Trajet.*?(?:strong\">.*?){1}(.*?)<',data, re.MULTILINE|re.DOTALL).group(1))#depart_adrese
    info_resa.append(re.search('Trajet.*?(?:br/>.*?){1}(.*?)<',data, re.MULTILINE|re.DOTALL).group(1))#depart_CP
    info_resa.append(re.search('MAP_ORIGN_LAT = "(.*?)"',data).group(1))
    info_resa.append(re.search('MAP_ORIGN_LNG = "(.*?)"',data).group(1))

    info_resa.append(re.search('Trajet.*?(?:grayLight\">.*?){2}(.*?)<', data, re.MULTILINE|re.DOTALL).group(1))#arrive_lieu
    info_resa.append(re.search('Trajet.*?(?:strong\">.*?){2}(.*?)<', data, re.MULTILINE|re.DOTALL).group(1))#arrive_adrese
    info_resa.append(re.search('Trajet.*?(?:br/>.*?){2}(.*?)<', data, re.MULTILINE|re.DOTALL).group(1))#arrive_CP
    info_resa.append(re.search('MAP_DESTINATION_LAT = "(.*?)"', data).group(1))
    info_resa.append(re.search('MAP_DESTINATION_LNG = "(.*?)"', data).group(1))

    info_resa.append(re.search('partir du.*?strong">(.*?)</span>',data, re.MULTILINE|re.DOTALL).group(1))#date_debut
    info_resa.append(re.search('Arrivée max.*?"strong">(.*?)</span>',data, re.MULTILINE|re.DOTALL).group(1))#date_fin

    info_resa.append(re.search('Catégorie.*?class="large">(.*?)</span>',data, re.MULTILINE|re.DOTALL).group(1)) #categorie
    info_resa.append(re.search('Modèle.*?class="large">(.*?)</span>',data, re.MULTILINE|re.DOTALL).group(1))#Modele
    info_resa.append(re.search('Nombre de places.*?class="large">(.*?)</span>',data, re.MULTILINE|re.DOTALL).group(1))#nbr_place

    info_resa.append(re.search('une distance de (\d+) km',data).group(1)+'km')#distance
    info_resa.append('True') if re.search('Pré-réservation', data) else info_resa.append('False')

    return info_resa

#from tools import *

#print(get_infos_resa(get_html('https://driiveme.com/trajet/roissy-en-france-marignane-details-2214874.html')))

