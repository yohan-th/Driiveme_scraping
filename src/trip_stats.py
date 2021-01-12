from tools import *
from database import *
import pandas as pd
import matplotlib.pyplot as plt
import sys
import base64
import io
from datetime import datetime, timedelta

class Stats():

    def __init__(self, database):
        self.DB = Database(database)
        self.trips = pd.read_sql_query("SELECT * FROM trips", self.DB.conn)
        self.cities = pd.read_sql_query("SELECT * FROM cities", self.DB.conn)

    def plot_new_cities(self):
        country = self.cities['country'].value_counts()

        labels = [n if v > country.sum() * 0.05 else ''
              for n, v in zip(country.index, country)]
        sizes = country.values.tolist()

        def my_autopct(pct):
            return ('%2.0f' % pct + '%') if pct > 5 else ''
        plt.pie(sizes, labels=labels, autopct=my_autopct, startangle=90)
        plt.legend(labels=country.index, loc=2, bbox_to_anchor=(-0.4, 1.1), fontsize='medium')
        month = datetime.today().strftime('%m')
        new = self.cities['add_date'].str.count(f"0./{month}/2020").sum()
        plt.title(f'Total cities : {len(self.cities) - new} + {new} new')

    def plot_new_trips(self):
        x = []
        y = []
        for delta in range(365, 1, -1):#nbr de jour from today -1
            x.append((datetime.now() - timedelta(delta)).strftime('%d/%m/%Y'))
            y.append(self.trips['date'].str.contains(x[-1]).sum())
        fig, ax = plt.subplots(figsize=(15, 3))
        ax.plot(x, y)

        fig.canvas.draw()
        labels = [item.get_text() for item in ax.get_xticklabels()]
        for n, label in enumerate(labels):
            if re.search('^01/.*', label):
                dt = datetime.strptime(label, "%d/%m/%Y")
                labels[n] = dt.strftime('%B')
            else:
                labels[n] = ''
        ax.set_xticklabels(labels)
        ax.title.set_text(f'Total trips : {len(self.trips)}')


    def plot_to_base64(self):
        pic_IObytes = io.BytesIO()
        plt.savefig(pic_IObytes, format='png')
        pic_IObytes.seek(0)
        pic_hash = base64.b64encode(pic_IObytes.read())
        return pic_hash


# pd.set_option('display.max_columns', None)
# pd.set_option('display.max_rows', None)

def send_stat():
    s = Stats('driiveme.db')
    s.plot_new_cities()
    b64_cities = s.plot_to_base64()
    s.plot_new_trips()
    b64_trips = s.plot_to_base64()

    content = f"""
    <html> 
        <head>
            <title>HTML E-mail</title>
        </head>
        <body>
            <div class="container" style="float:left;" >
                <div class="right" style="float:left;margin-left:200px;">
                    <h4 style="margin:50">Statistique in {datetime.today().strftime('%B')} since 11/2020</h4>
                    <p>Size database: {round(os.path.getsize('driiveme.db')/1000000)}MB</p>
                </div>
                <div class="left" style="float:left">
                    <img style="float:left;  margin-left:50px;" width="80%" src="data:image/png;base64,{b64_cities.decode('utf-8')}" alt="" />
                </div>
                
            </div>
            <img style="margin-left:50px;" width="80%" src="data:image/png;base64,{b64_trips.decode('utf-8')}" alt="Red dot" />
        </body>
    </html>
    """

    mail_yohan('Rapport scraping driiveme', content, False)
