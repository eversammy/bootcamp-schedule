"""
App should be able to read the current system time and alert the user if any upcoming Bootcamp is less
than 24 hours from the current system time
"""


def reminder(lock, title):
    from winotify import Notification
    import datetime
    time = ''
    lockTime = lock + '.000000'
    while str(time) < lockTime:
        time = datetime.datetime.now()
    else:
        print('Bootcamp Schedule\n' + title + '\n')
        toaster = Notification(app_id='Windows Notification', title='Bootcamp Schedule', msg=title)
        toaster.show()


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


def findSchedule(zone):    # returns the offset for any inputted timezone
    if zone.lower() in allTimezone():
        return allTimezone().get(zone.lower())
    else:
        for city in allTimezone():
            if '/' in city:
                if zone.lower() == city[city.rindex('/') + 1:]:
                    return allTimezone().get(city)


def bootcampSchedule(zone):    # returns dictionary of bootcamp schedule and notification time for inputted timezone
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
    time_format = '%Y-%m-%d %H:%M:%S'
    time_format_display = '%d-%B-%Y @ %I:%M %p'
    for count in range(len(monthCamp)):
        useTM = str(dt.timedelta(seconds=newTimeCamp[count] + findSchedule(zone)))
        displayDT = dt.datetime(year=int(newDateCamp[count][:4]),
                                month=int(newDateCamp[count][5:7]),
                                day=int(newDateCamp[count][8:10]),
                                hour=int(useTM[:useTM.index(':')]),
                                minute=int(useTM[useTM.index(':') + 1:useTM.rindex(':')]),
                                second=int(useTM[useTM.rindex(':') + 1:]))
        displayDTNotify = displayDT.replace(hour=int(useTM[:useTM.index(':')]) - 1)   # Notification = 1 hour < EST
        dictionary[count] = monthCamp[count], displayDTNotify.strftime(time_format), cohort[count], program[count],\
            topic[count], displayDT.strftime(time_format_display)
    return dictionary


def notify():  # returns notifications for inputted timezone
    try:
        zone = input('Enter Timezone or City for Upcoming Notifications: ')
        btCamp = bootcampSchedule(zone)
        for i in btCamp:
            msg = f'Cohort :  {btCamp.get(i)[2]} - Class Begins In An Hour\nProgram :  {btCamp.get(i)[3]}' \
                  f'\nTopic :  {btCamp.get(i)[4]}\nDate & Time :  {btCamp.get(i)[5]}'
            reminder(btCamp.get(i)[1], msg)
    except TypeError:
        print('Timezone or city unavailable')


notify()
