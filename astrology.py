# -*- coding: utf-8 -*-

from utils import get_sun_hours, get_month_days_number, get_location_datas, get_month_name, get_moon_stage
from datetime import datetime, timedelta, date
import calendar
from exportpdf import exportDatas, ExportHours


class Astrology:
    """Classe définissant l'astrologie caractérisée par :
    - location
    - latitude
    - longitude
    - address
    - date
    - day
    - week
    - month
    - year"""

    def __init__(self):  # Notre méthode constructeur
        """Pour l'instant, on ne va définir qu'un seul attribut"""
        self.location = ""
        self.latitude = 0
        self.longitude = 0
        self.address = ""
        self.date = datetime.today()
        self.day = datetime.today()
        self.week = datetime.today().isocalendar()[1]
        self.month = datetime.today().month
        self.year = datetime.today().year
        self.type_extraction = "day"
        self.colorStyle = None
        self.exportHours = ExportHours()

    def get_hour_series(self, day_number, hour_start, hours, minutes, seconds, i_start, i_end):
        day_name = ["Lundi", "Mardi", "Mercredi",
                    "Jeudi", "Vendredi", "Samedi", "Dimanche"]
        star_tab = {
            "Lundi": {
                '1': 'Lune',
                '2': 'Saturne',
                '3': 'Jupiter',
                '4': 'Mars',
                '5': 'Soleil',
                '6': 'Venus',
                '7': 'Mercure',
            },
            "Mardi": {
                '1': 'Mars',
                '2': 'Soleil',
                '3': 'Venus',
                '4': 'Mercure',
                '5': 'Lune',
                '6': 'Saturne',
                '7': 'Jupiter',
            },
            "Mercredi": {
                '1': 'Mercure',
                '2': 'Lune',
                '3': 'Saturne',
                '4': 'Jupiter',
                '5': 'Mars',
                '6': 'Soleil',
                '7': 'Venus',
            },
            "Jeudi": {
                '1': 'Jupiter',
                '2': 'Mars',
                '3': 'Soleil',
                '4': 'Venus',
                '5': 'Mercure',
                '6': 'Lune',
                '7': 'Saturne',
            },
            "Vendredi": {
                '1': 'Venus',
                '2': 'Mercure',
                '3': 'Lune',
                '4': 'Saturne',
                '5': 'Jupiter',
                '6': 'Mars',
                '7': 'Soleil',
            },
            "Samedi": {
                '1': 'Saturne',
                '2': 'Jupiter',
                '3': 'Mars',
                '4': 'Soleil',
                '5': 'Venus',
                '6': 'Mercure',
                '7': 'Lune',
            },
            "Dimanche": {
                '1': 'Soleil',
                '2': 'Venus',
                '3': 'Mercure',
                '4': 'Lune',
                '5': 'Saturne',
                '6': 'Jupiter',
                '7': 'Mars',
            },
        }
        output_list = []

        day = day_name[day_number]
        planet_order = star_tab[str(day)]
        day_planet = planet_order['1']

        for i in range(i_start, i_end):
            hour_end = hour_start + timedelta(hours=hours,
                                              minutes=minutes,
                                              seconds=seconds)
            index = i % 7
            planet_name = planet_order[str(index + 1)]
            # print('{} | {} | {} | {} | {}'.format(i,
            #                                       index,
            #                                       planet_name,
            #                                       hour_start.strftime('%H:%M'),
            #                                       hour_end.strftime('%H:%M')
            #                                       ))
            line = {
                'index': str(i + 1),
                'date': self.date,
                'day_name': day,
                'day_planet': day_planet,
                'planet': planet_name,
                'hour_start': hour_start.strftime('%H:%M'),
                'hour_end': hour_end.strftime('%H:%M'),
                # 'address': self.address
            }
            output_list.append(line)
            hour_start = hour_end
        return output_list

    def day_switch(self):
        # print("day_switch")
        output = {}
        self.date = self.day
        result = self.get_magic_hours()

        self.exportHours.hourList = result
        self.exportHours.moonPhase.append(result['moon_stage'])

        # return output

    def week_switch(self):
        # print("week_switch")
        # print(str(self.week))
        output = {}
        hourList = []
        weekList = []
        totalList = []
        moonPhaseDay = []
        moonPhaseTotal = []

        weekCount = 1
        weekList.append(self.week)

        for day_number in range(7):
            current_day = date.fromisocalendar(
                self.year, self.week, day_number + 1)  # (year, week, day of week)
            self.date = current_day
            # print(current_day)
            # print(str(current_day))
            result = self.get_magic_hours()
            hourList.append(result)
            moonPhaseDay.append(result['moon_stage'])

        totalList.append(hourList)
        moonPhaseTotal.append(moonPhaseDay)
        output['hourList'] = totalList
        output['moon_stage'] = moonPhaseTotal

        self.exportHours.hourList = totalList
        self.exportHours.weekCount = weekCount
        self.exportHours.weekStart = self.week
        self.exportHours.weekEnd = self.week
        self.exportHours.weekList = weekList
        self.exportHours.moonPhase = moonPhaseTotal

        return output

    def month_switch(self):
        # print("month_switch")
        output = {}
        # hourList = []
        weekList = []
        totalList = []
        moonPhaseDay = []
        moonPhaseTotal = []
        weekCount = 0

        month_days_number = get_month_days_number(self.month, self.year)

        week_start = date(self.year, self.month, 1).isocalendar()[1]
        week_end = date(self.year, self.month,
                        month_days_number).isocalendar()[1]

        for week_number in range(week_start, week_end + 1):
            weekList.append(week_number)
            weekCount += 1
            self.week = week_number
            result = self.week_switch()
            hourList = result['hourList'][0]
            totalList.append(hourList)
            moonPhaseDay = result['moon_stage'][0]
            moonPhaseTotal.append(moonPhaseDay)

        output['hourList'] = totalList

        self.exportHours.hourList = totalList
        self.exportHours.weekCount = weekCount
        self.exportHours.weekStart = week_start
        self.exportHours.weekEnd = week_end
        self.exportHours.weekList = weekList
        self.exportHours.monthName = get_month_name(self.month - 1)
        self.exportHours.moonPhase = moonPhaseTotal

    def year_switch(self):
        # print("year_switch")
        output = {}
        # hourList = []
        weekList = []
        totalList = []
        weekCount = 0
        moonPhaseDay = []
        moonPhaseTotal = []

        month_days_number = get_month_days_number(self.month, self.year)

        week_start = date(self.year, 1, 1).isocalendar()[1]
        week_end = date(self.year, 12,
                        31).isocalendar()[1]

        for week_number in range(week_start, week_end + 1):
            weekList.append(week_number)
            weekCount += 1
            self.week = week_number
            result = self.week_switch()
            hourList = result['hourList'][0]
            totalList.append(hourList)
            moonPhaseDay = result['moon_stage'][0]
            moonPhaseTotal.append(moonPhaseDay)

        output['hourList'] = totalList

        self.exportHours.hourList = totalList
        self.exportHours.weekCount = weekCount
        self.exportHours.weekStart = week_start
        self.exportHours.weekEnd = week_end
        self.exportHours.weekList = weekList
        self.exportHours.monthName = get_month_name(self.month - 1)

    def export_multi_dates(self):

        location_datas = get_location_datas(self.location)

        errorLocation = location_datas["error"]

        if (not errorLocation):
            self.latitude = location_datas["latitude"]
            self.longitude = location_datas["longitude"]
            self.address = location_datas["address"]

            # print(datas)

            options = {
                "day": self.day_switch,
                "week": self.week_switch,
                "month": self.month_switch,
                "year": self.year_switch
            }
            function_to_execute = options.get(self.type_extraction)

            function_to_execute()

            exportdatas = exportDatas()

            self.exportHours.address = self.address
            self.exportHours.treatmentCase = self.type_extraction
            self.exportHours.week = self.week
            self.exportHours.month = self.month
            self.exportHours.year = self.year

            exportdatas.exportHours = self.exportHours
            exportdatas.colorStyle = self.colorStyle

            exportdatas.make_export()

            return 'Done'
        else:
            print(errorLocation)

    def get_magic_hours(self):
        datas = {"date": self.date,
                 "address": self.address,
                 "latitude": self.latitude,
                 "longitude": self.longitude,
                 }
        sun_hours = get_sun_hours(datas)
        moonStage = get_moon_stage(self.date)
        day_sunrise = sun_hours["sunrise"]
        day_sunset = sun_hours["sunset"]
        diff = day_sunset - day_sunrise
        seconds = diff.seconds / 12
        day_hours = seconds // 3600
        day_minutes = (seconds % 3600) // 60
        day_seconds = seconds % 60

        day_number = day_sunrise.weekday()
        day_list = self.get_hour_series(day_number,
                                        day_sunrise,
                                        day_hours,
                                        day_minutes,
                                        day_seconds,
                                        0,
                                        12
                                        )

        # Calculate magic hours for night
        next_date = self.date + timedelta(hours=24)
        sun_hours = get_sun_hours(datas)
        next_sunrise = sun_hours["sunrise"]
        diff = next_sunrise - day_sunset
        seconds = diff.seconds / 12
        night_hours = seconds // 3600
        night_minutes = (seconds % 3600) // 60
        night_seconds = seconds % 60

        night_list = self.get_hour_series(day_number,
                                          day_sunset,
                                          night_hours,
                                          night_minutes,
                                          night_seconds,
                                          12,
                                          24
                                          )

        # for line in day_list:
        #     print(line)
        # for line in night_list:
        #     print(line)
        output_datas = {"date": self.date,
                        "day_list": day_list,
                        "night_list": night_list,
                        "moon_stage": moonStage
                        }
        return output_datas
