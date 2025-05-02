import datetime
from datetime import timezone
import requests

timenowtz = datetime.datetime.now(timezone.utc)
timenow = timenowtz.replace(tzinfo=None)

thedate = timenow.date().strftime('%Y-%m-%d')

daybefore = timenow - datetime.timedelta(days=1)
datebefore = daybefore.date().strftime('%Y-%m-%d')
daybefore2 = timenow - datetime.timedelta(days=2)
datebefore2 = daybefore.date().strftime('%Y-%m-%d')

dayafter = timenow + datetime.timedelta(days=1)
dateafter = dayafter.date().strftime('%Y-%m-%d')
dayafter2 = timenow + datetime.timedelta(days=2)
dateafter2 = dayafter.date().strftime('%Y-%m-%d')



# Powered by the Digital Atlas of the Roman Empire: https://imperium.ahlfeldt.se/
def make_coord_request(place_id):
    url = f"http://imperium.ahlfeldt.se/api/geojson.php?id={place_id}"
    r = requests.get(url)

    response = r.json()
    lat = response['features'][0]['geometry']['coordinates'][1]
    lng = response['features'][0]['geometry']['coordinates'][0]
    return [lat, lng]

# Powered by SunriseSunset.io: https://sunrisesunset.io/api/
def make_sun_request(lat, lng):
    url = f"https://api.sunrisesunset.io/json?lat={lat}&lng={lng}&timezone=UTC&date={thedate}&time_format=24"
    r = requests.get(url)
    response = r.json()
    sunrise = response['results']['sunrise']
    sunset = response['results']['sunset']

    url2 = f"https://api.sunrisesunset.io/json?lat={lat}&lng={lng}&timezone=UTC&date={datebefore}&time_format=24"
    r2 = requests.get(url2)
    response2 = r2.json()
    daystart = response2['results']['sunrise']
    nightstart = response2['results']['sunset']

    url3 = f"https://api.sunrisesunset.io/json?lat={lat}&lng={lng}&timezone=UTC&date={dateafter}&time_format=24"
    r3 = requests.get(url3)
    response3 = r3.json()
    nightend = response3['results']['sunrise']
    dayend = response3['results']['sunset']

    return [daystart, nightstart, sunrise, sunset, nightend, dayend]

def convert_sun_to_datetime(daystart, nightstart, sunrise, sunset, nightend, dayend, lng):
    splitrise = sunrise.split(':')
    hrise = splitrise[0]
    hrisefl = float(hrise)
    splitset = sunset.split(':')
    hset = splitset[0]
    hsetfl = float(hset)
    lngfl = float(lng)

    if hrisefl < hsetfl:
        firsttime = datetime.datetime.strptime(f"{datebefore}, {daystart}", "%Y-%m-%d, %H:%M:%S")
        secondtime = datetime.datetime.strptime(f"{datebefore}, {nightstart}", "%Y-%m-%d, %H:%M:%S")
        risetime = datetime.datetime.strptime(f"{thedate}, {sunrise}", "%Y-%m-%d, %H:%M:%S")
        settime = datetime.datetime.strptime(f"{thedate}, {sunset}", "%Y-%m-%d, %H:%M:%S")
        penulttime = datetime.datetime.strptime(f"{dateafter}, {nightend}", "%Y-%m-%d, %H:%M:%S")
        lasttime = datetime.datetime.strptime(f"{dateafter}, {dayend}", "%Y-%m-%d, %H:%M:%S")
    
    if hrisefl > hsetfl:
        if lngfl>0:
            firsttime = datetime.datetime.strptime(f"{datebefore2}, {daystart}", "%Y-%m-%d, %H:%M:%S")
            secondtime = datetime.datetime.strptime(f"{datebefore}, {nightstart}", "%Y-%m-%d, %H:%M:%S")
            risetime = datetime.datetime.strptime(f"{datebefore}, {sunrise}", "%Y-%m-%d, %H:%M:%S")
            settime = datetime.datetime.strptime(f"{thedate}, {sunset}", "%Y-%m-%d, %H:%M:%S")
            penulttime = datetime.datetime.strptime(f"{thedate}, {nightend}", "%Y-%m-%d, %H:%M:%S")
            lasttime = datetime.datetime.strptime(f"{dateafter}, {dayend}", "%Y-%m-%d, %H:%M:%S")
        if lngfl<0:
            firsttime = datetime.datetime.strptime(f"{datebefore}, {daystart}", "%Y-%m-%d, %H:%M:%S")
            secondtime = datetime.datetime.strptime(f"{thedate}, {nightstart}", "%Y-%m-%d, %H:%M:%S")
            risetime = datetime.datetime.strptime(f"{thedate}, {sunrise}", "%Y-%m-%d, %H:%M:%S")
            settime = datetime.datetime.strptime(f"{dateafter}, {sunset}", "%Y-%m-%d, %H:%M:%S")
            penulttime = datetime.datetime.strptime(f"{dateafter}, {nightend}", "%Y-%m-%d, %H:%M:%S")
            lasttime = datetime.datetime.strptime(f"{dateafter2}, {dayend}", "%Y-%m-%d, %H:%M:%S")
    return [firsttime, secondtime, risetime, settime, penulttime, lasttime]

