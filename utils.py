# -*- coding: utf-8 -*-

import math
# import datetime
from datetime import date, datetime
from geopy.geocoders import Nominatim
from geopy.exc import *
import timezonefinder
import pytz
from astral import LocationInfo, moon
from astral.sun import sun
import os


def deleteFileLine(original_file, line_number):
    """ Delete a line from a file at the given line number """
    is_skipped = False
    dummy_file = original_file + '.bak'
    # Open original file in read only mode and dummy file in write mode
    with open(original_file, 'r') as read_obj, open(dummy_file, 'w') as write_obj:
        # Line by line copy data from original file to dummy file
        for current_index, line in enumerate(read_obj):
            # If current line number matches the given line number then skip copying
            if current_index != line_number:
                write_obj.write(line)
            else:
                is_skipped = True
    # If any line is skipped then rename dummy file as original file
    if is_skipped:
        os.remove(original_file)
        os.rename(dummy_file, original_file)
    else:
        os.remove(dummy_file)


def getMoonPhaseName(moonStage):
    moonDic = {
        1: "Nouvelle Lune",
        2: "Croissant ascendant",
        3: "Premier quartier",
        4: "Lune gibbeuse ascendante",
        5: "Pleine Lune",
        6: "Lune gibbeuse descendante",
        7: "Dernier quartier",
        8: "Croissant descendant",
    }
    return moonDic[moonStage]


def get_year_week_count(inputYear):
    return date(inputYear, 12, 31).isocalendar()[1]


def get_moon_stage(inputDate):
    moonStage = 0

    phase = moon.phase(inputDate)
    rest = phase % 3.5
    intPart = phase // 3.5

    if (rest < 1):
        return int(intPart + 1)
    else:
        return ''


def get_month_days_number(Month_number, year):
    month_tab = {
        1: 31,
        2: 28,
        3: 31,
        4: 30,
        5: 31,
        6: 30,
        7: 31,
        8: 31,
        9: 30,
        10: 31,
        11: 30,
        12: 31
    }

    month_days_number = month_tab[Month_number]

    if (Month_number == 2) and (
        (year % 4 == 0 and year % 100 != 0 or year % 400 == 0)
    ):
        print("L'annee est une annee bissextile!")
        month_days_number += 1

    return month_days_number


def get_month_name(monthNumber):
    monthList = ["Janvier", "Février", "Mars", "Avril", "Mai", "Juin",
                 "Juillet", "Août", "Septembre", "Octobre", "Novembre", "Décembre"]
    return monthList[monthNumber]


def get_litteral_date(inputDate):
    days_list = ["Lundi", "Mardi", "Mercredi",
                 "Jeudi", "Vendredi", "Samedi", "Dimanche"]
    months_list = ["Janvier", "Février", "Mars", "Avril", "Mai", "Juin",
                   "Juillet", "Août", "Septembre", "Octobre", "Novembre", "Décembre"]
    outputDate = ''

    day_number = inputDate.weekday()
    month_number = inputDate.month
    dayName = days_list[day_number]
    dayNumber = str(inputDate.day)
    monthName = get_month_name(month_number - 1)
    year = str(inputDate.year)

    outputDate = '{} {} {} {}'.format(dayName,
                                      dayNumber,
                                      monthName,
                                      year
                                      )

    return outputDate


def get_time_zone(latitude, longitude):
    tf = timezonefinder.TimezoneFinder()
    timezone_str = tf.certain_timezone_at(lat=latitude, lng=longitude)

    if timezone_str is not None:
        # Display the current time in that time zone
        return pytz.timezone(timezone_str)
    print("Could not determine the time zone")
    return "UTC"


def get_location_datas(input_location):
    if (input_location is None):
        return {"address": None,
                "latitude": None,
                "longitude": None,
                "error": "Le lieu n'est pas alimenté"
                }
    else:
        # geolocator = Nominatim(user_agent="Heures_magiques")
        # location = geolocator.geocode(input_location)
        try:
            geolocator = Nominatim(user_agent="Heures_magiques")
            location = geolocator.geocode(input_location)

            if (location is None):
                return {"address": None,
                        "latitude": None,
                        "longitude": None,
                        "error": "Le lieu n'a pas été trouvé"
                        }
            else:
                return {"address": location.address,
                        "latitude": location.latitude,
                        "longitude": location.longitude,
                        "error": None
                        }

        except GeopyError:
            # raise Exception("There was a problem with the geolocator function")
            return {"address": None,
                    "latitude": None,
                    "longitude": None,
                    "error": "Il y a un problème avec la fonction de géolocalisation.\
                    Contrôler la connexion internet"
                    }
        # except GeopyError:
        #     print('GeopyError')
        # except GeocoderServiceError:
        #     print('GeocoderServiceError')
        # except GeocoderQueryError:
        #     print('GeocoderQueryError')
        # except GeocoderTimedOut:
        #     print('GeocoderTimedOut')
        # except GeocoderUnavailable:
        #     print('GeocoderUnavailable')


def get_sun_hours(datas):
    input_date = datas["date"]
    address = datas["address"]
    latitude = datas["latitude"]
    longitude = datas["longitude"]

    # print('latitude:', location.latitude)
    # print('longitude:', location.longitude)
    # print(location.address)

    if isinstance(input_date, str):
        working_date = datetime.datetime.strptime(input_date, '%Y-%m-%d')
    else:
        working_date = input_date
    # geolocator = Nominatim(user_agent="Heures_magiques")
    # location = geolocator.geocode(input_location)
    city = LocationInfo()
    city.name = address
    city.region = 'region'
    city.timezone = get_time_zone(latitude, longitude)
    city.latitude = latitude
    city.longitude = longitude
    # print("timezone :", city.timezone)
    s = sun(city.observer, date=working_date, tzinfo=city.timezone)

    # print((
    #     f'Dawn:    {s["dawn"]}\n'
    #     f'Sunrise: {s["sunrise"]}\n'
    #     f'Noon:    {s["noon"]}\n'
    #     f'Sunset:  {s["sunset"]}\n'
    #     f'Dusk:    {s["dusk"]}\n'
    # ))
    next_rising_hour = s["sunrise"]
    next_setting_hour = s["sunset"]

    # return {"sunrise": next_rising_hour.strftime('%H:%M'),
    #         "sunset": next_setting_hour.strftime('%H:%M')}
    return {"sunrise": next_rising_hour,
            "sunset": next_setting_hour}
