import datetime


__all__ = ['jstoffset']


class JSTOffset(datetime.tzinfo):
    def utcoffset(self, dt):
        return datetime.timedelta(hours=9)

    def dst(self, dt):
        return datetime.timedelta(0)

    def tzname(self):
        return 'Asia/Tokyo'


jstoffset = JSTOffset()
