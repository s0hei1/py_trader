import datetime as dt


class TimeService:

    def get_now(self):
        return dt.datetime.now(dt.UTC)