def get_datetimes_from_coord(lat, lng):
    srss = make_sun_request(lat, lng)
    daystart = srss[0]
    nightstart = srss[1]
    sunrise = srss[2]
    sunset = srss[3]
    nightend = srss[4]
    dayend = srss[5]
    datetimes = convert_sun_to_datetime(daystart, nightstart, sunrise, sunset, nightend, dayend, lng)
    return datetimes

def calc_dies_hodie(risetime, settime):
    dies = settime-risetime
    hora = dies/12
    hora_prima = risetime
    hora_secunda = hora_prima+hora
    hora_tertia = hora_prima+hora*2
    hora_quarta = hora_prima+hora*3
    hora_quinta = hora_prima+hora*4
    hora_sexta = hora_prima+hora*5
    hora_septima = hora_prima+hora*6
    hora_octava = hora_prima+hora*7
    hora_nona = hora_prima+hora*8
    hora_decima = hora_prima+hora*9
    hora_undecima = hora_prima+hora*10
    hora_duodecima = hora_prima+hora*11
    if hora_prima <= timenow < hora_secunda:
        tempus = "\nI\nprima diei hora"
    elif hora_secunda <= timenow < hora_tertia:
        tempus = "\nII\nseconda diei hora"
    elif hora_tertia <= timenow < hora_quarta:
        tempus = "\nIII\ntertia diei hora"
    elif hora_quarta <= timenow < hora_quinta:
        tempus = "\nIV\nquarta diei hora"
    elif hora_quinta <= timenow < hora_sexta:
        tempus = "\nV\nquinta diei hora"
    elif hora_sexta <= timenow < hora_septima:
        tempus = "\nVI\nsexta diei hora"
    elif hora_septima <= timenow < hora_octava:
        tempus = "\nVII\nseptima diei hora"
    elif hora_octava <= timenow < hora_nona:
        tempus = "\nVIII\noctava diei hora"
    elif hora_nona <= timenow < hora_decima:
        tempus = "\nIX\nnona diei hora"
    elif hora_decima <= timenow < hora_undecima:
        tempus = "\nX\ndecima diei hora"
    elif hora_undecima <= timenow < hora_duodecima:
        tempus = "\nXI\nundecima diei hora"
    elif hora_duodecima <= timenow < settime:
        tempus = "\nXII\nduodecima diei hora"
    else:
        tempus = "Eheu! Couldn't find the hour of the day!"
    return tempus

