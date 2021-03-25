import datetime
import json
from time import sleep

HOURS_IN_DAY = 24


class Schedule:

    def __init__(self, min_interval=60, config=None, logger=None):
        self.log = logger
        self.min_interval = min_interval
        self.schedule = {i: min_interval for i in range(HOURS_IN_DAY)}
        self.config = config
        self.reload()

    def reload(self):
        if self.config:
            with open(self.config, 'r') as conf:
                self.schedule = json.load(conf)

    def select_interval(self):
        self.reload()
        now_hour = datetime.datetime.now().hour
        return self.schedule.get(str(now_hour), self.min_interval)

    def do_sleep(self):
        interval = self.select_interval()
        self.log.debug(f"Спим {interval} сек")
        sleep(interval)
