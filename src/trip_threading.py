import threading
from tools import *
from infos_resa import *

class GetTripInfo_Thread(threading.Thread):

    def __init__(self, url, new_trips):
        threading.Thread.__init__(self)
        self.url = url
        self.new_trips = new_trips

    def run(self):
        html = get_html(self.url, 3)
        if html == -1:
            log(f"[Threading err get trip] --> abort page {self.url}")
            return
        infos = get_infos_resa(html)
        #print(infos)
        self.new_trips = self.new_trips.append(infos)