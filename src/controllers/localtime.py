import datetime


class LocalTime:
    @staticmethod
    def today():
        return datetime.date.today()

    @staticmethod
    def hour():
        return datetime.datetime.now().hour

    @staticmethod
    def date():
        return LocalTime.today().strftime("%B %d, %Y")

    @staticmethod
    def time():
        return datetime.datetime.now().strftime(
            "Its %H hours %M minutes and %S seconds"
        )
