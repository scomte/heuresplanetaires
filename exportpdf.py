# -*- coding: utf-8 -*-

from reportlab.lib import colors
from reportlab.platypus import TableStyle
from reportlab.platypus import Image
from reportlab.platypus import Table
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, PageBreak
from utils import get_litteral_date
from datetime import datetime
# from astrology import ExportHours


class ExportHours:
    treatmentCase = 'day'
    fileName = 'pdfTable.pdf'
    author = 'Sébastien COMTE'    # To do variabiliser
    address = ''
    docTitle = 'Extraction des heures planétaires'   # To do variabilise
    hourList = []
    week = 0
    weekStart = 0
    weekEnd = 0
    weekList = []
    weekCount = 0
    month = 0
    monthName = ''
    year = 0
    moonPhase = []


class TabLine:
    hourNumber = 'Heure n°'
    planetPicPath = ''
    planetName = ''
    hourStart = 'Début'
    hourEnd = 'Fin'


class TabTitle:
    dayName = ''
    dayPlanetName = ''
    planetPicPath = ''
    moonPicPath = ''


class ColorStyle:
    def __init__(self):  # Notre méthode constructeur
        self.styleType = 1
        self.titleBackground = ''
        self.titleFontColor = ''
        self.headerBackground = ''
        self.headerFontColor = ''
        self.alternateLineColor = False
        self.lineColor1 = ''
        self.lineColor2 = ''

    def setStyle(self):
        styleTab = {
            1: {
                'titleBackground': '#191970',
                'titleFontColor': '#ffffff',
                'headerBackground': '#191970',
                'headerFontColor': '#ffffff',
                'alternateLineColor': True,
                'lineColor1': '#ffffff',
                'lineColor2': '#A9E2F3',
            },
            2: {
                'titleBackground': '#9a0000',
                'titleFontColor': '#ffffff',
                'headerBackground': '#9a0000',
                'headerFontColor': '#ffffff',
                'alternateLineColor': True,
                'lineColor1': '#ff5f5f',
                'lineColor2': '#ffffff',
            },
            3: {
                'titleBackground': '#1b6413',
                'titleFontColor': '#ffffff',
                'headerBackground': '#1b6413',
                'headerFontColor': '#ffffff',
                'alternateLineColor': True,
                'lineColor1': '#6fed61',
                'lineColor2': '#ffffff',
            },
        }

        currentStyle = styleTab[self.styleType]
        self.titleBackground = currentStyle['titleBackground']
        self.titleFontColor = currentStyle['titleFontColor']
        self.headerBackground = currentStyle['headerBackground']
        self.headerFontColor = currentStyle['headerFontColor']
        self.alternateLineColor = currentStyle['alternateLineColor']
        self.lineColor1 = currentStyle['lineColor1']
        self.lineColor2 = currentStyle['lineColor2']


class TabStyle:
    titleTableSize = []
    headerTableSize = []
    linesTableSize = []
    hourElemWidth = 0
    picturePlanetSize = 0
    picturePlanetPosition = 0
    pictureMoonSize = 0
    pictureMoonPosition = 0
    picRowPlanetStyle = TableStyle()
    titleTableStyle = TableStyle()
    picPlanetTitleStyle = TableStyle()
    picMoonTitleStyle = TableStyle()
    headerStyle = TableStyle()
    linesStyle = TableStyle()
    linesStyleAlternate = []
    hourElemStyle = TableStyle()