def calc_dies_heri(firsttime, secondtime):
    dies = secondtime-firsttime
    hora = dies/12
    hora_prima = firsttime
    hora_secunda = hora_prima+hora
    hora_tertia = hora_prima+hora*2
    hora_quarta = hora_prima+hora*3
    hora_quinta = hora_prima+hora*4
    hora_sexta = hora_prima+hora*5
    hora_septima = hora_prima+hora*6
    hora_octava = hora_prima+hora*7
    hora_nona = hora_prima+hora*8
    hora_decima = hora_prima+hora*9
    hora_undecima = hora_prima+hora*10
    hora_duodecima = hora_prima+hora*11
    if hora_prima <= timenow < hora_secunda:
        tempus = "\nI\nprima diei hora"
    elif hora_secunda <= timenow < hora_tertia:
        tempus = "\nII\nseconda diei hora"
    elif hora_tertia <= timenow < hora_quarta:
        tempus = "\nIII\ntertia diei hora"
    elif hora_quarta <= timenow < hora_quinta:
        tempus = "\nIV\nquarta diei hora"
    elif hora_quinta <= timenow < hora_sexta:
        tempus = "\nV\nquinta diei hora"
    elif hora_sexta <= timenow < hora_septima:
        tempus = "\nVI\nsexta diei hora"
    elif hora_septima <= timenow < hora_octava:
        tempus = "\nVII\nseptima diei hora"
    elif hora_octava <= timenow < hora_nona:
        tempus = "\nVIII\noctava diei hora"
    elif hora_nona <= timenow < hora_decima:
        tempus = "\nIX\nnona diei hora"
    elif hora_decima <= timenow < hora_undecima:
        tempus = "\nX\ndecima diei hora"
    elif hora_undecima <= timenow < hora_duodecima:
        tempus = "\nXI\nundecima diei hora"
    elif hora_duodecima <= timenow < secondtime:
        tempus = "\nXII\nduodecima diei hora"
    else:
        tempus = "Eheu! Couldn't find the hour of the day!"
    return tempus

def calc_dies_cras(penulttime, lasttime):
    dies = lasttime-penulttime
    hora = dies/12
    hora_prima = penulttime
    hora_secunda = hora_prima+hora
    hora_tertia = hora_prima+hora*2
    hora_quarta = hora_prima+hora*3
    hora_quinta = hora_prima+hora*4
    hora_sexta = hora_prima+hora*5
    hora_septima = hora_prima+hora*6
    hora_octava = hora_prima+hora*7
    hora_nona = hora_prima+hora*8
    hora_decima = hora_prima+hora*9
    hora_undecima = hora_prima+hora*10
    hora_duodecima = hora_prima+hora*11
    if hora_prima <= timenow < hora_secunda:
        tempus = "\nI\nprima diei hora"
    elif hora_secunda <= timenow < hora_tertia:
        tempus = "\nII\nseconda diei hora"
    elif hora_tertia <= timenow < hora_quarta:
        tempus = "\nIII\ntertia diei hora"
    elif hora_quarta <= timenow < hora_quinta:
        tempus = "\nIV\nquarta diei hora"
    elif hora_quinta <= timenow < hora_sexta:
        tempus = "\nV\nquinta diei hora"
    elif hora_sexta <= timenow < hora_septima:
        tempus = "\nVI\nsexta diei hora"
    elif hora_septima <= timenow < hora_octava:
        tempus = "\nVII\nseptima diei hora"
    elif hora_octava <= timenow < hora_nona:
        tempus = "\nVIII\noctava diei hora"
    elif hora_nona <= timenow < hora_decima:
        tempus = "\nIX\nnona diei hora"
    elif hora_decima <= timenow < hora_undecima:
        tempus = "\nX\ndecima diei hora"
    elif hora_undecima <= timenow < hora_duodecima:
        tempus = "\nXI\nundecima diei hora"
    elif hora_duodecima <= timenow < lasttime:
        tempus = "\nXII\nduodecima diei hora"
    else:
        tempus = "Eheu! Couldn't find the hour of the day!"
    return tempus

