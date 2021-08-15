import datetime
import os
import logging
from logging import handlers


class DailyRotatingFileHandler(handlers.RotatingFileHandler):

    def __init__(self, basedir: str) -> None:
        self._basedir = basedir
        self.baseFilename = self.getBaseFilename()
        self._today = datetime.date.today()
        super().__init__(self.baseFilename)

    def getBaseFilename(self) -> str:
        self._today = datetime.date.today()
        _basename = self._today.strftime("%Y-%m-%d") + ".log"
        return os.path.join(self._basedir, _basename)

    def shouldRollover(self, record: logging.LogRecord) -> bool:
        if self._today != datetime.date.today():
            self.baseFilename = self.getBaseFilename()
            return True
        return False