class exportDatas:
    """Classe permettant d'effectuer l'export des datas en pdf
"""

    def __init__(self):  # Notre méthode constructeur
        """Pour l'instant, on ne va définir qu'un seul attribut"""
        self.exportHours = ExportHours()
        self.topMargin = 20
        self.leftMargin = 20
        self.rightMargin = 20
        self.bottomMargin = 20
        self.workingList = []
        self.workingLine = {}
        self.moonStage = ''
        self.colorStyle = 1

    def getTabLine(self):
        tabLine = TabLine()
        tabLine.hourNumber = self.workingLine["index"]
        tabLine.planetPicPath = 'images/' + \
            self.workingLine["planet"].lower() + '_ex.png'
        tabLine.planetName = self.workingLine["planet"]
        tabLine.hourStart = self.workingLine["hour_start"]
        tabLine.hourEnd = self.workingLine["hour_end"]

        return tabLine

    def getTabTitle(self):
        tabTitle = TabTitle()
        inputDate = self.workingList[0]["date"]
        dateName = get_litteral_date(inputDate)
        tabTitle.dayName = dateName
        tabTitle.dayPlanetName = self.workingList[0]["day_planet"]
        tabTitle.planetPicPath = 'images/' + \
            self.workingList[0]["day_planet"].lower() + '.png'
        if (self.moonStage):
            tabTitle.moonPicPath = 'images/moon_phase_'.lower() + str(self.moonStage) + '.png'
        else:
            tabTitle.moonPicPath = ''
        return tabTitle

    def getTabStyle(self):
        colorStyle = ColorStyle()
        colorStyle.styleType = self.colorStyle
        colorStyle.setStyle()

        tabStyle = TabStyle()
        tabStyle.titleTableSize = [10, 20, 55, 10]
        tabStyle.headerTableSize = [15, 40, 20, 20]
        tabStyle.linesTableSize = [15, 10, 30, 20, 20]
        tabStyle.hourElemWidth = 95
        tabStyle.picturePlanetSize = 8
        tabStyle.picturePlanetPosition = 10
        tabStyle.pictureMoonSize = 7
        tabStyle.pictureMoonPosition = 7
        tabStyle.picRowPlanetStyle = TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('LEFTPADDING', (0, 0), (-1, -1), 7),
            ('TOPPADDING', (0, 0), (-1, -1), 0),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
            # ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ])
        tabStyle.titleTableStyle = TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            # ('BACKGROUND', (0, 0), (3, 0), colors.HexColor("#191970")),
            ('BACKGROUND', (0, 0), (3, 0), colors.HexColor(colorStyle.titleBackground)),
            # ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.HexColor(colorStyle.titleFontColor)),
            ('FONTSIZE', (0, 0), (-1, -1), 4),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('TOPPADDING', (0, 0), (-1, -1), 5),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 0),
            ('LEFTPADDING', (0, 0), (-1, -1), 5),
            # ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ])
        tabStyle.picPlanetTitleStyle = TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('LEFTPADDING', (0, 0), (-1, -1), 4),
            ('TOPPADDING', (0, 0), (-1, -1), 0),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
            ('RIGHTPADDING', (0, 0), (-1, -1), 0),
            # ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ])
        tabStyle.picMoonTitleStyle = TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('LEFTPADDING', (0, 0), (-1, -1), 0),
            ('TOPPADDING', (0, 0), (-1, -1), 0),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
            ('RIGHTPADDING', (0, 0), (-1, -1), 0),
            # ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ])
        tabStyle.headerStyle = TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            # ('BACKGROUND', (0, 0), (3, 0), colors.darkblue),
            # ('BACKGROUND', (0, 0), (3, 0), colors.HexColor("#191970")),
            ('BACKGROUND', (0, 0), (3, 0), colors.HexColor(colorStyle.headerBackground)),
            # ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.HexColor(colorStyle.headerFontColor)),
            ('FONTSIZE', (0, 0), (-1, -1), 6),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('TOPPADDING', (0, 0), (-1, -1), 5),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 0),
            ('LEFTPADDING', (0, 0), (-1, -1), 5),
            # ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ])

        tabStyle.linesStyle = TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTSIZE', (0, 0), (-1, -1), 6),
            ('TOPPADDING', (0, 0), (-1, -1), 4),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 0),
            ('LEFTPADDING', (0, 0), (-1, -1), 5),
            # ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ])

        # 2) Alternate backgroud color
        if colorStyle.alternateLineColor:
            rowNumb = len(self.workingList)
            # #87CEFA -->DeepSkyBlue
            # #00FFFF --> html aqua/cyan
            # #A9E2F3
            ts = []
            for i in range(rowNumb):
                bc = colors.HexColor(
                    colorStyle.lineColor1) if i % 2 == 0 else colors.HexColor(colorStyle.lineColor2)
                ts.append(('BACKGROUND', (0, i), (-1, i), bc))

            tabStyle.linesStyleAlternate = ts
        else:
            tabStyle.linesStyle = TableStyle([
                ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor(colorStyle.lineColor1))
            ])

        tabStyle.hourElemStyle = TableStyle([
            ('BOX', (0, 0), (-1, -1), 1, colors.black),

            ('TOPPADDING', (0, 0), (-1, -1), 0),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 0),
            ('LEFTPADDING', (0, 0), (-1, -1), 0),
            ('RIGHTPADDING', (0, 0), (-1, -1), 0),
        ])
        return tabStyle

    def genhourTable(self):
        hourElemTable = None

        tabStyle = self.getTabStyle()
        # Main width
        # hourElemWidth = 95

        tabTitle = self.getTabTitle()
        picturePlanet = Image(tabTitle.planetPicPath)
        picturePlanet.drawWidth = tabStyle.picturePlanetSize
        picturePlanet.drawHeight = tabStyle.picturePlanetSize
        picPlanetTable = Table(
            [[picturePlanet]], tabStyle.picturePlanetPosition, tabStyle.picturePlanetPosition)

        if tabTitle.moonPicPath:
            pictureMoon = Image(tabTitle.moonPicPath)
            pictureMoon.drawWidth = tabStyle.pictureMoonSize
            pictureMoon.drawHeight = tabStyle.pictureMoonSize
            picMoonTable = Table(
                [[pictureMoon]], tabStyle.pictureMoonPosition, tabStyle.pictureMoonPosition)
        else:
            picMoonTable = Table(
                [['']], tabStyle.pictureMoonPosition, tabStyle.pictureMoonPosition)

        # 1) Build Structure
        titleTable = Table([
            [picPlanetTable, tabTitle.dayPlanetName, tabTitle.dayName, picMoonTable]
        ], tabStyle.titleTableSize)

        headerTable = Table([
            ['N°', 'Planète', 'Début', 'Fin']
        ], tabStyle.headerTableSize)

        lineDatas = []
        for line in self.workingList:
            self.workingLine = line
            hourElemTableCurrent = hourElemTable
            tabline = self.getTabLine()

            picRowPlanet = Image(tabline.planetPicPath)
            picRowPlanet.drawWidth = 8
            picRowPlanet.drawHeight = 8
            picRowPlanet = Table([[picRowPlanet]], 10, 10)

            picRowPlanet.setStyle(tabStyle.picRowPlanetStyle)

            row = [
                tabline.hourNumber,
                picRowPlanet,
                tabline.planetName,
                tabline.hourStart,
                tabline.hourEnd
            ]
            lineDatas.append(row)

        linesTable = Table(lineDatas, tabStyle.linesTableSize)

        hourElemTable = Table([
            [titleTable],
            [headerTable],
            [linesTable]
        ], tabStyle.hourElemWidth)

        # 2) Add Style
        '''
        # List available fonts
        from reportlab.pdfgen import canvas
        for font in canvas.Canvas('abc').getAvailableFonts():
            print(font)
        '''

        titleTable.setStyle(tabStyle.titleTableStyle)
        picPlanetTable.setStyle(tabStyle.picPlanetTitleStyle)
        picMoonTable.setStyle(tabStyle.picMoonTitleStyle)
        headerTable.setStyle(tabStyle.headerStyle)
        linesTable.setStyle(tabStyle.linesStyle)
        linesTable.setStyle(TableStyle(tabStyle.linesStyleAlternate))
        hourElemTable.setStyle(tabStyle.hourElemStyle)

        return hourElemTable

    def make_export(self):
        night_tab_list = []
        styles = getSampleStyleSheet()
        elems = []

        pdf = SimpleDocTemplate(self.exportHours.fileName,
                                pagesize=landscape(A4),
                                title=self.exportHours.docTitle,
                                author=self.exportHours.author,
                                # topMargin=margins[0],
                                # leftMargin=margins[1],
                                # rightMargin=margins[2],
                                # bottomMargin=margins[3]
                                topMargin=self.topMargin,
                                leftMargin=self.leftMargin,
                                rightMargin=self.rightMargin,
                                bottomMargin=self.bottomMargin
                                )

        if (self.exportHours.treatmentCase == 'day'):
            day_tab_list = []
            self.workingList = self.exportHours.hourList['day_list'] + \
                self.exportHours.hourList['night_list']
            self.moonStage = self.exportHours.hourList['moon_stage']
            day_tab_list.append(self.genhourTable())

            mainTable = Table([
                day_tab_list
            ])

            elems.append(mainTable)
        else:
            for week in self.exportHours.hourList:
                self.weekIndex = self.exportHours.hourList.index(week)
                if (self.exportHours.treatmentCase == 'week'):
                    pageTitle = '{} {} {} {}'.format('Semaine n°',
                                                     str(self.exportHours.week),
                                                     'année',
                                                     str(self.exportHours.year)
                                                     )

                if (self.exportHours.treatmentCase == 'month'):
                    pageTitle = '{} : {} {} {} {}'.format(self.exportHours.monthName,
                                                          'Semaine n°',
                                                          str(self.exportHours.weekList[self.exportHours.hourList.index(
                                                              week)]),
                                                          'année',
                                                          str(self.exportHours.year)
                                                          )

                if (self.exportHours.treatmentCase == 'year'):
                    pageTitle = '{} {} {} {}'.format('Semaine n°',
                                                     str(self.exportHours.weekList[self.exportHours.hourList.index(
                                                         week)]),
                                                     'année',
                                                     str(self.exportHours.year)
                                                     )

                text = '<font size=22>%s</font>' % pageTitle
                elems.append(Paragraph(text, styles["Heading1"]))

                day_tab_list = []
                # print(len(input))
                for day_tab in week:
                    # print(day_tab['date'])
                    self.workingList = day_tab['day_list'] + \
                        day_tab['night_list']
                    self.moonStage = day_tab['moon_stage']
                    day_tab_list.append(self.genhourTable())

                mainTable = Table([
                    day_tab_list
                ])

                elems.append(mainTable)

                text = '<font size=18>%s</font>' % self.exportHours.address
                elems.append(Paragraph(text, styles["Heading2"]))
                # elems.append(Spacer(1, 12))
                elems.append(PageBreak())

            # text = '<font size=22>%s</font>' % "Test de titre en attendant les vraies infos"
            # elems.append(Paragraph(text, styles["Heading1"]))

        pdf.build(elems)
