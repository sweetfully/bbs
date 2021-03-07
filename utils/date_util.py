import datetime
from django.utils import timezone


def get_date_interval(before_datetime):
    current_datetime = timezone.now()
    interval_date = (current_datetime - before_datetime).days
    last_month_days = get_last_month_day(current_datetime)
    if interval_date >= 360:      # 由于计算方式一个月使用30天计算，所以此处是360（12个月）
        year_num = interval_date // 365
        year_num = 1 if year_num == 0 else year_num
        return "%s年" % year_num
    elif interval_date >= last_month_days:
        month_num = interval_date // 30    # 一个月粗略估计是30天
        month_num = 1 if month_num == 0 else month_num
        return "%s月" % month_num
    if interval_date > 0:
        return "%s天" % interval_date
    elif interval_date == 0:
        return "1天"


# 获取上一个月的天数
def get_last_month_day(tmp_datetime):
    the_month_first_day = tmp_datetime.replace(day=1)
    last_month_first_day = (the_month_first_day - datetime.timedelta(days=1)).replace(day=1)
    last_month_days = (the_month_first_day - last_month_first_day).days
    return last_month_days
