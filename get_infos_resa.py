import re
import time

#[0] Booking number
#[1] Date
#[2] Brand
#[3] Depart_lieu
#[4] Depart_address
#[5] Depart_CP
#[6] GPS latitude
#[7] GPS longitude
#[8] Destination_lieu
#[9] Destination_address
#[10] Destination_CP
#[11] GPS latitude
#[12] GPS longitude
#[13] Date debut reservation
#[14] Date fin reservation
#[15] Categorie vehicule
#[16] Modele (if communicate)
#[17] Nbr place
#[18] Distance trajet
#[19] URL

def get_infos_resa(data:str, booking_nb:str):
  info_resa = []
  info_resa.append(booking_nb)
  info_resa.append(time.strftime("%d/%m/%Y %H:%M"))
  info_resa.append(re.search('.*Cette location est proposée par (.*)">.*',data).group(1))                            #brand
  info_resa.append(re.search('.*Départ.*xlarge strong">(.*)</span>.*',data).group(1))   #departlieu

  info_resa.append(re.search('Départ.*?class="thin">(.*?)</span>',data, re.MULTILINE|re.DOTALL).group(1))       #depart_adrese
  info_resa.append(re.search('Départ.*?class="large">(.*?)</span>',data, re.MULTILINE|re.DOTALL).group(1))      #depart_CP
  info_resa.append(re.search('MAP_ORIGN_LAT = "(.*?)"',data).group(1))
  info_resa.append(re.search('MAP_ORIGN_LNG = "(.*?)"',data).group(1))

  info_resa.append(re.search('Arrivée.*?xlarge strong">(.*?)</span>', data, re.MULTILINE|re.DOTALL).group(1))    #arrive_lieu
  info_resa.append(re.search('Arrivée.*?class="thin">(.*?)</span>', data, re.MULTILINE|re.DOTALL).group(1))      #arrive_adrese

  info_resa.append(re.search('Arrivée.*?class="large">(.*?)</span>', data, re.MULTILINE|re.DOTALL).group(1))     #arrive_CP
  info_resa.append(re.search('MAP_DESTINATION_LAT = "(.*?)"', data).group(1))
  info_resa.append(re.search('MAP_DESTINATION_LNG = "(.*?)"', data).group(1))

  info_resa.append(re.search('partir du.*class="xlarge strong">(.*?)</span>',data).group(1))                           #date_debut
  info_resa.append(re.search('max le.*<span class="xlarge strong">(.*?)</span>',data).group(1))                           #date_fin

  info_resa.append(re.search('Catégorie.*?class="large">(.*?)</span>',data, re.MULTILINE|re.DOTALL).group(1))   #categorie
  info_resa.append(re.search('Modèle.*?class="large">(.*?)</span>',data, re.MULTILINE|re.DOTALL).group(1))      #Modele
  info_resa.append(re.search('Nombre de places.*?class="large">(.*?)</span>',data, re.MULTILINE|re.DOTALL).group(1))#nbr_place

  info_resa.append(re.search('<span class="large gray">(\d+) km</span>',data).group(1)+'km')#distance

  return info_resa

