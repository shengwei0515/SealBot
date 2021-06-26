import time
import logging
logger = logging.getLogger(__name__)


class SealCoinService:
    
    def __init__(self):
        self.audience_list = []

    def get_all_audience(self):
        return self.audience_list
    
    def add_audience(self, audience):
        if audience not in self.audience_list:
            self.audience_list.append(audience.replace("\r",""))
    
    def remove_audience(self, audience):
        self.audience_list.remove(audience)

    def start_share_coin(self):
        while True:
            logger.debug(self.get_all_audience())
            print(self.get_all_audience())
            time.sleep(3)