import re
import time
import random
import logging
from src.models.seal_coin import DaoSealCoin
logger = logging.getLogger(__name__)

GAMBLE_RATE = 0.6

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
    
    def _if_win_gamble(self):
        random_this_time = random.random()
        if random_this_time <= GAMBLE_RATE:
            return True
        else:
            return False

    def _run_gamble_percent(self, audience: str, percent: int):
        try:
            audience_info = self.db_repositoy.get_only_with_fiter(DaoSealCoin, DaoSealCoin.audience == audience)
        except:
            return f"@{audience} 目前還沒有豹仔幣帳號，請晚點再試試看 VoHiYo"
        coin_to_gamble = int(audience_info.coin * percent)
        if coin_to_gamble < 1:
            return f"@{audience} 只有 {audience_info.coin} 豹仔幣，不夠你賭喔 LUL"
        if self._if_win_gamble():
            audience_info.coin += coin_to_gamble
            self.db_repositoy.update(audience_info)
            return f"@{audience} 透過賭博贏得了 {coin_to_gamble}，現在有 {audience_info.coin} 豹仔幣囉 PogChamp"
        else:
            audience_info.coin -= coin_to_gamble
            self.db_repositoy.update(audience_info)
            return f"@{audience} 透過賭博輸了 {coin_to_gamble}，現在剩下 {audience_info.coin} 豹仔幣囉 LUL"

    def _run_gamble_number(self, audience, number):
        try:
            audience_info = self.db_repositoy.get_only_with_fiter(DaoSealCoin, DaoSealCoin.audience == audience)
        except:
            return f"@{audience} 目前還沒有豹仔幣帳號，請晚點再試試看 VoHiYo"
        if number > audience_info.coin:
            return f"@{audience} 只有 {audience_info.coin} 豹仔幣，不夠你賭喔 LUL"
        if self._if_win_gamble():
            audience_info.coin += number
            self.db_repositoy.update(audience_info)
            return f"@{audience} 透過賭博贏得了 {number}，現在有 {audience_info.coin} 豹仔幣囉 PogChamp"
        else:
            audience_info.coin -= number
            self.db_repositoy.update(audience_info)
            return f"@{audience} 透過賭博輸了 {number}，現在剩下 {audience_info.coin} 豹仔幣囉 LUL"

    def gamble(self, audience: str, gamble_arg: str):
        if gamble_arg.lower() == "all":
            return self._run_gamble_percent(audience, 1)

        re_percent = re.compile("\d*\%")
        match_percent = re.search(re_percent, gamble_arg)
        if match_percent != None:
            percent = int(match_percent[0].replace("%", ""))/100
            if percent > 1 or percent < 0:
                # percent not in 0~100
                return f"@{audience} 指令怪怪的，請再重新試試看 WutFace"
            else:
                return self._run_gamble_percent(audience, percent)
        else:
            try:
                gamble_number = int(gamble_arg)
                return self._run_gamble_number(audience, gamble_number)
            except Exception as e:
                logger.warning(f"command gamble with error {str(e)}")
                return f"@{audience} 指令怪怪的，請再重新試試看 WutFace"

    def start_share_coin(self):
        while True:
            for audience in self.get_all_audience():
                audience_info = self.db_repositoy.get_only_with_fiter(DaoSealCoin, DaoSealCoin.audience == audience)
                audience_info.coin += 10
                self.db_repositoy.update(audience_info)
                logger.info("give " + audience_info.audience + " 10 coin")
            logger.info(self.get_all_audience())
            time.sleep(60)

    def give_coin(self, sender, reveiver, num_of_coin, is_sender_mod):
        try: 
            num_of_coin = int(num_of_coin)
        except:
            return f"@{sender} 指令怪怪的，請再重新試試看 WutFace"

        try:
            reveiver_info = self.db_repositoy.get_only_with_fiter(DaoSealCoin, DaoSealCoin.audience == reveiver)
        except:
            return f"@{reveiver} 目前還沒有豹仔幣帳號，請晚點再試試看 VoHiYo"

        if not is_sender_mod:
            try:
                sender_info = self.db_repositoy.get_only_with_fiter(DaoSealCoin, DaoSealCoin.audience == sender)
            except:
                return f"@{sender} 目前還沒有豹仔幣帳號，請晚點再試試看 VoHiYo"
            if num_of_coin < 0:
                return f"@{sender} 還想偷錢啊 StinkyGlitch"
            if sender_info.coin < num_of_coin:
                return f"@{sender} 只有 {sender_info.coin} 豹仔幣，不夠給錢喔 LUL"
            sender_info.coin -= num_of_coin
            self.db_repositoy.update(sender_info)
        
        reveiver_info.coin += num_of_coin
        self.db_repositoy.update(reveiver_info)

        return f"{sender} 已經成功給了 @{reveiver} {num_of_coin} 豹仔幣"