# quid proxima, quid superiore nocte egeris (Cic. Cat. 1.1.1)
def calc_nox_proxima(startime, risetime):
    nox = risetime - startime
    hora = nox/12
    hora_prima = startime
    hora_secunda = hora_prima+hora
    hora_tertia = hora_prima+hora*2
    hora_quarta = hora_prima+hora*3
    hora_quinta = hora_prima+hora*4
    hora_sexta = hora_prima+hora*5
    hora_septima = hora_prima+hora*6
    hora_octava = hora_prima+hora*7
    hora_nona = hora_prima+hora*8
    hora_decima = hora_prima+hora*9
    hora_undecima = hora_prima+hora*10
    hora_duodecima = hora_prima+hora*11
    if hora_prima <= timenow < hora_quarta:
        watch = "\nVIGILIA PRIMA\n"
        if hora_prima <= timenow < hora_secunda:
            tempus = watch + "I\nprima noctis hora"
        elif hora_secunda <= timenow < hora_tertia:
            tempus = watch + "II\nseconda noctis hora"
        elif hora_tertia <= timenow < hora_quarta:
            tempus = watch + "III\ntertia noctis hora"
    elif hora_quarta <= timenow < hora_septima:
        watch = "\nVIGILIA SECUNDA\n"
        if hora_quarta <= timenow < hora_quinta:
            tempus = watch + "IV\nquarta noctis hora"
        elif hora_quinta <= timenow < hora_sexta:
            tempus = watch + "V\nquinta noctis hora"
        elif hora_sexta <= timenow < hora_septima:
            tempus = watch + "VI\nsexta noctis hora"
    elif hora_septima <= timenow < hora_decima:
        watch = "\nVIGILIA TERTIA\n"
        if hora_septima <= timenow < hora_octava:
            tempus = watch + "VII\nseptima noctis hora"
        elif hora_octava <= timenow < hora_nona:
            tempus = watch + "VIII\noctava noctis hora"
        elif hora_nona <= timenow < hora_decima:
            tempus = watch + "IX\nnona noctis hora"
    elif hora_decima <= timenow < risetime:
        watch = "\nVIGILIA QUARTA\n"
        if hora_decima <= timenow < hora_undecima:
            tempus = watch + "X\ndecima noctis hora"
        elif hora_undecima <= timenow < hora_duodecima:
            tempus = watch + "XI\nundecima noctis hora"
        elif hora_duodecima <= timenow < risetime:
            tempus = watch + "XII\nduodecima noctis hora"
    else:
        tempus = "Eheu! Couldn't find the hour of the last night!"
    return tempus

def calc_nox_superior(settime, penulttime):
    nox = penulttime - settime
    hora = nox/12
    hora_prima = settime
    hora_secunda = hora_prima+hora
    hora_tertia = hora_prima+hora*2
    hora_quarta = hora_prima+hora*3
    hora_quinta = hora_prima+hora*4
    hora_sexta = hora_prima+hora*5
    hora_septima = hora_prima+hora*6
    hora_octava = hora_prima+hora*7
    hora_nona = hora_prima+hora*8
    hora_decima = hora_prima+hora*9
    hora_undecima = hora_prima+hora*10
    hora_duodecima = hora_prima+hora*11
    if hora_prima <= timenow < hora_quarta:
        watch = "\n  VIGILIA PRIMA\n"
        if hora_prima <= timenow < hora_secunda:
            tempus = watch + "        I\nprima noctis hora"
        elif hora_secunda <= timenow < hora_tertia:
            tempus = watch + "II\nseconda noctis hora"
        elif hora_tertia <= timenow < hora_quarta:
            tempus = watch + "III\ntertia noctis hora"
    elif hora_quarta <= timenow < hora_septima:
        watch = "\nVIGILIA SECUNDA\n"
        if hora_quarta <= timenow < hora_quinta:
            tempus = watch + "IV\nquarta noctis hora"
        elif hora_quinta <= timenow < hora_sexta:
            tempus = watch + "V\nquinta noctis hora"
        elif hora_sexta <= timenow < hora_septima:
            tempus = watch + "VI\nsexta noctis hora"
    elif hora_septima <= timenow < hora_decima:
        watch = "\nVIGILIA TERTIA\n"
        if hora_septima <= timenow < hora_octava:
            tempus = watch + "VII\nseptima noctis hora"
        elif hora_octava <= timenow < hora_nona:
            tempus = watch + "VIII\noctava noctis hora"
        elif hora_nona <= timenow < hora_decima:
            tempus = watch + "IX\nnona noctis hora"
    elif hora_decima <= timenow < settime:
        watch = "\nVIGILIA QUARTA\n"
        if hora_decima <= timenow < hora_undecima:
            tempus = watch + "X\ndecima noctis hora"
        elif hora_undecima <= timenow < hora_duodecima:
            tempus = watch + "XI\nundecima noctis hora"
        elif hora_duodecima <= timenow < settime:
            tempus = watch + "XII\nduodecima noctis hora"
    else:
        tempus = "Eheu! Couldn't find the hour of the next night!"
    return tempus 

