# -*- coding: utf-8 -*-
# author: wt
# date: '2019/1/4 0004 12:43'

import datetime


class Calendar(object):

    def __init__(self):
        pass

    def is_leap_year(self, year):  # 判断是否是闰年
        return True if (year % 100 != 0 and year % 4 == 0) or year % 400 == 0 else False

    def month_day(self, year, month):  # 判断当前月天数
        li = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
        if self.is_leap_year(year):
            li[1] = 29
        return li[month - 1]

    def total_day(self, year, month):  # 距1900年1月1日的天数
        days = 0
        for index_year in range(1900, year):
            days += 366 if self.is_leap_year(index_year) else 365
        for index_month in range(1, month):
            days += self.month_day(year, index_month)
        return days

    def get_calendar(self, year=datetime.datetime.now().year, month=datetime.datetime.now().month):  # 显示当前月

        year, month = year, month
        space_num = self.total_day(year, month) % 7 + 1
        # print("空格数",space_num)
        # print("星期",totalDay(year, month) % 7 + 1,"开始")
        _calendar = u"\n\u3000日\u3000一\u3000二\u3000三\u3000四\u3000五\u3000六\n"
        for i in range(1, self.month_day(year, month) + 1):
            if i == 1:
                for j in range(space_num % 7):
                    _calendar += u"\u3000\u3000"
            if i == int(datetime.datetime.now().day) and month == datetime.datetime.now().month:
                if i < 10:
                    _calendar += "\u30000%d)" % i
                else:
                    _calendar += "\u3000%2d)" % i
            else:
                if i < 10:
                    _calendar += "\u30000%d" % i
                else:
                    _calendar += "\u3000%2d" % i

            if (i + space_num) % 7 == 0:
                _calendar += "\n"
        return _calendar

    def get_year(self):
        return datetime.datetime.now().year

    def get_month(self):
        return datetime.datetime.now().month

if __name__ == "__main__":
    _calender = Calendar()
    print(_calender.get_calendar(2019, 1))
