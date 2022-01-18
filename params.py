#coding:utf-8

class limits:
    warning_time = 604800 # 604800 = 7 days
    alert_time = 864000 # 10 days

    limit_size_all = 100 # Gb
    limit_size_line = 10 # Gb
    mark_size = 70 # %

    product_formats = ["zip", '7z','gpg']

class signs:
    positiv_sign = '  '#"OK"
    #warning_sign = "\033[37mW\033[0m"

    warning_sign = 'w' #"W"
    #print("\033[4m\033[37m\033[44m{}\033[0m".format("Python 3"))

    alert_sign = "Cr"