def get_tempus_from_coord(lat, lng):
    datetimes = get_datetimes_from_coord(lat, lng)
    firsttime = datetimes[0]
    secondtime = datetimes[1]
    risetime = datetimes[2]
    settime = datetimes[3]
    penulttime = datetimes[4]
    lasttime = datetimes[5]
    if firsttime <= timenow < secondtime:
        dies_heri = calc_dies_heri(firsttime, secondtime)
        return dies_heri
    elif secondtime <= timenow < risetime:
        nox_proxima = calc_nox_proxima(secondtime, risetime)
        return nox_proxima
    elif risetime <= timenow < settime:
        dies = calc_dies_hodie(risetime, settime)
        return dies
    elif settime <= timenow < penulttime:
        nox_superior = calc_nox_superior(settime, penulttime)
        return nox_superior
    elif penulttime <= timenow < lasttime:
        dies_cras = calc_dies_cras(penulttime, lasttime)
        return dies_cras
    else:
        return "Eheu! Couldn't get the time from the sun"



def modify_date(firsttime, secondtime, risetime, settime, penulttime, lasttime):
    if secondtime <= timenow < risetime:
        nox_proxima = risetime - secondtime
        dimidium = nox_proxima/2
        media_nox = secondtime + dimidium
        if secondtime <= timenow < media_nox:
            mod_date = datebefore
        else:
            mod_date = thedate
    elif settime <= timenow < penulttime:
        nox_superior = penulttime - settime
        dimidium = nox_superior/2
        media_nox = settime + dimidium
        if media_nox <= timenow < penulttime:
            mod_date = dateafter
        else:
            mod_date = thedate
    elif risetime <= timenow < settime:
        mod_date = thedate
    elif firsttime <= timenow < secondtime:
        mod_date = datebefore
    elif penulttime <= timenow < lasttime:
        mod_date = dateafter
    else:
        mod_date = "Eheu! Couldn't figure out if it's past midnight!"
    return mod_date


def split_date(mod_date):
    splitdate = mod_date.split("-")
    yearstr = splitdate[0]
    year = int(yearstr)
    monthstr = splitdate[1]
    month = int(monthstr)
    daystr = splitdate[2]
    day = int(daystr)
    return [year, month, day]

