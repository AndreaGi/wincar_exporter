from datetime import date


def null_date():
    return b'   '


def convert_year(byte):
    year = 0
    decimal_byte = int(byte, 16)
    match decimal_byte:
        case 101:
            year = 1965
        case 129:
            year = 1981
        case 136:
            year = 1988
        case 137:
            year = 1989
        case 144:
            year = 1990
        case 145:
            year = 1991
        case 146:
            year = 1992
        case 147:
            year = 1993
        case 148:
            year = 1994
        case 149:
            year = 1995
        case 150:
            year = 1996
        case 151:
            year = 1997
        case 152:
            year = 1998
        case 153:
            year = 1999
        case 160:
            year = 2000
        case 161:
            year = 2001
        case 162:
            year = 2002
        case 163:
            year = 2003
        case 164:
            year = 2004
        case 165:
            year = 2005
        case 166:
            year = 2006
        case 167:
            year = 2007
        case 168:
            year = 2008
        case 169:
            year = 2009
        case 176:
            year = 2010
        case 177:
            year = 2011
        case 178:
            year = 2012
        case 179:
            year = 2013
        case 180:
            year = 2014
        case 181:
            year = 2015
        case 182:
            year = 2016
        case 183:
            year = 2017
        case 184:
            year = 2018
        case 185:
            year = 2019
        case 192:
            year = 2020
        case 193:
            year = 2021
        case 194:
            year = 2022
        case 195:
            year = 2023
    return year


def convert_date(byte):
    if byte == null_date() or byte == '':
        return
    year = 0
    # print(byte[0])
    # print(byte[1])
    # print(byte[2])
    match byte[0]:
        case 101:
            year = 1965
        case 129:
            year = 1981
        case 136:
            year = 1988
        case 137:
            year = 1989
        case 144:
            year = 1990
        case 145:
            year = 1991
        case 146:
            year = 1992
        case 147:
            year = 1993
        case 148:
            year = 1994
        case 149:
            year = 1995
        case 150:
            year = 1996
        case 151:
            year = 1997
        case 152:
            year = 1998
        case 153:
            year = 1999
        case 160:
            year = 2000
        case 161:
            year = 2001
        case 162:
            year = 2002
        case 163:
            year = 2003
        case 164:
            year = 2004
        case 165:
            year = 2005
        case 166:
            year = 2006
        case 167:
            year = 2007
        case 168:
            year = 2008
        case 169:
            year = 2009
        case 176:
            year = 2010
        case 177:
            year = 2011
        case 178:
            year = 2012
        case 179:
            year = 2013
        case 180:
            year = 2014
        case 181:
            year = 2015
        case 182:
            year = 2016
        case 183:
            year = 2017
        case 184:
            year = 2018
        case 185:
            year = 2019
        case 192:
            year = 2020
        case 193:
            year = 2021
        case 194:
            year = 2022
        case 195:
            year = 2023
        case 196:
            year = 2024

    month = 0
    match byte[1]:
        case 1:
            month = 1
        case 2:
            month = 2
        case 3:
            month = 3
        case 4:
            month = 4
        case 5:
            month = 5
        case 6:
            month = 6
        case 7:
            month = 7
        case 8:
            month = 8
        case 9:
            month = 9
        case 16:
            month = 10
        case 17:
            month = 11
        case 18:
            month = 12

    day = 0
    match byte[2]:
        case 1:
            day = 1
        case 2:
            day = 2
        case 3:
            day = 3
        case 4:
            day = 4
        case 5:
            day = 5
        case 6:
            day = 6
        case 7:
            day = 7
        case 8:
            day = 8
        case 9:
            day = 9
        case 16:
            day = 19
        case 17:
            day = 11
        case 18:
            day = 12
        case 19:
            day = 13
        case 20:
            day = 14
        case 21:
            day = 15
        case 22:
            day = 16
        case 23:
            day = 17
        case 24:
            day = 18
        case 25:
            day = 19
        case 32:
            day = 20
        case 33:
            day = 21
        case 34:
            day = 22
        case 35:
            day = 23
        case 36:
            day = 24
        case 37:
            day = 25
        case 38:
            day = 26
        case 39:
            day = 27
        case 40:
            day = 28
        case 41:
            day = 29
        case 48:
            day = 30
        case 49:
            day = 31

    if year == 0 or month == 0 or day == 0:
        return
    return date(year, month, day)
