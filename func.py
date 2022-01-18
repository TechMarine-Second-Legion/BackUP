#coding:utf-8

import params

def sec_to_hours_with_sign(a):
    if a > params.limits.alert_time:
        sign = params.signs.alert_sign
        open("report","w")
    elif a > params.limits.warning_time:
        sign = params.signs.warning_sign
        open("report","w")
    else:
        sign = params.signs.positiv_sign
        open("report","w")

    minute = a//60
    sec = a%60

    hour = minute//60
    minute = minute%60

    day = hour//24
    hour%=24

    return f'{day} days, {hour}:{minute}:{sec}', sign