menses = {
    'Ianuarius': {
        'name': 'Ianuarius',
        'abbr.':'Ian.',
        'nom.fem.pl.': 'Ianuariae',
        'acc.fem.pl.': 'Ianuarias',
        'abl.pl.': 'Ianuariis',
        'days': 31, 
        'kalendae': 1, 
        'nonae': 5, 
        'idus': 13
        },
    'Februarius': {
        'name': 'Februarius', 
        'abbr.':'Feb.',
        'nom.fem.pl.': 'Februariae',
        'acc.fem.pl.': 'Februarias',
        'abl.pl.': 'Februariis',
        'days': 28, 
        'kalendae': 1, 
        'nonae': 5, 
        'idus': 13
        },
    'Februarius (leap year)': {
        'name': 'Februarius', 
        'abbr.':'Feb.',
        'nom.fem.pl.': 'Februariae',
        'acc.fem.pl.': 'Februarias',
        'abl. pl.': 'Februariis',
        'days': 29, 
        'kalendae': 1, 
        'nonae': 5, 
        'idus': 13
        },
    'Martius': {
        'name': 'Martius', 
        'abbr.':'Mar.',
        'nom.fem.pl.': 'Martiae',
        'acc.fem.pl.': 'Martias',
        'abl.pl.': 'Martiis',
        'days': 31, 
        'kalendae': 1, 
        'nonae': 7, 
        'idus': 15
        },
    'Aprilis': {
        'name': 'Aprilis', 
        'abbr.':'Apr.',
        'nom.fem.pl.': 'Apriles',
        'acc.fem.pl.': 'Apriles',
        'abl.pl.': 'Aprilibus',
        'days': 30, 
        'kalendae': 1, 
        'nonae': 5, 
        'idus': 13
        },
    'Maius': {
        'name': 'Maius', 
        'abbr.':'Mai.',
        'nom.fem.pl.': 'Maiae',
        'acc.fem.pl.': 'Maias',
        'abl.pl.': 'Maiis',
        'days': 31, 
        'kalendae': 1, 
        'nonae': 7, 
        'idus': 15
        },
    'Iunius': {
        'name': 'Iunius',
        'abbr.':'Iun.',
        'nom.fem.pl.': 'Iuniae',
        'acc.fem.pl.': 'Iunias', 
        'abl.pl.': 'Iuniis',
        'days': 30, 
        'kalendae': 1, 
        'nonae': 5, 
        'idus': 13
        },
    'Iulius': {
        'name': 'Iulius', 
        'abbr.':'Iul.',
        'nom.fem.pl.': 'Iuliae',
        'acc.fem.pl.': 'Iulias',
        'abl.pl.': 'Iuliis',
        'days': 31, 
        'kalendae': 1, 
        'nonae': 7, 
        'idus': 15
        },
    'Augustus': {
        'name': 'Augustus',
        'abbr.':'Aug.',
        'nom.fem.pl.': 'Augustae',
        'acc.fem.pl.': 'Augustas',
        'abl.pl.': 'Augustis', 
        'days': 31, 
        'kalendae': 1, 
        'nonae': 5, 
        'idus': 13
        },
    'September': {
        'name': 'September',
        'abbr.':'Sept.',
        'nom.fem.pl.': 'Septembres',
        'acc.fem.pl.': 'Septembres',
        'abl.pl.': 'Septembribus', 
        'days': 30, 
        'kalendae': 1, 
        'nonae': 5, 
        'idus': 13
        },
    'October': {
        'name': 'October',
        'abbr.':'Oct.',
        'nom.fem.pl.': 'Octobres',
        'acc.fem.pl.': 'Octobres',
        'abl.pl.': 'Octobribus', 
        'days': 31, 
        'kalendae': 1, 
        'nonae': 7, 
        'idus': 15
        },
    'November': {
        'name': 'November',
        'abbr.':'Nov.',
        'nom.fem.pl.': 'Novembres',
        'acc.fem.pl.': 'Novembres', 
        'abl.pl.': 'Novembribus',
        'days': 30, 
        'kalendae': 1, 
        'nonae': 5, 
        'idus': 13
        },
    'December': {
        'name': 'December', 
        'abbr.':'Dec.',
        'nom.fem.pl.': 'Decembres',
        'acc.fem.pl.': 'Decembres',
        'abl.pl.': 'Decembribus',
        'days': 31, 
        'kalendae': 1, 
        'nonae': 5, 
        'idus': 13}
        }

#Solution found here: https://stackoverflow.com/questions/28777219/basic-program-to-convert-integer-to-roman-numerals
num_map = [(1000, 'M'), (900, 'CM'), (500, 'D'), (400, 'CD'), (100, 'C'), (90, 'XC'),
           (50, 'L'), (40, 'XL'), (10, 'X'), (9, 'IX'), (5, 'V'), (4, 'IV'), (1, 'I')]

