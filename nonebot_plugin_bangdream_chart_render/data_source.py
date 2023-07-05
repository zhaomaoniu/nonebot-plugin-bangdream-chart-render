import os

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from nonebot.log import logger

from .utils import fetch_data, read_xlsx_to_dict, read_csv_to_dict

class SongData(object):
    def __init__(self) -> None:
        self.inited = False

    async def init(self) -> None:
        await self._update_data()

        self.inited = True

        self._scheduler = AsyncIOScheduler()
        self._scheduler.add_job(self._update_data, 'interval', hours=1)
        self._scheduler.start()

    async def _update_data(self):
        self.song = await fetch_data("https://bestdori.com/api/songs/all.5.json", "data/song/", "all.5.json", False)
        self.band = await fetch_data("https://bestdori.com/api/bands/all.1.json", "data/band/", "all.1.json", False)

        if os.path.exists('data/bcr/nickname.csv'):
            self.nickname = read_csv_to_dict('data/bcr/nickname.csv')
        elif os.path.exists('data/bcr/nickname.xlsx'):
            self.nickname = read_xlsx_to_dict('data/bcr/nickname.xlsx')
        else:
            logger.warning("未配置歌曲别名文件，插件将不能正常运行！")
            self.nickname = {}

song_data = SongData()

