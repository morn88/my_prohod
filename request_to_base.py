import fdb
import datetime
import time


def my_request(date1, date2):
    my_date1 = date1
    my_date2 = date2
    full_dict = {}
    # con = fdb.connect(host='10.115.194.151/3050', database='C:\SCD17K.fdb',
    #                   user='sysdba', password='masterkey', charset='win1251')
    con = fdb.connect(dsn='SCD17K.FDB', user='SYSDBA', password='masterkey', charset='win1251')
    curs = con.cursor()

    """ Получение списка устройств пропускной системы """
    my_time = time.time()
    curs.execute("SELECT ID_AREAS_TREE, DISPLAY_NAME FROM AREAS_TREE ORDER BY ID_AREAS_TREE")
    device_list = curs.fetchall()
    device_dict = dict(device_list)
    time1 = time.time() - my_time
    print('Первый запрос: ', time1)

    """ Получение списка отделов предприятия """
    my_time = time.time()
    curs.execute("SELECT ID_REF, DISPLAY_NAME FROM SUBDIV_REF ORDER BY ID_REF")
    subdiv_list = curs.fetchall()
    subdiv_dict = dict(subdiv_list)
    time2 = time.time() - my_time
    print('Второй запрос: ', time2)

    """ Получение списка профессий предприятия """
    my_time = time.time()
    curs.execute("SELECT ID_REF, DISPLAY_NAME FROM APPOINT_REF ORDER BY ID_REF")
    appoint_list = curs.fetchall()
    appoint_dict = dict(appoint_list)
    time3 = time.time() - my_time
    print('Третий запрос: ', time3)

    """ Получене списка возможных событий КПС """
    my_time = time.time()
    curs.execute("SELECT * FROM MODEL_EVENTS ORDER BY INNER_NUMBER")
    events_list = curs.fetchall()
    new_events_list = []
    for i in events_list:
        new_events_list.append(i[2:4])
    events_dict = dict(new_events_list)

    time4 = time.time() - my_time
    print('Четверный запрос: ', time4)

    """ Получение списка сотрудников предприятия """
    my_time = time.time()
    curs.execute("SELECT ID_STAFF, LAST_NAME, FIRST_NAME, MIDDLE_NAME, TABEL_ID FROM STAFF WHERE DELETED = 0 "
                 "ORDER BY ID_STAFF")
    full_name_list = curs.fetchall()
    full_name_dict = {}

    time5 = time.time() - my_time
    print('Пятый запрос: ', time5)

    """ Получение списка соответствий профессий отделам"""
    curs.execute("SELECT STAFF_ID, SUBDIV_ID, APPOINT_ID FROM STAFF_REF ORDER BY ID_STAFF_REF ")
    staff_list = curs.fetchall()
    staff_dict = {}
    for i in staff_list:
        staff_dict[i[0]] = [i[1], i[2]]

    """ Формирование строки сотрудника """
    for i in full_name_list:
        string = str(i[1]) + ' ' + str(i[2]) + ' ' + str(i[3])
        full_name_dict[i[0]] = [string, i[4].lstrip()]

    for key, value in staff_dict.items():
        try:
            full_dict[key] = [full_name_dict[key][0], full_name_dict[key][1],
                              subdiv_dict[value[0]], appoint_dict[value[1]]]
        except KeyError:
            full_dict[key] = ['Нет данных', subdiv_dict[value[0]], appoint_dict[value[1]]]

    # for key, value in full_dict.items():
    #     print(key, ' : ', value)

    """ Получения списка событий проходной за выбранный период """
    my_time = time.time()
    curs.execute(
        ("SELECT ID_REG, INNER_NUMBER_EV, DATE_EV, TIME_EV, AREAS_ID, STAFF_ID, USER_ID "
         "FROM REG_EVENTS WHERE REG_EVENTS.DATE_EV >= ? AND REG_EVENTS.DATE_EV <= ? ORDER BY ID_REG"),
        (my_date1, my_date2,))
    main_request_list = curs.fetchall()
    time6 = time.time() - my_time
    print('Шестой запрос: ', time6)
    out_list = []

    for item in main_request_list:
        try:
            # print(item[2], item[3], ' '.join(full_dict[item[5]]), events_dict[item[1]], device_dict[item[4]])
            out_list.append(str(item[2]) + "#" + str(item[3]) + "#" + ' '.join(full_dict[item[5]]) +
                            "#" + events_dict[item[1]] + "#" + device_dict[item[4]])
        except KeyError:
            try:
                # print(item[2], item[3], ' '.join(full_dict[item[5]]), 'Нет данных')
                out_list.append(
                    "{0} {1} {2} Нет данных".format(str(item[2]), str(item[3]), ' '.join(full_dict[item[5]])))
            except KeyError:
                # print(item[2], item[3], "Нет данных", 'Нет данных')
                out_list.append(str(item[2]) + "#" + str(item[3]) + "#" + "Нет данных" + "#" + 'Нет данных')

    con.close()
    print("Общее время выполнения запросов: ", time1 + time2 + time3 + time4 + time5 + time6)
    return out_list


if __name__ == '__main__':
    script_time = time.time()
    first_date = datetime.date(2015, 11, 1)
    second_date = datetime.date.today()
    my_list = my_request(first_date, second_date)
    f = open('test_list.txt', 'w')
    for line in my_list:
        f.write(line + '\n')
    f.close()
    print('Общее ремя выполнение скрипта:', time.time() - script_time)
