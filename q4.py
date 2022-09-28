"""
App should be able to generate the Bootcamp schedule in the time/timezone of any country specified
"""


def allTimezone():  # returns list of timezones and offset
    import pandas
    fileLocation = 'timezones_Detailed_588_Countries.csv'
    openFile = pandas.read_csv(fileLocation)
    dictionary = {}
    timeZone = list(openFile['timezone'])
    offset = list(openFile['offset'])
    for index in range(len(timeZone)):
        dictionary[str(timeZone[index]).lower()] = offset[index]
    return dictionary


def findSchedule1(zone):    # returns the offset for any inputted timezone
    if zone.lower() in allTimezone():
        return allTimezone().get(zone.lower())
    else:
        for city in allTimezone():
            if '/' in city:
                if zone.lower() == city[city.rindex('/') + 1:]:
                    return allTimezone().get(city)


def bootcampSchedule(zone):   # returns dictionary of bootcamp schedule for inputted timezone
    import pandas
    import datetime as dt
    fileLocation = 'BootcampSchedule.xlsx'
    openFile = pandas.read_excel(fileLocation)
    dictionary = {}
    monthCamp = list(openFile['Month '])
    dateCamp = list(openFile['Date '])
    timeCamp = list(openFile['Bootcamp Time (EST)'])
    cohort = list(openFile['Cohort'])
    program = list(openFile['Program '])
    topic = list(openFile['Topic '])
    newDateCamp = []
    for i in dateCamp:  # coverts date format list from file to timedelta format
        newDateCamp.append(str(i)[:10])
    newTimeCamp = []
    for p in timeCamp:  # coverts time format list from file to seconds
        newTimeCamp.append(dt.timedelta(hours=int(p[:p.index('.')])).seconds
                           + dt.timedelta(minutes=int(p[p.index('.') + 1:p.rindex(' ')])).seconds
                           + 5 * 3600)  # make EST(-5 hours) timezone system time
    time_format_date = '%Y-%m-%d'
    time_format_time = '%H:%M %p'
    for count in range(1, len(monthCamp)):
        useTM = str(dt.timedelta(seconds=newTimeCamp[count] + findSchedule1(zone)))
        displayDT = dt.datetime(year=int(newDateCamp[count][:4]),
                                month=int(newDateCamp[count][5:7]),
                                day=int(newDateCamp[count][8:10]),
                                hour=int(useTM[:useTM.index(':')]),
                                minute=int(useTM[useTM.index(':') + 1:useTM.rindex(':')]),
                                second=int(useTM[useTM.rindex(':')+1:]))
        dictionary[count] = monthCamp[count], displayDT.strftime(time_format_date), \
            displayDT.strftime(time_format_time), cohort[count], program[count], topic[count]
    return dictionary


def dicted():  # Use dicted or Listed to return bootcamp schedule
    try:
        zone = input('Enter Timezone or City to Receive Bootcamp Schedule: ')
        print(bootcampSchedule(zone))
    except TypeError:
        print('Timezone or City Unavailable.')


def listed():   # Use dicted or Listed to return bootcamp schedule
    zone = input('Enter Timezone or City to Receive Bootcamp Schedule: ')
    try:
        for i in bootcampSchedule(zone):
            print(i, bootcampSchedule(zone).get(i))
    except TypeError:
        print('Timezone or City Unavailable.')


listed()
#   dicted()
