"""
a) App should hold information about the times in countries of the world
b) App Should be able to tell the current time in any country specified by the user
# BASED ON FILE - Time zones_404_Countries.xlsx
"""


def campSchedule2():     # returns dictionary for timezone and time offset based on EST time
    import datetime as dt
    import pandas
    fileLocation = 'Time zones_404_Counries.xlsx'
    openFile = pandas.read_excel(fileLocation)
    dictionary1 = {}
    timeZone = list(openFile['Time Zone'])
    offset = list(openFile['GMT Offset'])
    offset2 = []
    for i in offset:    # remove blank lines in the Excel sheet, ie "UTC "
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
            seconds=int(offset3[count]) + 5 * 3600)).strftime(time_format)  # make EST(-5 hours) timezone system time

    return dictionary1


def findSchedule2(zone):    # returns the current time for inputted timezone or city
    if zone.lower() in campSchedule2():
        return campSchedule2().get(zone)
    else:
        for city in campSchedule2():
            if zone.lower() == city[city.rindex('/') + 1:]:
                return campSchedule2().get(city)


def schedule2():    # takes timezone
    timezone = input('Enter Timezone or City: ')
    if findSchedule2(timezone) is None:
        print('Timezone or city unavailable')
    else:
        print(f'Current time at {timezone.upper()} from EST timezone is {findSchedule2(timezone)}')


schedule2()
