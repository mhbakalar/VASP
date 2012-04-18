import os, datetime

def datefolder():
    today = datetime.date.today()
    yearstr = '{num:02d}'.format(num=int(str(today.year)[2:4]))
    monthstr = '{num:02d}'.format(num=today.month)
    datefolder = '{year}{month}{day}'.format(year=yearstr,
                                             month=monthstr,
                                             day=today.day)
    return datefolder
