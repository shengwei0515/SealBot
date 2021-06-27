import time
import logging
from src.models.seal_coin import DaoSealCoin
logger = logging.getLogger(__name__)


class SealCoinService:
    
    def __init__(self, db_repositoy):
        self.audience_list = []
        self.db_repositoy = db_repositoy

    def get_all_audience(self):
        return self.audience_list
    
    def add_audience(self, audience):
        # remove useless string
        audience = audience.replace("\r","")

        # check if audience exist
        query_result = self.db_repositoy.get_with_fiter(DaoSealCoin, DaoSealCoin.audience == audience)
        if query_result.count() == 0:
            new_audience = DaoSealCoin(audience=audience, coin=100)
            self.db_repositoy.create(new_audience)
        # creat user here
        if audience not in self.audience_list:
            self.audience_list.append(audience)
    
    def remove_audience(self, audience):
        self.audience_list.remove(audience)

    def query_coin(self, audience):
        audience = audience.replace("\r","")
        result = self.db_repositoy.get_only_with_fiter(DaoSealCoin, DaoSealCoin.audience == audience)
        return result.coin

    def start_share_coin(self):
        while True:
            for audience in self.get_all_audience():
                audience_info = self.db_repositoy.get_only_with_fiter(DaoSealCoin, DaoSealCoin.audience == audience)
                audience_info.coin += 10
                self.db_repositoy.update(audience_info)
                logger.info("give " + audience_info.audience + " 10 coin")
            logger.info(self.get_all_audience())
            time.sleep(60)