def num2roman(num):
    roman = ''
    while num > 0:
        for i, r in num_map:
            while num >= i:
                roman += r
                num -= i

    return roman


ordinals = {1:'primum', 2:'secundum', 3:'tertium', 4:'quartum', 5:'quintum', 6:'sextum', 
            7:'septimum', 8:'octavum', 9:'nonum', 10:'decimum', 11:'undecimum', 12:'duodecimum', 
            13:'tertium decimum', 14:'quartum decimum', 15:'quintum decimum', 16:'sextum decimum', 
            17:'septimum decimum', 18:'duodevicesimum', 19:'undevicesimum'
}



def get_mensis_from_month(month, year):
    if month == 1:
        mensis = menses['Ianuarius']
    if month == 2:
        if year % 400 == 0:
            mensis = menses['Februarius (leap year)']
        elif year % 4 == 0 and year % 100 != 0:
            mensis = menses['Februarius (leap year)']
        else: 
            mensis = menses['Februarius']
    if month == 3:
        mensis = menses['Martius']
    if month == 4:
        mensis = menses['Aprilis']
    if month == 5:
        mensis = menses['Maius']
    if month == 6:
        mensis = menses['Iunius']
    if month == 7:
        mensis = menses ['Iulius']
    if month == 8:
        mensis = menses['Augustus']
    if month == 9:
        mensis = menses['September']
    if month == 10:
        mensis = menses['October']
    if month == 11:
        mensis = menses['November']
    if month == 12:
        mensis = menses['December']
    return mensis

def get_mensis_prox(month, year):
    next_month = month+1
    mensis_prox = get_mensis_from_month(next_month, year)
    return mensis_prox

def get_datus(day, mensis, mensis_prox):
    if day == mensis['kalendae']:
        datus = f"\nKal. {mensis['abbr.']}\n(Kalendis {mensis['abl.pl.']})"
    elif day == mensis['nonae']:
        datus = f"\nNon. {mensis['abbr.']}\n(Nonis {mensis['abl.pl.']})"
    elif day == mensis['idus']:
        datus = f"\nEid. {mensis['abbr.']}\n(Idibus {mensis['abl.pl.']})"
    elif day == mensis['nonae']-1:
        datus = f"\nprid. Non. {mensis['abbr.']}\n(pridie Nonas {mensis['acc.fem.pl.']})"
    elif day == mensis['idus']-1:
        datus = f"\nprid. Non. {mensis['abbr.']}\n(pridie Idus {mensis['acc.fem.pl.']})"
    elif day == mensis['days']:
        datus = f"\nprid. Kal. {mensis_prox['abbr.']}\n(pridie Kalendas {mensis_prox['acc.fem.pl.']})"
    elif mensis == menses['Februarius (leap year)']:
        if day == 25:
            datus = "\na.d. VI Kal. Mar.\n(ante diem bis sextum Kalendas Martias)"
        elif mensis['idus'] < day < 25:
            number = mensis['days']-day+1
            numeral = num2roman(number)
            ordinal = ordinals[number]
            datus = f"\na.d. {numeral} Kal. Mar.\n(ante diem {ordinal} Kalendas Martias)"
        elif day > 25:
            number = mensis['days']-day+2
            numeral = num2roman(number)
            ordinal = ordinals[number]
            datus = f"\na.d. {numeral} Kal. Mar.\n(ante diem {ordinal} Kalendas Martias)"
    elif mensis['kalendae'] < day < mensis['nonae']-1:
        number = mensis['nonae']-day+1
        numeral = num2roman(number)
        ordinal = ordinals[number]
        datus = f"\na.d. {numeral} Non. {mensis['abbr.']}\n(ante diem {ordinal} Nonas {mensis['acc.fem.pl.']})"
    elif mensis['nonae'] < day < mensis['idus']:
        number = mensis['idus']-day+1
        numeral = num2roman(number)
        ordinal = ordinals[number]
        datus = f"\na.d. {numeral} Eid. {mensis['abbr.']}\n(ante diem {ordinal} Idus {mensis['acc.fem.pl.']})"
    elif day > mensis['idus']:
        number = mensis['days']-day+2
        numeral = num2roman(number)
        ordinal = ordinals[number]
        datus = f"\na.d. {numeral} Kal. {mensis_prox['abbr.']}\n(ante diem {ordinal} Kalendas {mensis_prox['acc.fem.pl.']})"

    return datus



