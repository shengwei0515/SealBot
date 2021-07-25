import time
import logging
import threading
import asyncio
from concurrent.futures import ThreadPoolExecutor
from enum import Enum
logger = logging.getLogger(__name__)

class EnumColdDownStatus(Enum):
    Unlocked = 0
    Locked = 1


class ColdDownService:

    def __init__(self):
        self.cold_down_status = {}
        self._executor = ThreadPoolExecutor(1)
    
    def set_new_cold_down(self, cold_down_name):
        self.cold_down_status[cold_down_name] = EnumColdDownStatus.Unlocked

    async def lock_with_time(self, cold_down_name, cold_down_time_in_second):
        self.cold_down_status[cold_down_name] = EnumColdDownStatus.Locked
        logger.info(f"[Lock Cold Down] {cold_down_name} is {self.cold_down_status[cold_down_name]}")
        await asyncio.sleep(cold_down_time_in_second)
        self.cold_down_status[cold_down_name] = EnumColdDownStatus.Unlocked
        logger.info(f"[Unlock Cold Down] {cold_down_name} is {self.cold_down_status[cold_down_name]}")

    def is_cold_down(self, cold_down_name):
        if self.cold_down_status[cold_down_name] == EnumColdDownStatus.Locked:
            logger.info(f"{cold_down_name} is locked")
            return True
        else:
            logger.info(f"{cold_down_name} is unlocked")
            return False