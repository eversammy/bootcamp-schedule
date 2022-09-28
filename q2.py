"""
a) App should hold the time zones and times of the 200 time zones provided
b) App should therefore be able to tell the time zone of any country specified by the user
"""


def campSchedule1():   # returns dictionary for timezone name, acronym, and offset based on EST time
    import pandas
    import datetime as dt
    fileLocation = 'timezones_Standard_Times.csv'
    openFile = pandas.read_csv(fileLocation)
    dictionary = {}
    timeZone = list(openFile['Zone'])
    offset = list(openFile['GMT Offset'])
    zoneName = list(openFile['Time Zone Name'])
    offsetTemp = []
    for i in offset:    # change offset sheet values from A±00 to 0
        if i == '±00':
            offsetTemp.append('0')
        else:
            offsetTemp.append(i)
    newOffset = []
    for p in offsetTemp:    # coverts time format in sheet to seconds
        if ':' in p:
            h, m = dt.timedelta(hours=int(p[1:3])), dt.timedelta(minutes=int(p[4:6]))
            newOffset.append(p[0] + str(h.seconds + m.seconds))
        elif p == '#VALUE!':
            newOffset.append('#VALUE!')
        elif '-' in p:
            h = dt.timedelta(hours=int(p.strip('-')))
            newOffset.append('-' + str(h.seconds))
        else:
            h = dt.timedelta(hours=int(p))
            newOffset.append(str(h.seconds))
    time_format = '%d-%m-%Y %H:%M:%S'
    for count in range(len(timeZone)):
        if newOffset[count] == '#VALUE!':
            dictionary[timeZone[count].lower()] = zoneName[count].lower(), '#VALUE!'
        else:
            dictionary[str(timeZone[count]).lower()] = zoneName[count].lower(), (dt.datetime.now() + dt.timedelta(
                seconds=int(newOffset[count]) + 5 * 3600)).strftime(time_format)   # EST(-5 hours) == system time

    return dictionary


def findSchedule1(zone):    # returns the current time for inputted timezone or name or acronym
    if zone.lower() in campSchedule1():
        return campSchedule1().get(zone.lower())[1]
    else:
        for zoneName in campSchedule1():
            if zone.lower() == campSchedule1().get(zoneName)[0]:
                return campSchedule1().get(zoneName)[1]


def schedule1():     # takes timezone name or acronym
    timezone = input('Enter Timezone Name or Acronym: ')
    if findSchedule1(timezone) is None:
        print('Timezone unavailable')
    elif findSchedule1(timezone) == '#VALUE!':
        print('Timezone offset not provided')
    else:
        print(f'Current time at {timezone.upper()} from EST timezone is {findSchedule1(timezone)}')


schedule1()
