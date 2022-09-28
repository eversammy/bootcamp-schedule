"""
a) App should hold information about the times in countries of the world
b) App Should be able to tell the current time in any country specified by the user
# BASED ON FILES - Time zones_404_Counries.xlsx & timezones_Detailed_588_Countries.csv
"""


def campSchedule1():    # returns dictionary for timezone and time offset based on EST time
    import datetime as dt
    import pandas
    fileLocation = 'Time zones_404_Counries.xlsx'
    openFile = pandas.read_excel(fileLocation)
    dictionary1 = {}
    timeZone = list(openFile['Time Zone'])
    offset = list(openFile['GMT Offset'])
    offset2 = []
    for i in offset:    # remove blank lines in the sheet, ie "UTC "
        if i == 'UTC':
            offset2.append('+00:00')
        else:
            offset2.append(i[4:])
    time_format = '%d-%m-%Y %H:%M:%S'
    offset3 = []
    for o in offset2:    # coverts time format in sheet to seconds
        if o[0] == '+':
            p, h = dt.timedelta(hours=int(o[1:3])), dt.timedelta(minutes=int(o[4:6]))
            offset3.append('+' + str(p.seconds + h.seconds))
        elif o[0] == '-':
            p, h = dt.timedelta(hours=int(o[1:3])), dt.timedelta(minutes=int(o[4:6]))
            offset3.append('-' + str(p.seconds + h.seconds))
    for count in range(len(timeZone)):
        dictionary1[timeZone[count].lower()] = (dt.datetime.now() + dt.timedelta(
            seconds=int(offset3[count]) + 5 * 3600)).strftime(time_format)   # make EST(-5 hours) timezone system time

    return dictionary1


def campSchedule2():    # returns dictionary for timezone and time offset based on EST time
    import pandas
    import datetime
    fileLocation = 'timezones_Detailed_588_Countries.csv'
    openFile = pandas.read_csv(fileLocation)
    dictionary2 = {}
    timeZone = list(openFile['timezone'])
    offset = list(openFile['offset'])
    time_format = '%d-%m-%Y %H:%M:%S'
    for count in range(len(timeZone)):
        dictionary2[timeZone[count].lower()] = (datetime.datetime.now() + datetime.timedelta(
            seconds=(offset[count]) + 5 * 3600)).strftime(time_format)   # make EST(-5 hours) timezone system time
    return dictionary2


def combSch():   # combines both dictionaries
    sch1 = campSchedule1()
    sch2 = campSchedule2()
    for i in sch2:
        sch1.update({i: sch2.get(i)})
    return sch1


def findSchedule(zone):   # returns the current time for inputted timezone or city
    if zone.lower() in combSch():
        return combSch().get(zone)
    else:
        for city in combSch():
            if '/' in city:
                if zone.lower() == city[city.rindex('/') + 1:]:
                    return combSch().get(city)


def schedule():  # takes timezone
    timezone = input('Enter Timezone or City: ')
    if findSchedule(timezone) is None:
        print('Timezone or city unavailable')
    else:
        print(f'Current time at {timezone.upper()} from EST timezone is {findSchedule(timezone)}')


schedule()
