from send.get_infos_resa import *
from send.tools import *
from send.database import *

def get_3_last_booked_trajet():

	html = get_html('https://www.driiveme.com/rechercher-trajet.html', 3)
	if html == -1:
		mail_yohan("[driiveme] Erreur fatal get_html - EXIT",
		           "Can't reach rechercher-trajet.html. EXIT")
		sys.exit(1)

	try:
		last_trajet_reserved = re.search(
			'.*Les derniers trajets r(.*)Les derni.*',
			html, re.MULTILINE | re.DOTALL)
		trajets = re.findall('.*href="(.*)".*', last_trajet_reserved.group(1),
		                     re.MULTILINE)
	except:
		mail_yohan("[driiveme] Erreur get last_trajet_reserved - EXIT",
		           f"scraping.py Can't find last trajet reserved with following page :\n\n\n{html}")
		sys.exit(1)
	return trajets


DB_file = 'data.csv'
all_trajet_ID = get_trajets_DB(DB_file)

while True:
	trajets = get_3_last_booked_trajet()

	for trajet in trajets:
		resa = re.search("/trajet/[\w-]+details-(\d+).html", trajet)

		if resa.group(1) in all_trajet_ID:
			continue

		url = 'https://www.driiveme.com' + resa.group(0)
		html = get_html(url, 5)
		if html == -1:
			continue

		all_trajet_ID.append(resa.group(1))

		try:
			info_resa = get_infos_resa(html, resa.group(1))
			info_resa.append(url)
		except:
			mail_yohan("[driiveme] Erreur get_infos_resa",
			           f"re.search fail pour extract les infos de la page suivante :\n\n\n{url}\n\n{html}")
			continue

		save_trajets_DB(DB_file, info_resa)

	time.sleep(60 * 10)