def horologium_universalis(lat, lng):
    tempus = get_tempus_from_coord(lat, lng)
    datetimes = get_datetimes_from_coord(lat, lng)
    firsttime = datetimes[0]
    secondtime = datetimes[1]
    risetime = datetimes[2]
    settime = datetimes[3]
    penulttime = datetimes[4]
    lasttime = datetimes[5]
    mod_date = modify_date(firsttime, secondtime, risetime, settime, penulttime, lasttime)
    ymd = split_date(mod_date)
    year = ymd[0]
    month = ymd[1]
    day = ymd[2]
    mensis = get_mensis_from_month(month, year)
    mensis_prox = get_mensis_prox(month, year)
    datus = get_datus(day, mensis, mensis_prox)
    datus_et_tempus = f"{datus}\n{tempus}\n"
    return datus_et_tempus


def horologium_romanum(place_id):
    coords = make_coord_request(place_id)
    lat = coords[0]
    lng = coords[1]
    datus_et_tempus = horologium_universalis(lat, lng)
    return datus_et_tempus

# Solution found here: https://www.reddit.com/r/learnpython/comments/1c19y94/learning_dynamic_text_box/
def print_in_box(text: str) -> None:
    """Print multi-line text in a box."""
    margin_width = 2
    horizontal_border_char = '='
    vertical_border_char = '|'

    lines = text.split('\n')
    max_line_length = max(len(line) for line in lines)

    max_line_length += 2 * margin_width
    horizontal_border = (
        vertical_border_char +
        horizontal_border_char * max_line_length +
        vertical_border_char
        )

    print(horizontal_border)

    for line in lines:
        # Calculate margin widths.
        left_margin = (max_line_length - len(line)) // 2
        right_margin = max_line_length - (len(line) + left_margin)

        formatted_line = (
            f"{vertical_border_char}"
            f"{' ' * left_margin}{line}{' ' * right_margin}"
            f"{vertical_border_char}"
            )

        print(formatted_line)

    print(horizontal_border)

def horologium():
    while True:
        setting = input("""
Salve! What setting would you like to use? To pick a location from the Digital Atlas of the Roman Empire (https://imperium.ahlfeldt.se/), enter 1. To use any latitude and longitude, enter 2. To quit, enter 0.
        """)

        if setting == '1':
            place_id = input("Please enter the place ID of a location from the Digital Atlas of the Roman Empire:")
            horologium = horologium_romanum(place_id)
            print("\n\n")
            print_in_box(horologium)

            while True: 
                refresh = input("\n\n\n To refresh, press Enter. To select a new location, enter 1.")
                if refresh == '1':
                    break
                else:
                    horologium = horologium_romanum(place_id)
                    print("\n\n")
                    print_in_box(horologium)

        elif setting == '2':
            lat = input("Please enter your latitude, in decimal notation:")
            lng = input("Please enter your longitude, in decimal notation:")
            horologium = horologium_universalis(lat, lng)
            print("\n\n")
            print_in_box(horologium)

            while True: 
                refresh = input("\n\n\n To refresh, press Enter. To select a new location, enter 1.")
                if refresh == '1':
                    break
                else:
                    horologium = horologium_universalis(lat, lng)
                    print("\n\n")
                    print_in_box(horologium)
        elif setting == '0':
            print('Vale!')
            break

horologium()