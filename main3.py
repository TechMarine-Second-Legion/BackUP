#!/usr/bin/python3
#coding:utf-8

version = "Version: 0.5"

import os, time, datetime, psutil
import params, func, mail_def1

from prettytable import PrettyTable
#from prettytable import MSWORD_FRIENDLY, DEFAULT, PLAIN_COLUMNS, MARKDOWN, ORGMODE

full_size=0

# Собирание всех линеек у одного пользователя
def to_prettytable(user, lines):
    part_of_table = []

    for i in lines:
        part_of_table.append([])
        part_of_table[-1].append(" ")
        for j in i:
            part_of_table[-1].append(j)
        part_of_table[-1].append(' ')
    part_of_table[0][0] = user

    part_of_table[-1][-1] = round((sum(row[-2] for row in part_of_table)),3)

    for i in range(len(part_of_table)):
        part_of_table[i][-2] = str(part_of_table[i][-2])
        len_now = len(part_of_table[i][-2][part_of_table[i][-2].rfind('.'):])
        part_of_table[i][-2]+='0'*(4 - len_now)
        part_of_table[i][-2] = part_of_table[i][-2].rjust(7)
    return part_of_table

# Составление одной линейки
def user_lines(user):
    all_product = os.listdir(f'/home/{user}/')
    zip_prod = [i for i in all_product if i.split('.')[-1] in params.limits.product_formats]
    zip_prod.sort(key=len, reverse=True)

   print(f"Все файлы типа '{params.limits.product_formats}' у пользователя {user}:\n{zip_prod}")
   print(f"Общее количество: {len(zip_prod)}", end='\n\n')

    exa = '202'
    # В имени архива есть дата, начинается с года. До неё - имя линейки.

    lines = []

    for i in zip_prod:
        b = zip_prod.copy()
        #print(f"i: {i}")

        # Имя линейки и год разделены знаком "-"
        line = i[:i.find(exa) - (i[i.find(exa)-1]=='-')]

        cnt_in_line = 0
        size_of_line = 0
        last_update = 0

        # Поиск продуктов линейки. Полагается, что до exa имя лиинейки, а после только дата
        for j in zip_prod:
            if j.find(line) != -1:

                cnt_in_line+=1
                size_of_line+=os.stat(f'/home/{user}/{j}').st_size
                if last_update < os.stat(f'/home/{user}/{j}').st_mtime:
                    last_update = os.stat(f'/home/{user}/{j}').st_mtime
                b.remove(j)
        zip_prod = b.copy()

        global full_size
        if cnt_in_line!=0:
#           print(f"Линейка '{line}', последнее обновление {time.time()-last_update} секунд назад , количество: {cnt_in_line}, размер линейки: {size_of_line} Byte")#, end='\n\n')
            last_time_apd, status_sign = func.sec_to_hours_with_sign(int(time.time()-last_update))
            full_size += size_of_line/1024**3
            lines.append([line, last_time_apd,status_sign, cnt_in_line, round(size_of_line/1024**3,3)])
    lines.sort()
    return lines

def main(params = params):

    os.system('clear')

    #Get all users
    users = os.listdir('/home/')

    # Delete unbackup users
    users = list(set(users) - set(params.none_backup_users))
    users.sort()
    print(f"Список всех пользователей:\n{users}", end='\n\n')

    # User, line, Last_update, Cnt, Size, Over
    table = PrettyTable()
    table.field_names = ["User", "Line", "Last_update_ago",'Status', "Cnt", "Size (Gb)", "Full_size (Gb)"]

    global full_size
    for i in users:
        table.add_rows(to_prettytable(i, user_lines(i)))
        if i != users[-1]:
            table.add_row([' ' for i in range(len(table.field_names))])

    table.add_row([' ' for i in range(len(table.field_names)-1)].append(round(full_size,3))) # append full_size в -1-1
    table.align['Line'] = 'l'
    print(table)

    if os.path.exists("report"):
        os.remove("report")

        text = version+'\n'
        text += "Cформирован: "+ str(datetime.datetime.now())+"\n\n"
        text += "Обсервация докладывает: \n"
        text += str(table)+'\n'
        text += f"Используется: {round(psutil.disk_usage('/home/').used/(1024**3),3)} Gb"+'\n'
        text += f"Свободно: {round(psutil.disk_usage('/home').free/(1024**3),3)} GB"+'\n'
        with open("report.txt","w") as f:
            f.write(text)
        print(f"Используется: {round(psutil.disk_usage('/home/').used/(1024**3),3)} Gb")
        print(f"Свободно: {round(psutil.disk_usage('/home').free/(1024**3),3)} GB")
        #mail_def1.send_mail(text)
        print("Done")

main()

