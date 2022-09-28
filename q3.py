"""
App should be able to provide the equivalent time in any specified target country and display its time zone
"""


def campSchedule():    # returns dictionary of countries, timezones and offset
    import datetime as dt
    import pandas
    fileLocation = "Time zones_404_Counries.xlsx"
    openFile = pandas.read_excel(fileLocation)
    dictionary = {}
    timeZone = list(openFile['Time Zone'])
    offset = list(openFile['GMT Offset'])
    cName = list(openFile['Country Name'])
    offset2 = []
    for i in offset:  # remove blank lines in sheet, ie "UTC "
        if i == 'UTC':
            offset2.append('+00:00')
        else:
            offset2.append(i[4:])
    time_format = '%d-%m-%Y %H:%M:%S'
    offset3 = []
    for o in offset2:  # coverts time format list from file to seconds
        if o[0] == '+':
            p, h = dt.timedelta(hours=int(o[1:3])), dt.timedelta(minutes=int(o[4:6]))
            offset3.append('+' + str(p.seconds + h.seconds))
        elif o[0] == '-':
            p, h = dt.timedelta(hours=int(o[1:3])), dt.timedelta(minutes=int(o[4:6]))
            offset3.append('-' + str(p.seconds + h.seconds))
    for count in range(len(timeZone)):
        dictionary[timeZone[count].lower()] = cName[count].lower(), (dt.datetime.now() + dt.timedelta(
            seconds=int(offset3[count]) + 5 * 3600)).strftime(time_format)   # make EST(-5 hours) timezone system time
    return dictionary


def findSchedule(country, zone):   # returns the bootcamp time for inputted country and timezone
    if zone.lower() in campSchedule() and country.lower() in campSchedule().get(zone.lower())[0]:
        return f'The schedule time for {country.upper()} in {zone.upper()} timezone is ' \
               f'{campSchedule().get(zone.lower())[1]}'
    else:
        return 'Country or Timezone Unavailable'


def schedule4():    # Takes country and timezone
    country = input('Enter Country: ')
    timezone = input('Enter Time Zone: ')
    print(findSchedule(country, timezone))


schedule4()
