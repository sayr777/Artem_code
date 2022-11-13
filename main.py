from kivymd.app import MDApp
from kivymd.theming import ThemeManager
from kivy.properties import ObjectProperty, StringProperty, NumericProperty
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.lang import Builder
from kivy_garden.mapview import MapMarker, MapView, MapSource, MarkerMapLayer
from kivy_garden.mapview.clustered_marker_layer import ClusteredMarkerLayer
from kivy_garden.mapview.geojson import GeoJsonMapLayer
from kivy_garden.mapview.utils import get_zoom_for_radius, haversine
from kivymd.uix.list import OneLineListItem, TwoLineListItem, ThreeLineListItem
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
from dialog import Dialog
from data import Data
import user_info
import matplotlib
from news import News
from gps import Gps
from user import User
from profiledetails import ProfileDetails
from notes import Notes
from addnote import AddNote
from regionchooser import RegionChooser
from yaweather import city_location as cl
from yaweather import yandex_weather as yw
from yaweather import condit
from app_info import window_manager as WM
from notification import XNotification
import re
import random
import io
import datetime
import requests
import base64
import os
import urllib.parse
import plyer
from kivy.core.text import LabelBase
from kivymd.font_definitions import theme_font_styles
from kivy.uix.image import Image
from kivy.core.image import Image as CoreImage
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.dialog import MDDialog
from kivy.clock import mainthread
import sqlite3 as SQLCommander
from sms_base import rec_otp
from kivy.uix.popup import Popup
import json
#from shapely.geometry import Point
#from shapely.geometry import Polygon

from kivy.core.window import Window

#subimport
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.textfield import MDTextField
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDRoundFlatButton
from kivymd.uix.button import MDFillRoundFlatIconButton
from kivymd.uix.toolbar import *
from kivymd.uix.button import MDIconButton
from kivymd.uix.button import MDFlatButton
from kivymd.uix.relativelayout import RelativeLayout
from kivymd.uix.bottomsheet import MDCustomBottomSheet
from kivy import platform
from kivy.factory import Factory
from kivymd.uix.card import MDCard

if platform == 'android':
    from android.permissions import Permission, request_permissions
    request_permissions([Permission.INTERNET])

KIVY_FILENAME = 'main.kv'

MONTH_LIST = {
    '1' : 'Январь',
    '2' : 'Февраль',
    '3' : 'Март',
    '4' : 'Апрель',
    '5' : 'Май',
    '6' : 'Июнь',
    '7' : 'Июль',
    '8' : 'Август',
    '9' : 'Сентябрь',
    '10' : 'Октябрь',
    '11' : 'Ноябрь',
    '12' : 'Декабрь'
}

CALENDAR_CODE = [
    [2, 2, 2, 2, 2, 2, 3, 3, 3, 3, 2, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 3, 3, 3, 3, 3, 2, 2, 2, 2, 2, 2],
    [0, 0, 0, 0, 0, 0, 0, 0, 1, 2, 2, 2, 2, 2, 0, 0, 0, 2, 2, 2, 3, 3, 3, 3, 2, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 1, 2, 2, 2, 2, 2, 0, 0, 0, 2, 2, 3, 3, 3, 3, 3, 3, 3, 2, 2, 1, 1, 0, 0, 0, 0, 0, 0]
]

class BaseChillOne(Screen):
    base_chill_full_name = StringProperty()
    base_chill_location = StringProperty()
    base_chill_addition_items = StringProperty()
    base_chill_telephone = StringProperty()

    def entering(self):
        data = json.loads(Data.data_base_chill)
        res = None
        for item in data:
            if item['fields']['base_chill_name'] == Data.base_chill_name:
                res = item
                break
        self.base_chill_full_name = res['fields']['base_chill_full_name']
        self.base_chill_location = res['fields']['base_chill_location'].replace('\\n', '\n')
        self.base_chill_addition_items = res['fields']['base_chill_additional_items'].replace('\\n', '\n')
        self.base_chill_telephone = res['fields']['base_chill_telephone']
        Data.object_map_lon = res['fields']['base_chill_longitude']
        Data.object_map_lat = res['fields']['base_chill_latitude']

    def click_on_show_map(self):
        self.parent.current = 'GPSHelper'
        self.parent.get_screen('GPSHelper').showObjectMap()

class OneRecipe(Screen):
    recipe_image = ObjectProperty()
    recipe_name = StringProperty()
    recipe_ingredients = StringProperty()
    recipe_recipe = StringProperty()

    def entering(self):
        data = json.loads(Data.data_recipe)
        res = None
        for item in data:
            if item['fields']['recipe_name'] == Data.recipe_name:
                res = item
                break
        self.recipe_name = res['fields']['recipe_name']
        self.recipe_ingredients = res['fields']['recipe_ingredients'].replace('\\n', '\n')
        self.recipe_recipe = res['fields']['recipe_recipe'].replace('\\n', '\n')
        if not os.path.exists("pics_recipes/"+self.recipe_name+'.jpg'):
            with open("pics_recipes/"+self.recipe_name+'.jpg', 'wb') as fh:
                fh.write(base64.b64decode(res['fields']['recipe_image'][2:-1]))
        self.recipe_image.source = "pics_recipes/"+self.recipe_name+'.jpg'

class PlaceChill(Screen):
    box_content = ObjectProperty()

    def entering(self):
        data = json.loads(Data.data_base_chill)
        self.box_content.clear_widgets()
        for item in data:
            self.box_content.add_widget(MDRoundFlatButton(size_hint_x=0.85, font_size='18sp', text=item['fields']['base_chill_name'], theme_text_color='Custom', text_color=(0, 0, 0, 1.0), md_bg_color=(1.0, 1.0, 1.0, 1.0), line_color=(1.0, 1.0, 1.0, 1.0), halign='left', on_release=self.click_on_place))

    def click_on_place(self, obj):
        Data.base_chill_name = obj.text
        self.parent.current = 'BaseChillOne'

class EquipmentOne(Screen):
    equipment_name = StringProperty()
    equipment_time_address = StringProperty()
    equipment_products = StringProperty()
    equipment_telephone = StringProperty()

    def entering(self):
        data = json.loads(Data.data_equipment)
        res = None
        for item in data:
            if item['fields']['equipment_name'] == Data.equipment_name:
                res = item
                break
        self.equipment_name = res['fields']['equipment_name']
        self.equipment_time_address = res['fields']['equipment_time_adress']
        self.equipment_products = res['fields']['equipment_products'].replace('\\n', '\n')
        self.equipment_telephone = res['fields']['equipment_telephone']
        Data.object_map_lon = res['fields']['equipment_longitude']
        Data.object_map_lat = res['fields']['equipment_latitude']

    def click_on_show_map(self):
        self.parent.current = 'GPSHelper'
        self.parent.get_screen('GPSHelper').showObjectMap()

class Equipment(Screen):
    box_content = ObjectProperty()

    def entering(self):
        data = json.loads(Data.data_equipment)
        self.box_content.clear_widgets()
        for item in data:
            self.box_content.add_widget(MDRoundFlatButton(size_hint_x=0.85, font_size='18sp', text=item['fields']['equipment_name'], theme_text_color='Custom', text_color=(0, 0, 0, 1.0), md_bg_color=(1.0, 1.0, 1.0, 1.0), line_color=(1.0, 1.0, 1.0, 1.0), halign='left', on_release=self.click_on_place))

    def click_on_place(self, obj):
        Data.equipment_name = obj.text
        self.parent.current = 'EquipmentOne'

class BaitOne(Screen):
    bait_name = StringProperty()
    bait_time_address = StringProperty()
    bait_products = StringProperty()
    bait_telephone = StringProperty()

    def entering(self):
        data = json.loads(Data.data_bait)
        res = None
        for item in data:
            if item['fields']['bait_name'] == Data.bait_name:
                res = item
                break
        self.bait_name = res['fields']['bait_name']
        self.bait_time_address = res['fields']['bait_time_adress']
        self.bait_products = res['fields']['bait_products'].replace('\\n', '\n')
        self.bait_telephone = res['fields']['bait_telephone']
        Data.object_map_lon = res['fields']['bait_longitude']
        Data.object_map_lat = res['fields']['bait_latitude']

    def click_on_show_map(self):
        self.parent.current = 'GPSHelper'
        self.parent.get_screen('GPSHelper').showObjectMap()

class Bait(Screen):
    box_content = ObjectProperty()

    def entering(self):
        data = json.loads(Data.data_bait)
        self.box_content.clear_widgets()
        for item in data:
            self.box_content.add_widget(MDRoundFlatButton(size_hint_x=0.85, font_size='18sp', text=item['fields']['bait_name'], theme_text_color='Custom', text_color=(0, 0, 0, 1.0), md_bg_color=(1.0, 1.0, 1.0, 1.0), line_color=(1.0, 1.0, 1.0, 1.0), halign='left', on_release=self.click_on_place))
    
    def click_on_place(self, obj):
        Data.bait_name = obj.text
        self.parent.current = 'BaitOne'

class BuyFishOne(Screen):
    buy_fish_name = StringProperty()
    buy_fish_time_address = StringProperty()
    buy_fish_telephone = StringProperty()

    def entering(self):
        data = json.loads(Data.data_buy_fish)
        res = None
        for item in data:
            if item['fields']['buy_fish_name'] == Data.buy_fish_name:
                res = item
                break
        self.buy_fish_name = res['fields']['buy_fish_name']
        self.buy_fish_time_address = res['fields']['buy_fish_time_adress']
        self.buy_fish_telephone = res['fields']['buy_fish_telephone']
        Data.object_map_lon = res['fields']['buy_fish_longitude']
        Data.object_map_lat = res['fields']['buy_fish_latitude']

    def click_on_show_map(self):
        self.parent.current = 'GPSHelper'
        self.parent.get_screen('GPSHelper').showObjectMap()

class BuyFish(Screen):
    box_content = ObjectProperty()

    def entering(self):
        data = json.loads(Data.data_buy_fish)
        self.box_content.clear_widgets()
        for item in data:
            self.box_content.add_widget(MDRoundFlatButton(size_hint_x=0.85, font_size='18sp', text=item['fields']['buy_fish_name'], theme_text_color='Custom', text_color=(0, 0, 0, 1.0), md_bg_color=(1.0, 1.0, 1.0, 1.0), line_color=(1.0, 1.0, 1.0, 1.0), halign='left', on_release=self.click_on_place))
    
    def click_on_place(self, obj):
        Data.buy_fish_name = obj.text
        self.parent.current = 'BuyFishOne'

class Calendar(Screen):
    one_label = ObjectProperty()
    two_label = ObjectProperty()
    three_label = ObjectProperty()
    four_label = ObjectProperty()
    fife_label = ObjectProperty()
    six_label = ObjectProperty()
    seven_label = ObjectProperty()
    eight_label = ObjectProperty()
    nine_label = ObjectProperty()
    ten_label = ObjectProperty()
    eleven_label = ObjectProperty()
    twelve_label = ObjectProperty()
    thirteen_label = ObjectProperty()
    fourteen_label = ObjectProperty()
    fifteen_label = ObjectProperty()
    sixteen_label = ObjectProperty()
    seventeen_label = ObjectProperty()
    eightteen_label = ObjectProperty()
    nineteen_label = ObjectProperty()
    twenty_label = ObjectProperty()
    twenty_one_label = ObjectProperty()
    twenty_two_label = ObjectProperty()
    twenty_three_label = ObjectProperty()
    twenty_four_label = ObjectProperty()
    twenty_five_label = ObjectProperty()
    twenty_six_label = ObjectProperty()
    twenty_seven_label = ObjectProperty()
    twenty_eight_label = ObjectProperty()
    twenty_nine_label = ObjectProperty()
    thirty_label = ObjectProperty()
    thirty_one_label = ObjectProperty()
    icom_weather = ObjectProperty()
    icon_wind = ObjectProperty()
    icon_pressure = ObjectProperty()
    icon_humidity = ObjectProperty()

    curMonth = StringProperty()
    temperature = StringProperty()
    wind = StringProperty()
    humidity = StringProperty()
    pressure = StringProperty()
    territory = StringProperty()
    dateAndTime = StringProperty()
    weather_description = StringProperty()
    curYear = StringProperty()
    current_month = 0

    def build_calendar(self):
        if self.current_month in [1, 3, 5, 7, 8, 10, 12]:
            self.twenty_nine_label.opacity = 1
            self.thirty_label.opacity = 1
            self.thirty_one_label.opacity = 1
        elif self.current_month in [2]:
       	    self.twenty_nine_label.opacity = 0
            self.thirty_label.opacity = 0
            self.thirty_one_label.opacity = 0
        elif self.current_month in [4, 6, 9, 11]:
            self.twenty_nine_label.opacity = 1
            self.thirty_label.opacity = 1
            self.thirty_one_label.opacity = 0

    def entering(self):
        self.curMonth = '  ' + MONTH_LIST[str(datetime.datetime.now().month)]
        self.curYear = str(datetime.datetime.now().year)
        self.current_month = datetime.datetime.now().month
        self.check_penalti()
        self.build_calendar()
        latitude = cl('Астрахань')[0]
        longtitude = cl('Астрахань')[1]

        data = yw(latitude, longtitude, '6c229def-853b-4dbc-a510-0b33f6d710d3')

        self.territory = 'Астрахань'
        self.dateAndTime = str(data['forecast']['date']) + ' , ' + str(datetime.datetime.now().hour) + ':' + str(datetime.datetime.now().minute)
        self.temperature = str(data['fact']['temp']) + 'C'
        self.wind = str(data['fact']['wind_speed']) + ' ' + str(data['fact']['wind_class'])
        self.humidity = str(data['fact']['humidity'])
        self.pressure = str(data['fact']['pressure_mm'])
        self.weather_description = str(data['fact']['condition'])

        self.icon_weather.icon = condit[self.weather_description]

    def click_on_cell(self, widget):
        day = int(widget.text)
        if widget.text_color == [1.0, 0.0, 0.0, 1.0]:
            Dialog('Вылов рыбы в этот день запрещен!', 'Внимание!!!')
            Data.number_rule = 1
            self.parent.get_screen('PenaltieList').ids.zag.text = self.parent.get_screen('PenaltieList').data[Data.number_rule][0]
            self.parent.get_screen('PenaltieList').ids.main_text.text = self.parent.get_screen('PenaltieList').data[Data.number_rule][1]
            Data.screen_history.append('Calendar')
            self.parent.current = 'PenaltieList'
        else:
            Data.screen_history.append('Calendar')
            self.parent.current = 'Itog'
            
    def check_penalti(self):
        if self.current_month == 5:
            self.one_label.text_color = [0.0, 0.0, 0.0, 1.0]
            self.two_label.text_color = [0.0, 0.0, 0.0, 1.0]
            self.three_label.text_color = [0.0, 0.0, 0.0, 1.0]
            self.four_label.text_color = [0.0, 0.0, 0.0, 1.0]
            self.fife_label.text_color = [0.0, 0.0, 0.0, 1.0]
            self.six_label.text_color = [0.0, 0.0, 0.0, 1.0]
            self.seven_label.text_color = [0.0, 0.0, 0.0, 1.0]
            self.eight_label.text_color = [0.0, 0.0, 0.0, 1.0]
            self.nine_label.text_color = [0.0, 0.0, 0.0, 1.0]
            self.ten_label.text_color = [0.0, 0.0, 0.0, 1.0]
            self.eleven_label.text_color = [0.0, 0.0, 0.0, 1.0]
            self.twelve_label.text_color = [0.0, 0.0, 0.0, 1.0]
            self.thirteen_label.text_color = [0.0, 0.0, 0.0, 1.0]
            self.fourteen_label.text_color = [0.0, 0.0, 0.0, 1.0]
            self.fifteen_label.text_color = [0.0, 0.0, 0.0, 1.0]
            self.sixteen_label.text_color = [1.0, 0.0, 0.0, 1.0]
            self.seventeen_label.text_color = [1.0, 0.0, 0.0, 1.0]
            self.eightteen_label.text_color = [1.0, 0.0, 0.0, 1.0]
            self.nineteen_label.text_color = [1.0, 0.0, 0.0, 1.0]
            self.twenty_label.text_color = [1.0, 0.0, 0.0, 1.0]
            self.twenty_one_label.text_color = [1.0, 0.0, 0.0, 1.0]
            self.twenty_two_label.text_color = [1.0, 0.0, 0.0, 1.0]
            self.twenty_three_label.text_color = [1.0, 0.0, 0.0, 1.0]
            self.twenty_four_label.text_color = [1.0, 0.0, 0.0, 1.0]
            self.twenty_five_label.text_color = [1.0, 0.0, 0.0, 1.0]
            self.twenty_six_label.text_color = [1.0, 0.0, 0.0, 1.0]
            self.twenty_seven_label.text_color = [1.0, 0.0, 0.0, 1.0]
            self.twenty_eight_label.text_color = [1.0, 0.0, 0.0, 1.0]
            self.twenty_nine_label.text_color = [1.0, 0.0, 0.0, 1.0]
            self.thirty_label.text_color = [1.0, 0.0, 0.0, 1.0]
            self.thirty_one_label.text_color = [1.0, 0.0, 0.0, 1.0]
        elif self.current_month == 6:
            self.one_label.text_color = [1.0, 0.0, 0.0, 1.0]
            self.two_label.text_color = [1.0, 0.0, 0.0, 1.0]
            self.three_label.text_color = [1.0, 0.0, 0.0, 1.0]
            self.four_label.text_color = [1.0, 0.0, 0.0, 1.0]
            self.fife_label.text_color = [1.0, 0.0, 0.0, 1.0]
            self.six_label.text_color = [1.0, 0.0, 0.0, 1.0]
            self.seven_label.text_color = [1.0, 0.0, 0.0, 1.0]
            self.eight_label.text_color = [1.0, 0.0, 0.0, 1.0]
            self.nine_label.text_color = [1.0, 0.0, 0.0, 1.0]
            self.ten_label.text_color = [1.0, 0.0, 0.0, 1.0]
            self.eleven_label.text_color = [1.0, 0.0, 0.0, 1.0]
            self.twelve_label.text_color = [1.0, 0.0, 0.0, 1.0]
            self.thirteen_label.text_color = [1.0, 0.0, 0.0, 1.0]
            self.fourteen_label.text_color = [1.0, 0.0, 0.0, 1.0]
            self.fifteen_label.text_color = [1.0, 0.0, 0.0, 1.0]
            self.sixteen_label.text_color = [1.0, 0.0, 0.0, 1.0]
            self.seventeen_label.text_color = [1.0, 0.0, 0.0, 1.0]
            self.eightteen_label.text_color = [1.0, 0.0, 0.0, 1.0]
            self.nineteen_label.text_color = [1.0, 0.0, 0.0, 1.0]
            self.twenty_label.text_color = [1.0, 0.0, 0.0, 1.0]
            self.twenty_one_label.text_color = [0.0, 0.0, 0.0, 1.0]
            self.twenty_two_label.text_color = [0.0, 0.0, 0.0, 1.0]
            self.twenty_three_label.text_color = [0.0, 0.0, 0.0, 1.0]
            self.twenty_four_label.text_color = [0.0, 0.0, 0.0, 1.0]
            self.twenty_five_label.text_color = [0.0, 0.0, 0.0, 1.0]
            self.twenty_six_label.text_color = [0.0, 0.0, 0.0, 1.0]
            self.twenty_seven_label.text_color = [0.0, 0.0, 0.0, 1.0]
            self.twenty_eight_label.text_color = [0.0, 0.0, 0.0, 1.0]
            self.twenty_nine_label.text_color = [0.0, 0.0, 0.0, 1.0]
            self.thirty_label.text_color = [0.0, 0.0, 0.0, 1.0]
            self.thirty_one_label.text_color = [0.0, 0.0, 0.0, 1.0]
        else:
            self.one_label.text_color = [0.0, 0.0, 0.0, 1.0]
            self.two_label.text_color = [0.0, 0.0, 0.0, 1.0]
            self.three_label.text_color = [0.0, 0.0, 0.0, 1.0]
            self.four_label.text_color = [0.0, 0.0, 0.0, 1.0]
            self.fife_label.text_color = [0.0, 0.0, 0.0, 1.0]
            self.six_label.text_color = [0.0, 0.0, 0.0, 1.0]
            self.seven_label.text_color = [0.0, 0.0, 0.0, 1.0]
            self.eight_label.text_color = [0.0, 0.0, 0.0, 1.0]
            self.nine_label.text_color = [0.0, 0.0, 0.0, 1.0]
            self.ten_label.text_color = [0.0, 0.0, 0.0, 1.0]
            self.eleven_label.text_color = [0.0, 0.0, 0.0, 1.0]
            self.twelve_label.text_color = [0.0, 0.0, 0.0, 1.0]
            self.thirteen_label.text_color = [0.0, 0.0, 0.0, 1.0]
            self.fourteen_label.text_color = [0.0, 0.0, 0.0, 1.0]
            self.fifteen_label.text_color = [0.0, 0.0, 0.0, 1.0]
            self.sixteen_label.text_color = [0.0, 0.0, 0.0, 1.0]
            self.seventeen_label.text_color = [0.0, 0.0, 0.0, 1.0]
            self.eightteen_label.text_color = [0.0, 0.0, 0.0, 1.0]
            self.nineteen_label.text_color = [0.0, 0.0, 0.0, 1.0]
            self.twenty_label.text_color = [0.0, 0.0, 0.0, 1.0]
            self.twenty_one_label.text_color = [0.0, 0.0, 0.0, 1.0]
            self.twenty_two_label.text_color = [0.0, 0.0, 0.0, 1.0]
            self.twenty_three_label.text_color = [0.0, 0.0, 0.0, 1.0]
            self.twenty_four_label.text_color = [0.0, 0.0, 0.0, 1.0]
            self.twenty_five_label.text_color = [0.0, 0.0, 0.0, 1.0]
            self.twenty_six_label.text_color = [0.0, 0.0, 0.0, 1.0]
            self.twenty_seven_label.text_color = [0.0, 0.0, 0.0, 1.0]
            self.twenty_eight_label.text_color = [0.0, 0.0, 0.0, 1.0]
            self.twenty_nine_label.text_color = [0.0, 0.0, 0.0, 1.0]
            self.thirty_label.text_color = [0.0, 0.0, 0.0, 1.0]
            self.thirty_one_label.text_color = [0.0, 0.0, 0.0, 1.0]

    def preMonth(self):
        self.current_month -= 1
        if self.current_month == 0:
            self.current_month = 12
        self.check_penalti()
        self.build_calendar()
        self.curMonth = '  ' + MONTH_LIST[str(self.current_month)]

    def postMonth(self):
        self.current_month += 1
        if self.current_month == 13:
            self.current_month = 1
        self.check_penalti()
        self.build_calendar()
        self.curMonth = '  ' + MONTH_LIST[str(self.current_month)]

class Itog(Screen):
    box_content = ObjectProperty()

    def entering(self):
        self.box_content.clear_widgets()
        data = json.loads(Data.data_fish)
        for item in data:
            self.box_content.add_widget(MDFlatButton(pos_hint= {'center_y': 0.85}, font_size = '16sp', text= item['fields']['fish_name'],on_release= self.click_on_fish, bold= True))

    def click_on_fish(self, obj):
        Data.fish_catalog_name = obj.text
        self.parent.current = 'Fish'

class Rules(Screen):
    def click_on_rule_fishing(self):
        Data.number_rule = 0
        self.parent.get_screen('RuleFishing').ids.zag.text = self.parent.get_screen('RuleFishing').data[Data.number_rule][0]
        self.parent.get_screen('RuleFishing').ids.main_text.text = self.parent.get_screen('RuleFishing').data[Data.number_rule][1]
        Data.screen_history.append('Rules')
        self.parent.current = 'RuleFishing'

    def click_on_deadlines_spawning_off(self):
        Data.number_rule = 1
        self.parent.get_screen('RuleFishing').ids.zag.text = self.parent.get_screen('RuleFishing').data[Data.number_rule][0]
        self.parent.get_screen('RuleFishing').ids.main_text.text = self.parent.get_screen('RuleFishing').data[Data.number_rule][1]
        Data.screen_history.append('Rules')
        self.parent.current = 'RuleFishing'

    def click_on_spawning_areas(self):
        Data.number_rule = 2
        self.parent.get_screen('RuleFishing').ids.zag.text = self.parent.get_screen('RuleFishing').data[Data.number_rule][0]
        self.parent.get_screen('RuleFishing').ids.main_text.text = self.parent.get_screen('RuleFishing').data[Data.number_rule][1]
        Data.screen_history.append('Rules')
        self.parent.current = 'RuleFishing'

    def click_on_weapons_fishing(self):
        Data.number_rule = 3
        self.parent.get_screen('RuleFishing').ids.zag.text = self.parent.get_screen('RuleFishing').data[Data.number_rule][0]
        self.parent.get_screen('RuleFishing').ids.main_text.text = self.parent.get_screen('RuleFishing').data[Data.number_rule][1]
        Data.screen_history.append('Rules')
        self.parent.current = 'RuleFishing'

    def click_on_daily_rate_of_fish_catch(self):
        Data.number_rule = 4
        self.parent.get_screen('RuleFishing').ids.zag.text = self.parent.get_screen('RuleFishing').data[Data.number_rule][0]
        self.parent.get_screen('RuleFishing').ids.main_text.text = self.parent.get_screen('RuleFishing').data[Data.number_rule][1]
        Data.screen_history.append('Rules')
        self.parent.current = 'RuleFishing'

    def click_on_what_fish_off_fishing(self):
        Data.number_rule = 5
        self.parent.get_screen('RuleFishing').ids.zag.text = self.parent.get_screen('RuleFishing').data[Data.number_rule][0]
        self.parent.get_screen('RuleFishing').ids.main_text.text = self.parent.get_screen('RuleFishing').data[Data.number_rule][1]
        Data.screen_history.append('Rules')
        self.parent.current = 'RuleFishing'

    def click_on_size_penalti_fishing(self):
        Data.number_rule = 6
        self.parent.get_screen('RuleFishing').ids.zag.text = self.parent.get_screen('RuleFishing').data[Data.number_rule][0]
        self.parent.get_screen('RuleFishing').ids.main_text.text = self.parent.get_screen('RuleFishing').data[Data.number_rule][1]
        Data.screen_history.append('Rules')
        self.parent.current = 'RuleFishing'

    def click_on_what_can_pay_penalti_and_where(self):
        Data.number_rule = 7
        self.parent.get_screen('RuleFishing').ids.zag.text = self.parent.get_screen('RuleFishing').data[Data.number_rule][0]
        self.parent.get_screen('RuleFishing').ids.main_text.text = self.parent.get_screen('RuleFishing').data[Data.number_rule][1]
        Data.screen_history.append('Rules')
        self.parent.current = 'RuleFishing'

class RuleFishing(Screen):
    zag = ObjectProperty()
    main_text = ObjectProperty()

    data = [
        ['Правила рыболовства', '    Граждане вправе осуществлять любительское и спортивное рыболовство на водных объектах общего пользования свободно и бесплатно.\n\n    Однако, рыболов должен помнить, что во время лова он находится в границах водоохранных зон рек, озер, ручьев, каналов (50-200 м. от береговой линии в зависимости от протяженности водотока), где действует специальный режим осуществления хозяйственной и иной деятельности в целях предотвращения загрязнения, засорения, заиления указанных водных объектов и истощения их вод, а также сохранения среды обитания водных биологических ресурсов и других объектов животного и растительного мира.\n\n    В границах водоохранных зон запрещаются движение и стоянка транспортных средств (кроме специальных транспортных средств), за исключением их движения по дорогам и стоянки на дорогах и в специально оборудованных местах, имеющих твердое покрытие.\n\n    Нарушение данного запрета влечет за собой административную ответственность в виде штрафа для граждан в размере от трех тысяч до четырех тысяч пятисот рублей (статья 8.42 КоАП РФ).\n\n    В определенные месяцы, в области запрещено ловить рыбу. Ограничения вводятся в связи с периодом активного нереста. Ловить разрешается только на удочку. Количество крючков, используемых 1 человеком, должно быть не более 5.\n\n    Объем пойманной рыбы на одного человека не должен превышать 10 кг.'],
        ['Сроки нерестового запрета', '    Нерестовый период в Астраханской области в 2022 году устанавливается с 16 мая по 20 июня.\n\n    Запрещается любая рыбалка с 20 апреля по 20 июня — повсеместно, за исключением водных объектов рыбохозяйственного значения в пределах административных границ населенных пунктов, а также на рыбопромысловых участках, предоставленных для организации любительского и спортивного рыболовства в этот период. В эти месяцы запрещен отлов любого вида рыбы. Рыбалка разрешена, но только в специализированных водоемах и хранилищах.\n\n    В сроки, С 1 апреля по 30 июня запрещен вылов раков в любом количестве.\n\n    Запрещается:\n\n       •   любительская и спортивная охота на каспийского тюленя.\n\n       •   в запретных районах: волжское запретное предустьевое пространство, за исключением рыбопромысловых участков, предоставленных для организации любительского и спортивного рыболовства, нерестилища, зимовальные ямы.\n\n       •   применение колющих орудий лова, сетей всех типов, ловушек всех типов и конструкций (кроме раколовок), огнестрельного и пневматического оружия, арбалетов и луков, сомовников, капканов, крючковых самоловных снастей, сетных отцеживающих и объячеивающих орудий добычи (вылова) и приспособлений (бредней, неводов, волокуш, наметок, подъемников, кругов, «телевизоров», «экранов» и т.п.);\n\n       •   рыбалка кружками с общим количеством крючков более 10 штук на орудиях добычи (вылова) у одного гражданина;\n\n       •   рыбалка при помощи устройства заездок, загородок, заколок, запруд и других видов заграждений, частично или полностью перекрывающих русло водоемов и водотоков и препятствующих свободному перемещению рыбы;\n\n       •   рыбалка способом багрения, глушения, гона (в том числе с помощью бряцал и ботания), переметами с общим количеством крючков более 10 штук на орудиях добычи (вылова) у одного гражданина, «на подсветку»;\n\n       •   рыбалка жаберным способом (при использовании «жмыхоловок», «комбайнов») с количеством крючков более 2-х штук;\n\n       •   рыбалка раков руками вброд или путем ныряния.'],
        ['Нерестовые участки', '    Река Волга славится огромными территориями нерестилищ осетровой рыбы. Отправляясь на ловлю, стоит прочитать список (или лучше иметь его под рукой), чтобы выбрать правильное и не запрещенное место. Верхняя, средняя и нижняя зоны, следующие\n\n   •   Остров Спорный, Тракторный, Зеленый, Ельшанская, Рудневская. Протяженность нереста 1 км.\n\n   •   Остров Баррикадский, Татьянский – 2 км.\n\n   •   Гряд у Центрального стадиона. Протяженность нерестилища – 5 км.\n\n   •   Райгородская, Солодниковская гряда. Протяженность составляет 1 км.\n\n   •   Светлоярская и Дубовская зона. Территория занимает 2,5 км.\n\n   •   Каменноярская гряда – 6 км.\n\n   •   Соленозаймищенская, Пришибинская, Косикинская, Восточная. Протяженность гряды составляет 1 км.\n\n   •   Ветлянская, Верхнекопановская зона распространяется на 1,5 км.\n\n   •   Копановская, Сероглазовская имеет протяженность 2 км.\n\n   •   Цаган-Аманская – крупная гряда, которая протянулась на 8 км.\n\n    В период, когда начинается нерест, разрешена рыбалка, но только в специализированных местах с применением не более 2 крючков на одного человека.'],
        ['Орудия рыболовства', '    Для рыбалки в Астраханской области разрешается использовать следующие орудия и способы добычи (вылова):\n\n   •   поплавочная удочка, состоящая из удилища (в том числе с пропускными кольцами и со съемной катушкой с леской), лески, поплавка, грузил, поводков и крючков;\n\n   •   донная удочка (донка), состоящая из удилища (в том числе с пропускными кольцами и съемной катушкой с леской или шнуром) или хлыстика, лески или шнура, грузила, поводков и крючков;\n\n   •   донная удочка, состоящая из удилища (в том числе с пропускными кольцами и съемной катушкой с леской и шнуром) или хлыстика, лески, грузила, кормушки или жмыхоловки с количеством крючков не более 2-х штук;\n\n   •   донная удочка с амортизаторов (применяются только одинарные крючки);\n\n   •   блесны, воблеры, мушки и другие приманки, разные по форме и цвету с крючками (одинарными, двойниками или тройниками);\n\n   •   раколовки, в количестве не более трех штук у одного гражданина, каждый из параметров разрешаемых раколовок (длина, ширина, высота -для многоугольных, высота, диаметр - для конических и цилиндрических) не должны превышать 80 см:\n\n   •   добыча (вылов) на дорожку с применением гребного судна или плавучего средства с использованием не более двух приманок на одно судно или плавучее средство;\n\n   •   добыча (вылов) на троллинг - с применением паруса и/или мотора с использованием не более двух приманок на одно судно или плавучее средство;\n\n   •   добыча (вылов) рыбы «на квок»;\n\n   •   кораблики;\n\n   •   жерлицы;\n\n   •   специальные ружья и пистолеты для подводной охоты;\n\n   •   спиннинговая снасть (спиннинг), состоящую из удилища с пропускными кольцами и рукояткой, на которой крепится съемная катушка с леской или шнуром и оснащается одной приманкой с крючками (одинарными, двойниками или тройниками). Дополнительно перед приманкой может ставиться грузило без крючков.\n\n    Крючки - двойники или крючки - тройники применяются только при добыче (вылове) на спиннинг и жерлицу.'],
        ['Суточная норма вылова рыбы', '    Не только местные любят рыбачить на «своей» территории. Активность проявляют и любители попытать удачу в улове крупной рыбы с других регионов. Многие удильщики как можно раньше начинают готовиться к поездке. Необходимо закупить крючки, удочки и узнать период, когда стоит посещать водоем. Но после вступления закона в силу, рыбакам ограничили масштабы отлова. Введена суточная норма, чтобы не нарушать баланс и предотвратить исчезновение некоторых видов:\n\n   •   Суточная норма выловленной добычи не должна превышать 10 кг.\n\n   •   Кроме сома, можно ловить не более 1 экземпляра в одни руки.\n\n   •   Раков нельзя вылавливать больше 50 шт. При этом запрещено брать всех подряд. Особей меньше 10 см следует отпускать обратно.\n\n    Таким образом, рыбак может поймать каждого экземпляра рыбы не более 10 кг. В эту категорию, не попадает сом, так как его размеры могут быть весьма внушительные и не войти в обозначенные килограммы.'],
        ['Какую рыбу запрещено ловить', '    Под запретом в Астраханской области находятся следующие виды рыб:\n\n       •   осетровые;\n\n       •   Сельдь;\n\n       •   Рыбец;\n\n       •   Налим;\n\n       •   Усач.\n\n    Если рыбака поймают с таким уловом, то неприятностей ему не избежать.\n\n    Также действует запрет на перевозку и вывоз из региона рыбы определенных размеров:\n\n       •   Вобла, плотва. Рыба в длину не должна превышать 17 см.\n\n       •   Линь, чехонь – отлов рыбы производится при размере от 22 см.\n\n       •   Сом должен достигнуть в длину 60 см, иначе отлов запрещен.\n\n       •   Лещ. Рыба должна достигать 24 см.\n\n       •   Щука. Эту благородную рыбу можно ловить размером не более 32 см.\n\n       •   Сазан. Отлов рыбы можно производить, когда особь достигнет длины, как минимум, 40 см.\n\n       •   Рак. Нельзя ловить особей меньше 10 см.\n\n    За нарушение предусмотрена и административная, и уголовная ответственность. Нарушителям придется не только оплатить крупный штраф за запрещенные экземпляры, но и можно получить наказание, которое придется отбывать в местах лишения свободы.'],
        ['Размер штрафа за ловлю рыбы', '    При выборе дислокации для рыбалки, в каком бы районе она не находилась, необходимо предварительно уточнять информацию, где и когда возможно закинуть удочку. Незнание закона не поможет избежать наказания. А за некоторые нарушения можно получить довольно внушительный штраф. Не забывают и об уголовной ответственности. За нарушение правил вылова рыбы, размеры и суммы зависят от вида и редкости улова:\n\n       •   При нарушении запрета на вылов, штраф до 5 тыс. руб. При этом конфискуют удочки и другие средства лова.\n\n       •   При обнаружении в улове рыбака редкого или исчезающего вида рыб, ему грозит штраф до 1500 руб. и изъятие всех снастей.\n\n       •   При осуществлении лова рыбы в период нереста, это будет стоить рыболову от 100 до 300 тыс. руб.\n\n    Применение запрещенного вида орудия во время рыбалки в нерест и причинение крупного вреда заставит браконьера заплатить штраф в размере 300 тыс. руб.\n\n    Уголовная ответственность идет за браконьерские действия в крупных водоемах в период нереста с применением моторной лодки или яхты. Также, подобное поведение грозит рыбакам штрафом в размере 500 тыс. руб. или сроком до 2 лет лишения свободы. Отлов рыбы, занесенной в Красную книгу, запрещен. Это грозит браконьеру штрафом в районе 1 млн руб. или 3 годами тюрьмы.'],
        ['Когда можно оплатить штраф и где', '    В случае нарушения закона заполняют протокол и обозначают сумму штрафа, в зависимости от нарушения нарушителю предоставляют 10 суток для оплаты или, в случае несогласия, можно обратиться в суд, обжаловать решение. Но необходимо иметь существенные доказательства невиновности. Если в течение 5 месяцев не производится оплата штрафа, дело передается судебным приставам. В этом случае с гражданина взимается назначенная сумма в принудительном порядке.']
    ]

    def click_on_pre(self):
        Data.number_rule = Data.number_rule - 1
        if Data.number_rule < 0:
            Data.number_rule = 7
        self.parent.get_screen('RuleFishing').ids.zag.text = self.parent.get_screen('RuleFishing').data[Data.number_rule][0]
        self.parent.get_screen('RuleFishing').ids.main_text.text = self.parent.get_screen('RuleFishing').data[Data.number_rule][1]
        self.parent.current = 'RuleFishing'

    def click_on_menu(self):
        Data.screen_history.append('RuleFishing')
        self.parent.current = 'Rules'

    def click_on_next(self):
        Data.number_rule = Data.number_rule + 1
        if Data.number_rule > 7:
            Data.number_rule = 0
        self.parent.get_screen('RuleFishing').ids.zag.text = self.parent.get_screen('RuleFishing').data[Data.number_rule][0]
        self.parent.get_screen('RuleFishing').ids.main_text.text = self.parent.get_screen('RuleFishing').data[Data.number_rule][1]
        self.parent.current = 'RuleFishing'

class Penalties(Screen):
    def click_on_state256(self):
        Data.number_penalties = 0
        self.parent.get_screen('PenaltieList').ids.zag.text = self.parent.get_screen('PenaltieList').data[Data.number_penalties][0]
        self.parent.get_screen('PenaltieList').ids.main_text.text = self.parent.get_screen('PenaltieList').data[Data.number_penalties][1]
        Data.screen_history.append('Penalties')
        self.parent.current = 'PenaltieList'

    def click_on_state258(self):
        Data.number_penalties = 1
        self.parent.get_screen('PenaltieList').ids.zag.text = self.parent.get_screen('PenaltieList').data[Data.number_penalties][0]
        self.parent.get_screen('PenaltieList').ids.main_text.text = self.parent.get_screen('PenaltieList').data[Data.number_penalties][1]
        Data.screen_history.append('Penalties')
        self.parent.current = 'PenaltieList'

    def click_on_state258_1(self):
        Data.number_penalties = 2
        self.parent.get_screen('PenaltieList').ids.zag.text = self.parent.get_screen('PenaltieList').data[Data.number_penalties][0]
        self.parent.get_screen('PenaltieList').ids.main_text.text = self.parent.get_screen('PenaltieList').data[Data.number_penalties][1]
        Data.screen_history.append('Penalties')
        self.parent.current = 'PenaltieList'

    def click_on_state11_7(self):
        Data.number_penalties = 3
        self.parent.get_screen('PenaltieList').ids.zag.text = self.parent.get_screen('PenaltieList').data[Data.number_penalties][0]
        self.parent.get_screen('PenaltieList').ids.main_text.text = self.parent.get_screen('PenaltieList').data[Data.number_penalties][1]
        Data.screen_history.append('Penalties')
        self.parent.current = 'PenaltieList'

    def click_on_state11_8(self):
        Data.number_penalties = 4
        self.parent.get_screen('PenaltieList').ids.zag.text = self.parent.get_screen('PenaltieList').data[Data.number_penalties][0]
        self.parent.get_screen('PenaltieList').ids.main_text.text = self.parent.get_screen('PenaltieList').data[Data.number_penalties][1]
        Data.screen_history.append('Penalties')
        self.parent.current = 'PenaltieList'

    def click_on_state11_8_1(self):
        Data.number_penalties = 5
        self.parent.get_screen('PenaltieList').ids.zag.text = self.parent.get_screen('PenaltieList').data[Data.number_penalties][0]
        self.parent.get_screen('PenaltieList').ids.main_text.text = self.parent.get_screen('PenaltieList').data[Data.number_penalties][1]
        Data.screen_history.append('Penalties')
        self.parent.current = 'PenaltieList'

    def click_on_state11_10(self):
        Data.number_penalties = 6
        self.parent.get_screen('PenaltieList').ids.zag.text = self.parent.get_screen('PenaltieList').data[Data.number_penalties][0]
        self.parent.get_screen('PenaltieList').ids.main_text.text = self.parent.get_screen('PenaltieList').data[Data.number_penalties][1]
        Data.screen_history.append('Penalties')
        self.parent.current = 'PenaltieList'

    def click_on_state8_33(self):
        Data.number_penalties = 7
        self.parent.get_screen('PenaltieList').ids.zag.text = self.parent.get_screen('PenaltieList').data[Data.number_penalties][0]
        self.parent.get_screen('PenaltieList').ids.main_text.text = self.parent.get_screen('PenaltieList').data[Data.number_penalties][1]
        Data.screen_history.append('Penalties')
        self.parent.current = 'PenaltieList'

    def click_on_state8_35(self):
        Data.number_penalties = 8
        self.parent.get_screen('PenaltieList').ids.zag.text = self.parent.get_screen('PenaltieList').data[Data.number_penalties][0]
        self.parent.get_screen('PenaltieList').ids.main_text.text = self.parent.get_screen('PenaltieList').data[Data.number_penalties][1]
        Data.screen_history.append('Penalties')
        self.parent.current = 'PenaltieList'

    def click_on_state8_37(self):
        Data.number_penalties = 9
        self.parent.get_screen('PenaltieList').ids.zag.text = self.parent.get_screen('PenaltieList').data[Data.number_penalties][0]
        self.parent.get_screen('PenaltieList').ids.main_text.text = self.parent.get_screen('PenaltieList').data[Data.number_penalties][1]
        Data.screen_history.append('Penalties')
        self.parent.current = 'PenaltieList'

    def click_on_state20_25(self):
        Data.number_penalties = 10
        self.parent.get_screen('PenaltieList').ids.zag.text = self.parent.get_screen('PenaltieList').data[Data.number_penalties][0]
        self.parent.get_screen('PenaltieList').ids.main_text.text = self.parent.get_screen('PenaltieList').data[Data.number_penalties][1]
        Data.screen_history.append('Penalties')
        self.parent.current = 'PenaltieList'

    def click_on_state18_2(self):
        Data.number_penalties = 11
        self.parent.get_screen('PenaltieList').ids.zag.text = self.parent.get_screen('PenaltieList').data[Data.number_penalties][0]
        self.parent.get_screen('PenaltieList').ids.main_text.text = self.parent.get_screen('PenaltieList').data[Data.number_penalties][1]
        Data.screen_history.append('Penalties')
        self.parent.current = 'PenaltieList'

    def click_on_state18_3(self):
        Data.number_penalties = 12
        self.parent.get_screen('PenaltieList').ids.zag.text = self.parent.get_screen('PenaltieList').data[Data.number_penalties][0]
        self.parent.get_screen('PenaltieList').ids.main_text.text = self.parent.get_screen('PenaltieList').data[Data.number_penalties][1]
        Data.screen_history.append('Penalties')
        self.parent.current = 'PenaltieList'

    def click_on_state18_7(self):
        Data.number_penalties = 13
        self.parent.get_screen('PenaltieList').ids.zag.text = self.parent.get_screen('PenaltieList').data[Data.number_penalties][0]
        self.parent.get_screen('PenaltieList').ids.main_text.text = self.parent.get_screen('PenaltieList').data[Data.number_penalties][1]
        Data.screen_history.append('Penalties')
        self.parent.current = 'PenaltieList'

class PenaltieList(Screen):
    zag = ObjectProperty()
    main_text = ObjectProperty()

    data = [
    ['Статья 256 УК РФ. Незаконная добыча (вылов) водных биологических ресурсов', '    1. Незаконная добыча (вылов) водных биологических ресурсов (за исключением водных биологических ресурсов континентального шельфа Российской Федерации и исключительной экономической зоны Российской Федерации), если это деяние совершено:\n\n       а) с причинением крупного ущерба;\n\n       б) с применением самоходного транспортного плавающего средства или взрывчатых и химических веществ, электротока или других запрещенных орудий и способов массового истребления водных биологических ресурсов;\n\n       в) в местах нереста или на миграционных путях к ним;\n\n       г) на особо охраняемых природных территориях либо в зоне экологического бедствия или в зоне чрезвычайной экологической ситуации, -\n\n    наказывается штрафом в размере от трехсот тысяч до пятисот тысяч рублей или в размере заработной платы или иного дохода осужденного за период от двух до трех лет, либо обязательными работами на срок до четырехсот восьмидесяти часов, либо исправительными работами на срок до двух лет, либо лишением свободы на тот же срок.\n\n    2. Незаконная добыча котиков, морских бобров или других морских млекопитающих в открытом море или в запретных зонах -\n\n    наказывается штрафом в размере от трехсот тысяч до пятисот тысяч рублей или в размере заработной платы или иного дохода осужденного за период от двух до трех лет, либо обязательными работами на срок до четырехсот восьмидесяти часов, либо исправительными работами на срок до двух лет, либо лишением свободы на тот же срок.\n\n    3. Деяния, предусмотренные частями первой или второй настоящей статьи, совершенные лицом с использованием своего служебного положения либо группой лиц по предварительному сговору или организованной группой либо причинившие особо крупный ущерб, -\n\n    наказываются штрафом в размере от пятисот тысяч до одного миллиона рублей или в размере заработной платы или иного дохода осужденного за период от трех до пяти лет либо лишением свободы на срок от двух до пяти лет с лишением права занимать определенные должности или заниматься определенной деятельностью на срок до трех лет или без такового.\n\n    Примечание. Крупным ущербом в настоящей статье признается ущерб, причиненный водным биологическим ресурсам, исчисленный по утвержденным Правительством Российской Федерации таксам, превышающий сто тысяч рублей, особо крупным - двести пятьдесят тысяч рублей.'],
    ['Статья 258 УК РФ. Незаконная охота', '    1. Незаконная охота, если это деяние совершено:\n\n       а) с причинением крупного ущерба;\n\n       б) с применением механического транспортного средства или воздушного судна, взрывчатых веществ, газов или иных способов массового уничтожения птиц и зверей;\n\n       в) в отношении птиц и зверей, охота на которых полностью запрещена;\n\n       г) на особо охраняемой природной территории либо в зоне экологического бедствия или в зоне чрезвычайной экологической ситуации, -\n\n    наказывается штрафом в размере до пятисот тысяч рублей или в размере заработной платы или иного дохода осужденного за период до двух лет, либо исправительными работами на срок до двух лет, либо лишением свободы на срок до двух лет.\n\n    2. То же деяние, совершенное лицом с использованием своего служебного положения либо группой лиц по предварительному сговору или организованной группой, либо причинившее особо крупный ущерб, -\n\n    наказывается штрафом в размере от пятисот тысяч до одного миллиона рублей или в размере заработной платы или иного дохода осужденного за период от трех до пяти лет либо лишением свободы на срок от трех до пяти лет с лишением права занимать определенные должности или заниматься определенной деятельностью на срок до трех лет или без такового.\n\n    Примечание. Крупным ущербом в настоящей статье признается ущерб, исчисленный по утвержденным Правительством Российской Федерации таксам и методике, превышающий сорок тысяч рублей, особо крупным - сто двадцать тысяч рублей. '],
    ['Статья 258.1 УК РФ. Незаконные добыча и оборот особо ценных диких животных и водных биологических ресурсов', '\n\n    1. Незаконные добыча, содержание, приобретение, хранение, перевозка, пересылка и продажа особо ценных диких животных и водных биологических ресурсов, принадлежащих к видам, занесенным в Красную книгу Российской Федерации и (или) охраняемым международными договорами Российской Федерации, их частей и дериватов (производных) -\n\n    наказываются обязательными работами на срок до четырехсот восьмидесяти часов, либо исправительными работами на срок до двух лет, либо принудительными работами на срок до четырех лет со штрафом в размере до одного миллиона рублей или в размере заработной платы или иного дохода осужденного за период до двух лет или без такового и с ограничением свободы на срок до одного года или без такового, либо лишением свободы на срок до четырех лет со штрафом в размере до одного миллиона рублей или в размере заработной платы или иного дохода осужденного за период до двух лет или без такового и с ограничением свободы на срок до одного года или без такового.\n\n    1.1. Незаконные приобретение или продажа особо ценных диких животных и водных биологических ресурсов, принадлежащих к видам, занесенным в Красную книгу Российской Федерации и (или) охраняемым международными договорами Российской Федерации, их частей и дериватов (производных) с использованием средств массовой информации либо электронных или информационно-телекоммуникационных сетей, в том числе сети "Интернет", -\n\n    наказываются принудительными работами на срок до пяти лет со штрафом в размере от пятисот тысяч до одного миллиона пятисот тысяч рублей или в размере заработной платы или иного дохода осужденного за период от одного года до трех лет или без такового и с ограничением свободы на срок до двух лет или без такового либо лишением свободы на срок до пяти лет со штрафом в размере от пятисот тысяч до одного миллиона пятисот тысяч рублей или в размере заработной платы или иного дохода осужденного за период от одного года до трех лет или без такового и с ограничением свободы на срок до двух лет или без такового.\n\n    2. Деяния, предусмотренные частью первой настоящей статьи, совершенные:\n\n       а) лицом с использованием своего служебного положения;\n\n       б) с публичной демонстрацией, в том числе в средствах массовой информации или информационно-телекоммуникационных сетях (включая сеть "Интернет"), -\n\n    наказываются лишением свободы на срок до шести лет со штрафом в размере до двух миллионов рублей или в размере заработной платы или иного дохода осужденного за период до пяти лет или без такового и с лишением права занимать определенные должности или заниматься определенной деятельностью на срок до трех лет или без такового.\n\n    2.1. Деяния, предусмотренные частью первой настоящей статьи, совершенные лицом с использованием своего служебного положения, -\n\n    наказываются лишением свободы на срок от трех до семи лет со штрафом в размере от одного миллиона до трех миллионов рублей или в размере заработной платы или иного дохода осужденного за период от трех до пяти лет или без такового и с лишением права занимать определенные должности или заниматься определенной деятельностью на срок до пяти лет или без такового.\n\n    3. Деяния, предусмотренные частями первой или второй настоящей статьи, совершенные группой лиц по предварительному сговору или организованной группой, -\n\n    наказываются лишением свободы на срок от пяти до восьми лет со штрафом в размере до двух миллионов рублей или в размере заработной платы или иного дохода осужденного за период до пяти лет или без такового, с ограничением свободы на срок до двух лет или без такового и с лишением права занимать определенные должности или заниматься определенной деятельностью на срок до пяти лет или без такового.\n\n    3.1. Деяния, предусмотренные частями первой или второй настоящей статьи, совершенные группой лиц по предварительному сговору или организованной группой, -\n\n    наказываются лишением свободы на срок от шести до девяти лет со штрафом в размере от одного миллиона пятисот тысяч до трех миллионов рублей или в размере заработной платы или иного дохода осужденного за период от трех до пяти лет или без такового, с ограничением свободы на срок до двух лет или без такового и с лишением права занимать определенные должности или заниматься определенной деятельностью на срок до семи лет или без такового.'],
    ['Статья 11.7. Нарушение правил плавания', '    1. Нарушение судоводителем или иным лицом, управляющим судном (за исключением маломерного) на морском, внутреннем водном транспорте, правил плавания и стоянки судов, входа судов в порт и выхода их из порта, за исключением случаев, предусмотренных частью 3 настоящей статьи, буксировки составов и плотов, подачи звуковых и световых сигналов, несения судовых огней и знаков -\n\n    влечет наложение административного штрафа в размере от пяти тысяч до десяти тысяч рублей или лишение права управления судном на срок от шести месяцев до одного года.\n\n       1.1. Повторное в течение года совершение административного правонарушения, предусмотренного частью 1 настоящей статьи, -\n\n    влечет наложение административного штрафа в размере от десяти тысяч до двадцати тысяч рублей или лишение права управления судном на срок от одного года до двух лет.\n\n    2. Превышение судоводителем или иным лицом, управляющим маломерным судном, установленной скорости, несоблюдение требований навигационных знаков, преднамеренная остановка или стоянка судна в запрещенных местах либо нарушение правил маневрирования, подачи звуковых сигналов, несения бортовых огней и знаков -\n\n    влечет предупреждение, или наложение административного штрафа в размере от пятисот до одной тысячи рублей, или лишение права управления маломерным судном на срок до шести месяцев.\n\n    3. Осуществление капитаном судна плавания без лоцмана в районах обязательной лоцманской проводки судов, за исключением случаев, если судно относится к категории судов, освобождаемых от обязательной лоцманской проводки, или капитану судна предоставлено право осуществлять плавание без лоцмана капитаном морского порта в установленном порядке, -\n\n    влечет наложение административного штрафа в размере от двадцати тысяч до двадцати пяти тысяч рублей или лишение права управления судном на срок до трех месяцев.\n\n    4. Необъявление или неправильное объявление капитаном судна лоцману данных об осадке, о длине, ширине и вместимости судна и иных данных о судне, которые необходимы лоцману для осуществления лоцманской проводки судна, -\n\n    влечет наложение административного штрафа в размере от одной тысячи до трех тысяч рублей или лишение права управления судном на срок до трех месяцев.\n\n    Примечание. Под маломерным судном в настоящем Кодексе следует понимать судно, длина которого не должна превышать двадцать метров и общее количество людей, на котором не должно превышать двенадцать.'],
    ['Статья 11.8. Нарушение правил эксплуатации судов, а также управление судном лицом, не имеющим права управления', '    1. Управление судном (в том числе маломерным, подлежащим государственной регистрации), не прошедшим технического осмотра (освидетельствования), либо не несущим бортовых номеров или обозначений, либо переоборудованным без соответствующего разрешения или с нарушением норм пассажировместимости, ограничений по району и условиям плавания, за исключением случаев, предусмотренных частью 3 настоящей статьи, -\n\n    влечет наложение административного штрафа в размере от пяти тысяч до десяти тысяч рублей.\n\n    2. Управление судном лицом, не имеющим права управления этим судном, или передача управления судном лицу, не имеющему права управления, -\n\n    влечет наложение административного штрафа в размере от десяти тысяч до пятнадцати тысяч рублей.\n\n    3. Управление судном (в том числе маломерным, подлежащим государственной регистрации), не зарегистрированным в установленном порядке либо имеющим неисправности, с которыми запрещена его эксплуатация, -\n\n    влечет наложение административного штрафа в размере от пятнадцати тысяч до двадцати тысяч рублей. '],
    ['Статья 11.8.1. Управление маломерным судном судоводителем, не имеющим при себе документов, необходимых для допуска к управлению маломерным судном', '    1. Управление маломерным судном судоводителем, не имеющим при себе удостоверения на право управления маломерным судном, судового билета маломерного судна или его копии, заверенной в установленном порядке, а равно документов, подтверждающих право владения, пользования или распоряжения управляемым им судном в отсутствие владельца, -\n\n    влечет предупреждение или наложение административного штрафа в размере ста рублей.\n\n    За совершение данного правонарушения в соответствии со статьей 27.13 настоящего Кодекса применяется задержание транспортного средства, помещение на специализированную стоянку\n\n    2. Передача управления маломерным судном лицу, не имеющему при себе удостоверения на право управления маломерным судном, -\n\n    влечет предупреждение или наложение административного штрафа в размере ста рублей.'],
    ['Статья 11.10. Нарушение правил обеспечения безопасности пассажиров на судах водного транспорта, а также на маломерных судах', '    Нарушение правил обеспечения безопасности пассажиров при посадке на суда, в пути следования и при их высадке с судов водного транспорта либо с маломерных судов -\n\n    влечет наложение административного штрафа на граждан в размере от трехсот до пятисот рублей; на должностных лиц - от пятисот до одной тысячи рублей.'],
    ['Статья 8.33. Нарушение правил охраны среды обитания или путей миграции объектов животного мира и водных биологических ресурсов', '    Нарушение правил охраны среды обитания или путей миграции объектов животного мира и водных биологических ресурсов -\n\n    влечет предупреждение или наложение административного штрафа на граждан в размере от двух тысяч до пяти тысяч рублей; на должностных лиц - от пяти тысяч до десяти тысяч рублей; на юридических лиц - от десяти тысяч до пятнадцати тысяч рублей. '],
    ['Статья 8.35. Уничтожение редких и находящихся под угрозой исчезновения видов животных или растений', '    Уничтожение редких и находящихся под угрозой исчезновения видов животных или растений, занесенных в Красную книгу Российской Федерации либо охраняемых международными договорами, а равно действия (бездействие), которые могут привести к гибели, сокращению численности либо нарушению среды обитания этих животных или к гибели таких растений, либо добыча, хранение, перевозка, сбор, содержание, приобретение, продажа либо пересылка указанных животных или растений, их продуктов, частей либо дериватов без надлежащего на то разрешения или с нарушением условий, предусмотренных разрешением, либо с нарушением иного установленного порядка, если эти действия не содержат уголовно наказуемого деяния, -\n\n    влечет наложение административного штрафа на граждан в размере от двух тысяч пятисот до пяти тысяч рублей с конфискацией орудий добычи животных или растений, а также самих животных или растений, их продуктов, частей либо дериватов или без таковой; на должностных лиц - от пятнадцати тысяч до двадцати тысяч рублей с конфискацией орудий добычи животных или растений, а также самих животных или растений, их продуктов, частей либо дериватов или без таковой; на юридических лиц - от пятисот тысяч до одного миллиона рублей с конфискацией орудий добычи животных или растений, а также самих животных или растений, их продуктов, частей либо дериватов или без таковой.'],
    ['Статья 8.37. Нарушение правил охоты, правил, регламентирующих рыболовство и другие виды пользования объектами животного мира', '    1. Нарушение правил охоты, за исключением случаев, предусмотренных частями 1.2, 1.3 настоящей статьи, -\n\n    влечет наложение административного штрафа на граждан в размере от пятисот до четырех тысяч рублей с конфискацией орудий охоты или без таковой или лишение права осуществлять охоту на срок до двух лет; на должностных лиц - от двадцати тысяч до тридцати пяти тысяч рублей с конфискацией орудий охоты или без таковой.\n\n       1.1. Повторное в течение года совершение административного правонарушения, предусмотренного частью 1 настоящей статьи, -\n\n    влечет наложение административного штрафа на граждан в размере от 4 000 до 5 000 рублей с конфискацией орудий охоты или без таковой или лишение права осуществлять охоту на срок от одного года до трех лет; на должностных лиц - от тридцати пяти тысяч до пятидесяти тысяч рублей с конфискацией орудий охоты или без таковой.\n\n    1.2. Осуществление охоты с нарушением установленных правилами охоты сроков охоты, за исключением случаев, если допускается осуществление охоты вне установленных сроков, либо осуществление охоты недопустимыми для использования орудиями охоты или способами охоты -\n\n    влечет для граждан лишение права осуществлять охоту на срок от одного года до двух лет; наложение административного штрафа на должностных лиц в размере от тридцати пяти тысяч до пятидесяти тысяч рублей с конфискацией орудий охоты или без таковой.\n\n       1.3. Непредъявление по требованию должностных лиц органов, уполномоченных в области охраны, контроля и регулирования использования объектов животного мира (в том числе отнесенных к охотничьим ресурсам) и среды их обитания, органов, осуществляющих функции по контролю в области организации и функционирования особо охраняемых природных территорий федерального значения, государственных учреждений, находящихся в ведении органов исполнительной власти субъектов Российской Федерации, осуществляющих государственный охотничий надзор, функции по охране, контролю и регулированию использования объектов животного мира и среды их обитания, других уполномоченных в соответствии с законодательством Российской Федерации должностных лиц, производственных охотничьих инспекторов охотничьего билета, разрешения на добычу охотничьих ресурсов, путевки либо разрешения на хранение и ношение охотничьего оружия в случае осуществления охоты с охотничьим огнестрельным и (или) пневматическим оружием -\n\n    влечет для граждан лишение права осуществлять охоту на срок от одного года до двух лет; наложение административного штрафа на должностных лиц в размере от двадцати пяти тысяч до сорока тысяч рублей с конфискацией орудий охоты или без таковой.\n\n    2. Нарушение правил, регламентирующих рыболовство, за исключением случаев, предусмотренных частью 2 статьи 8.17 настоящего Кодекса, -\n\n    влечет наложение административного штрафа на граждан в размере от двух тысяч до пяти тысяч рублей с конфискацией судна и других орудий добычи (вылова) водных биологических ресурсов или без таковой; на должностных лиц - от двадцати тысяч до тридцати тысяч рублей с конфискацией судна и других орудий добычи (вылова) водных биологических ресурсов или без таковой; на юридических лиц - от ста тысяч до двухсот тысяч рублей с конфискацией судна и других орудий добычи (вылова) водных биологических ресурсов или без таковой.\n\n    3. Нарушение правил пользования объектами животного мира, за исключением случаев, предусмотренных частями 1 - 2 настоящей статьи, -\n\n    влечет наложение административного штрафа на граждан в размере от пятисот до одной тысячи рублей с конфискацией орудий добывания животных или без таковой; на должностных лиц - от двух тысяч пятисот до пяти тысяч рублей с конфискацией орудий добывания животных или без таковой; на юридических лиц - от пятидесяти тысяч до ста тысяч рублей с конфискацией орудий добывания животных или без таковой. '],
    ['Статья 20.25. Уклонение от исполнения административного наказания', '    1. Неуплата административного штрафа в срок, предусмотренный настоящим Кодексом, -\n\n    влечет наложение административного штрафа в двукратном размере суммы неуплаченного административного штрафа, но не менее одной тысячи рублей, либо административный арест на срок до пятнадцати суток, либо обязательные работы на срок до пятидесяти часов.\n\n    2. Самовольное оставление места отбывания административного ареста или уклонение от отбывания административного ареста-влечет административный арест на срок до пятнадцати суток либо обязательные работы на срок до пятидесяти часов.\n\n    3. Уклонение иностранного гражданина или лица без гражданства от исполнения административного наказания в виде административного выдворения за пределы Российской Федерации в форме контролируемого самостоятельного выезда из Российской Федерации -\n\n    влечет наложение административного штрафа в размере от трех тысяч до пяти тысяч рублей и административное выдворение за пределы Российской Федерации.\n\n    4. Уклонение от отбывания обязательных работ -\n\n    влечет наложение административного штрафа в размере от ста пятидесяти тысяч до трехсот тысяч рублей или административный арест на срок до пятнадцати суток.\n\n    5. Нарушение административного запрета на посещение мест проведения официальных спортивных соревнований в дни их проведения -\n\n    влечет наложение административного штрафа в размере от сорока тысяч до пятидесяти тысяч рублей или административный арест на срок от десяти до пятнадцати суток.\n\n    Примечания:\n\n       1. К административной ответственности за совершение административного правонарушения, предусмотренного частью 1 настоящей статьи, не привлекаются иностранные граждане и лица без гражданства в случае, если они своевременно не уплатили административный штраф, который был назначен им одновременно с административным выдворением за пределы Российской Федерации.\n\n       2. Административное выдворение за пределы Российской Федерации иностранного гражданина или лица без гражданства в форме контролируемого самостоятельного выезда из Российской Федерации не применяется к иностранным гражданам и лицам без гражданства, привлекаемым к административной ответственности за административное правонарушение, предусмотренное частью 3 настоящей статьи.\n\n       3. Административный арест, предусмотренный частью 1 настоящей статьи, не может применяться к лицу, которое не уплатило административный штраф за совершение административного правонарушения, предусмотренного главой 12 настоящего Кодекса и зафиксированного с применением работающих в автоматическом режиме специальных технических средств, имеющих функции фото- и киносъемки, видеозаписи, или средств фото- и киносъемки, видеозаписи. '],
    ['Статья 18.2. Нарушение пограничного режима в пограничной зоне', '\n\n    1. Нарушение правил въезда (прохода) в пограничную зону, временного пребывания, передвижения лиц и (или) транспортных средств в пограничной зоне -\n\n    влечет предупреждение или наложение административного штрафа в размере от пятисот до одной тысячи рублей.\n\n       1.1. Те же действия, совершенные иностранным гражданином или лицом без гражданства, -\n\n    влекут предупреждение или наложение административного штрафа в размере от пятисот до одной тысячи рублей с административным выдворением за пределы Российской Федерации или без такового.\n\n    2. Ведение хозяйственной, промысловой или иной деятельности либо проведение массовых общественно-политических, культурных или иных мероприятий в пограничной зоне, а равно содержание или выпас скота в карантинной полосе в пределах пограничной зоны без разрешения пограничных органов либо с разрешения таких органов, но с нарушением установленного порядка ведения хозяйственной, промысловой или иной деятельности либо нарушение порядка проведения массовых общественно-политических, культурных или иных мероприятий в пограничной зоне -\n\n    влечет предупреждение или наложение административного штрафа на граждан в размере от трехсот до одной тысячи рублей; на должностных лиц - от двух тысяч до пяти тысяч рублей; на юридических лиц - от пяти тысяч до десяти тысяч рублей. '],
    ['Статья 18.3. Нарушение пограничного режима в территориальном море и во внутренних морских водах Российской Федерации', '    1. Нарушение установленных в территориальном море и во внутренних морских водах Российской Федерации, в российской части вод пограничных рек, озер и иных водных объектов правил учета, хранения, выхода из пунктов базирования и возвращения в пункты базирования, пребывания на водных объектах российских маломерных самоходных и несамоходных (надводных и подводных) судов (средств) или средств передвижения по льду -\n\n    влечет предупреждение или наложение административного штрафа на граждан в размере от пятисот до одной тысячи рублей; на должностных лиц - от двух тысяч до пяти тысяч рублей; на юридических лиц - от пяти тысяч до десяти тысяч рублей.\n\n    2. Ведение в территориальном море и во внутренних морских водах Российской Федерации, в российской части вод пограничных рек, озер и иных водных объектов промысловой, исследовательской, изыскательской и иной деятельности без разрешения (уведомления) пограничных органов либо с разрешения (с уведомлением) таких органов, но с нарушением условий такого разрешения (уведомления) -\n\n    влечет предупреждение или наложение административного штрафа на граждан в размере от трехсот до одной тысячи рублей с конфискацией орудий совершения или предмета административного правонарушения или без таковой; на должностных лиц - от двух тысяч до пяти тысяч рублей с конфискацией орудий совершения или предмета административного правонарушения или без таковой; на юридических лиц - от восьми тысяч до двенадцати тысяч рублей с конфискацией орудий совершения или предмета административного правонарушения или без таковой. '],
    ['Статья 18.7. Неповиновение законному распоряжению или требованию военнослужащего в связи с исполнением им обязанностей по охране Государственной границы Российской Федерации', '    Неповиновение законному распоряжению или требованию военнослужащего в связи с исполнением им обязанностей по охране Государственной границы Российской Федерации -\n\n    влечет наложение административного штрафа в размере от одной тысячи до одной тысячи пятисот рублей или административный арест на срок до пятнадцати суток.']
    ]

    def click_on_pre(self):
        Data.number_penalties = Data.number_penalties - 1
        if Data.number_penalties < 0:
            Data.number_penalties = 13
        self.parent.get_screen('PenaltieList').ids.zag.text = self.parent.get_screen('PenaltieList').data[Data.number_penalties][0]
        self.parent.get_screen('PenaltieList').ids.main_text.text = self.parent.get_screen('PenaltieList').data[Data.number_penalties][1]
        self.parent.current = 'PenaltieList'

    def click_on_menu(self):
        Data.screen_history.append('PenaltieList')
        self.parent.current = 'Penalties'

    def click_on_next(self):
        Data.number_penalties = Data.number_penalties + 1
        if Data.number_penalties > 13:
            Data.number_penalties = 0
        self.parent.get_screen('PenaltieList').ids.zag.text = self.parent.get_screen('PenaltieList').data[Data.number_penalties][0]
        self.parent.get_screen('PenaltieList').ids.main_text.text = self.parent.get_screen('PenaltieList').data[Data.number_penalties][1]
        self.parent.current = 'PenaltieList'

class Fish(Screen):
    fish_image = ObjectProperty()
    fish_name = StringProperty()
    fish_latin_name = StringProperty()
    fish_description = StringProperty()

    def __init__(self, **kwargs):
        super(Fish, self).__init__(**kwargs)
        
    def entering(self):
        self.data = json.loads(Data.data_fish)
        fish_data = None
        for item in self.data:
        	if item['fields']['fish_name'] == Data.fish_catalog_name:
        		fish_data = item
        		break

        self.fish_name = fish_data['fields']['fish_name']
        self.fish_latin_name = fish_data['fields']['latin_fish_name']
        self.fish_description = fish_data['fields']['fish_description'].replace('\\n', '\n')
        if not os.path.exists("pics_fish_catalog/"+self.fish_name+'.jpg'):
        	with open("pics_fish_catalog/"+self.fish_name+'.jpg', 'wb') as fh:
        		fh.write(base64.b64decode(fish_data['fields']['fish_image'][2:-1]))
        self.fish_image.source = "pics_fish_catalog/"+self.fish_name+'.jpg'

    def click_weapon(self):
        Data.fish_name = self.fish_name
        self.parent.current = 'Weapon'
        

class Weapon(Screen):
    main_text = StringProperty()

    def entering(self):
        data = json.loads(Data.data_weapons)
        desc = None
        for item in data:
            if Data.fish_name == item['fields']['weapon_fish_name']:
                desc = item['fields']['weapon_fish_description'].replace('\\n', '\n')
        if desc == None:
            Dialog('Внимание!!!', 'Орудие лова для '+Data.fish_name+' неизвестно')
            self.parent.current = 'CatalogFish'
        else:
            self.main_text = desc

class CardFish(MDCard):
    image_fish = ObjectProperty()
    fish_name = StringProperty()
    latin_fish_name = StringProperty()

    def __init__(self, dop, **kwargs):
        super(CardFish, self).__init__(**kwargs)
        self.fish_name = dop['fields']['fish_name']
        self.latin_fish_name = dop['fields']['latin_fish_name']
        if not os.path.exists('icons_fish_catalog/'+self.fish_name+'.jpg'):
            with open('icons_fish_catalog/'+self.fish_name+'.jpg', 'wb') as fh:
                fh.write(base64.b64decode(dop['fields']['fish_icon_image'][2:-1]))
        self.image_fish.source = 'icons_fish_catalog/'+self.fish_name+'.jpg'

    def click_on_fish(self):
        Data.fish_catalog_name = self.children[0].children[1].children[3].text[4:]
        APP_PROCESS.root.current = 'Fish'

class CatalogFish(Screen):
    box_content = ObjectProperty()
    search_field = ObjectProperty()
	
    def __init__(self, **kwargs):
        super(CatalogFish, self).__init__(**kwargs)
        
    def entering(self):
        self.box_content.clear_widgets()
        data = json.loads(Data.data_fish)
        for item in data:
            self.box_content.add_widget(CardFish(item))

    def changeSearch(self):
        self.box_content.clear_widgets()
        data = json.loads(Data.data_fish)
        if len(self.search_field.text) == 0:
            for item in data:
                self.box_content.add_widget(CardFish(item))
        else:
            for item in data:
                if not len(self.search_field.text) > len(item['fields']['fish_name']):
                    if item['fields']['fish_name'][:len(self.search_field.text)].lower() == self.search_field.text.lower():
                        self.box_content.add_widget(CardFish(item))
        
class Recipes(Screen):
    recipe_box = ObjectProperty()
    search_field = ObjectProperty()

    def entering(self):
        self.recipe_box.clear_widgets()
        data = json.loads(Data.data_recipe)
        for item in data:
            self.recipe_box.add_widget(OneLineListItem(text=item['fields']['recipe_name'], on_release=self.callback))

    def callback(self, obj):
        Data.recipe_name = obj.text
        self.parent.current = 'OneRecipe'

    def changeSearch(self):
        self.recipe_box.clear_widgets()
        data = json.loads(Data.data_recipe)
        if len(self.search_field.text) == 0:
            for item in data:
                self.recipe_box.add_widget(OneLineListItem(text=item['fields']['recipe_name'], on_release=self.callback))
        else:
            for item in data:
                if item['fields']['recipe_name'][:len(self.search_field.text)].lower() == self.search_field.text.lower():
                    self.recipe_box.add_widget(OneLineListItem(text=item['fields']['recipe_name'], on_release=self.callback))

class CustomMenuBlock(Screen, MDFloatLayout):
    pass

class CustomBottomSheet(Screen, MDBoxLayout):
    but_map = ObjectProperty()
    but_satellite = ObjectProperty()
    but_hybrid = ObjectProperty()

    image_allowed = ObjectProperty()
    image_disallowed = ObjectProperty()
    image_shops = ObjectProperty()

    def click_on_map(self):
        Data.map_src = True
        Data.satellite_src = False
        Data.hybrid_src = False

    def click_on_satellite(self):
        Data.satellite_src = True
        Data.map_src = False
        Data.hybrid_src = False

    def click_on_hybrid(self):
        Data.hybrid_src = True
        Data.map_src = False
        Data.satellite_src = False

class ContentMarkerAllowed(Screen):
    pass

class ContentMarkerDisAllowed(Screen):
    subInfo = StringProperty()

    def __init__(self, **kwargs):
        super(ContentMarkerDisAllowed, self).__init__(**kwargs)

        
    def entering(self):
        if Data.is_polygon:
            self.subInfo = Data.polygon_text
            Data.is_polygon = False

class ContentMarkerShops(Screen):
    pass

class CustomFishLayers(Screen):
    but_silurus = ObjectProperty()
    but_cyprinus = ObjectProperty()

class ContentMarkerSilurus(Screen):
    pass

class ContentMarkerCyprinus(Screen):
    pass

class SearchMenu(Screen):
    search_box = ObjectProperty()
    noone = None

    def open_objects(self, widg):
        counter = 0
        for item in Data.parse_list:
            if item['name'] == widg.text:
                self.noone = counter
                break
            counter += 1
        Data.search_object = Data.parse_list[self.noone]
        self.parent.current = 'GPSHelper'
        self.parent.get_screen('GPSHelper').search_object_to_map()

#define different screens
class GPSHelper(Screen):
    input_search = ObjectProperty()
    main_map = ObjectProperty()
    
    search_object = False
    
    fishing_allowed = False
    fishing_disallowed = False
    fishing_shops = False

    silurus = False
    cyprinus = False

    blinker = ObjectProperty()

    def __init__(self, **kwargs):
        super(GPSHelper, self).__init__(**kwargs)

        @mainthread
        def delayed():
            self.main_map.bind(on_touch_down=self.click_on_map)
        delayed()
        
        self.source_street = MapSource(url='https://mt1.google.com/vt/lyrs=m&x={x}&y={y}&z={z}')
        self.source_satellite = MapSource(url='https://mt1.google.com/vt/lyrs=s&x={x}&y={y}&z={z}')
        self.source_hybrid = MapSource(url='https://mt1.google.com/vt/lyrs=y&x={x}&y={y}&z={z}')

        source_fishing_allowed = 'resources/layers/fishing_allowed.geojson'
        source_fishing_disallowed = 'resources/layers/fishing_disallowed.geojson'
        source_fishing_shops = 'resources/layers/fishing_shops.geojson'
        source_silurus = 'resources/layers/silurus.geojson'
        source_cyprinus = 'resources/layers/cyprinus.geojson'
        
        self.layer_polygon_disallowed = GeoJsonMapLayer(source=source_fishing_disallowed)
        self.layer_fishing_allowed = MarkerMapLayer()
        self.layer_fishing_disallowed = MarkerMapLayer()
        self.layer_fishing_shops = MarkerMapLayer()
        self.layer_silurus = MarkerMapLayer()
        self.layer_cyprinus = MarkerMapLayer()
        self.layer_object_map = MarkerMapLayer()
        self.layer_search_object = MarkerMapLayer()

        self.layer_silurus.add_widget(MapMarker(lon=47.948970794677734, lat=46.56228323662375, source='resources/map_sign/fish.png', on_release=self.markerSilurus))
        self.layer_silurus.add_widget(MapMarker(lon=48.008880615234375, lat = 46.53253190986272, source='resources/map_sign/fish.png', on_release=self.markerSilurus))
        self.layer_silurus.add_widget(MapMarker(lon=48.03926467895508, lat = 46.52745366594394, source='resources/map_sign/fish.png', on_release=self.markerSilurus))
        self.layer_silurus.add_widget(MapMarker(lon=47.99600601196288, lat = 46.55874226707572, source='resources/map_sign/fish.png', on_release=self.markerSilurus))

        self.layer_cyprinus.add_widget(MapMarker(lon=48.013343811035156, lat = 46.481373492133784, source='resources/map_sign/fish.png', on_release=self.markerCyprinus))
        self.layer_cyprinus.add_widget(MapMarker(lon=48.02999496459961, lat=46.50193716468582, source='resources/map_sign/fish.png', on_release=self.markerCyprinus))
        self.layer_cyprinus.add_widget(MapMarker(lon=47.97025680541992, lat=46.46257575132626, source='resources/map_sign/fish.png', on_release=self.markerCyprinus))
        self.layer_cyprinus.add_widget(MapMarker(lon=47.9611587524414, lat=46.49141993572272, source='resources/map_sign/fish.png', on_release=self.markerCyprinus))
        self.layer_cyprinus.add_widget(MapMarker(lon=48.005104064941406, lat=46.409931207495845, source='resources/map_sign/fish.png', on_release=self.markerCyprinus))

        self.layer_fishing_allowed.add_widget(MapMarker(lon=47.948970794677734, lat=46.56228323662375, source='resources/map_sign/fishing_allowed_mark.png', on_release=self.markerAllowedPressed))
        self.layer_fishing_allowed.add_widget(MapMarker(lon=48.008880615234375, lat=46.53253190986272, source='resources/map_sign/fishing_allowed_mark.png', on_release=self.markerAllowedPressed))
        self.layer_fishing_allowed.add_widget(MapMarker(lon=48.03926467895508, lat=46.52745366594394, source='resources/map_sign/fishing_allowed_mark.png', on_release=self.markerAllowedPressed))
        self.layer_fishing_allowed.add_widget(MapMarker(lon=47.99600601196288, lat=46.55874226707572, source='resources/map_sign/fishing_allowed_mark.png', on_release=self.markerAllowedPressed))
        self.layer_fishing_allowed.add_widget(MapMarker(lon=48.013343811035156, lat=46.481373492133784, source='resources/map_sign/fishing_allowed_mark.png', on_release=self.markerAllowedPressed))
        self.layer_fishing_allowed.add_widget(MapMarker(lon=48.02999496459961, lat=46.50193716468582, source='resources/map_sign/fishing_allowed_mark.png', on_release=self.markerAllowedPressed))
        self.layer_fishing_allowed.add_widget(MapMarker(lon=47.97025680541992, lat=46.46257575132626, source='resources/map_sign/fishing_allowed_mark.png', on_release=self.markerAllowedPressed))
        self.layer_fishing_allowed.add_widget(MapMarker(lon=47.9611587524414, lat=46.49141993572272, source='resources/map_sign/fishing_allowed_mark.png', on_release=self.markerAllowedPressed))
        self.layer_fishing_allowed.add_widget(MapMarker(lon=48.005104064941406, lat=46.409931207495845, source='resources/map_sign/fishing_allowed_mark.png', on_release=self.markerAllowedPressed))

        self.layer_fishing_disallowed.add_widget(MapMarker(lon=47.95463562011719, lat=46.528162286622035, source='resources/map_sign/fishing_disallowed_mark.png', on_release=self.markerDisAllowedPressed))
        self.layer_fishing_disallowed.add_widget(MapMarker(lon=48.01574707031249, lat=46.527689873863785, source='resources/map_sign/fishing_disallowed_mark.png', on_release=self.markerDisAllowedPressed))
        self.layer_fishing_disallowed.add_widget(MapMarker(lon=48.01300048828125, lat=46.50264611816897, source='resources/map_sign/fishing_disallowed_mark.png', on_release=self.markerDisAllowedPressed))
        self.layer_fishing_disallowed.add_widget(MapMarker(lon=47.99171447753906, lat=46.49177448218621, source='resources/map_sign/fishing_disallowed_mark.png', on_release=self.markerDisAllowedPressed))
        self.layer_fishing_disallowed.add_widget(MapMarker(lon=47.97557830810547, lat=46.500519229985045, source='resources/map_sign/fishing_disallowed_mark.png', on_release=self.markerDisAllowedPressed))
        self.layer_fishing_disallowed.add_widget(MapMarker(lon=47.96424865722656, lat=46.50099187899411, source='resources/map_sign/fishing_disallowed_mark.png', on_release=self.markerDisAllowedPressed))
        self.layer_fishing_disallowed.add_widget(MapMarker(lon=47.976951599121094, lat=46.53359473803679, source='resources/map_sign/fishing_disallowed_mark.png', on_release=self.markerDisAllowedPressed))

        self.layer_fishing_shops.add_widget(MapMarker(lon=47.99520134925842, lat=46.46676590440685, source='resources/map_sign/fishing_shops_mark.png', on_release=self.markerShopsPressed))
        self.layer_fishing_shops.add_widget(MapMarker(lon=48.03745687007904, lat=46.4956595690788, source='resources/map_sign/fishing_shops_mark.png', on_release=self.markerShopsPressed))
        self.layer_fishing_shops.add_widget(MapMarker(lon=48.069820404052734, lat=46.36908189730966, source='resources/map_sign/fishing_shops_mark.png', on_release=self.markerShopsPressed))
        self.layer_fishing_shops.add_widget(MapMarker(lon=48.03526818752289, lat=46.32747782427445, source='resources/map_sign/fishing_shops_mark.png', on_release=self.markerShopsPressed))

    def search_object_to_map(self):
    	if self.search_object:
    		self.main_map.remove_layer(self.layer_search_object)
    		self.search_object = False
    	self.layer_search_object.add_widget(MapMarker(lon=Data.search_object['point']['lon'], lat=Data.search_object['point']['lat']))
    	self.main_map.center_on(Data.search_object['point']['lat'], Data.search_object['point']['lon'])
    	self.search_object = True
    	self.main_map.add_layer(self.layer_search_object)
    	self.layer_search_object.reposition()
    
    def search_mode(self):
        if self.input_search.text != '':            
            key="rucugy0894"
            locale = str(self.main_map.lat) + ',' + str(self.main_map.lon)
		
            data = json.loads(self.places_req(key,locale,self.input_search.text))
            self.input_search.text = ''
            counter = 0
            Data.parse_list = []
            for item in data['result']['items']:
                if counter < 5:
                    if 'point' in item:
                        Data.parse_list.append(item)
                        counter += 1
                else:
                    break

            self.parent.get_screen('SearchMenu').search_box.clear_widgets()
            if len(Data.parse_list) == 0:
                self.parent.get_screen('SearchMenu').search_box.add_widget(OneLineListItem(text='По вашему запросу ничего не найдено'))
            else:
                for item in Data.parse_list:
                    if 'address_name' in item:
                        self.parent.get_screen('SearchMenu').search_box.add_widget(ThreeLineListItem(text=item['name'], secondary_text=item['address_name'], tertiary_text='Показать на карте ->', on_release=self.parent.get_screen('SearchMenu').open_objects))
                    elif 'subtype_specification' in item:
                        self.parent.get_screen('SearchMenu').search_box.add_widget(ThreeLineListItem(text=item['name'], secondary_text=item['subtype_specification'], tertiary_text='Показать на карте ->', on_release=self.parent.get_screen('SearchMenu').open_objects))
                    else:
                        self.parent.get_screen('SearchMenu').search_box.add_widget(ThreeLineListItem(text=item['name'], tertiary_text='Показать на карте ->', on_release=self.parent.get_screen('SearchMenu').open_objects))
            Data.screen_history.append('GPSHelper')
            self.parent.current = 'SearchMenu'

    def places_req(self, my_key, my_locale, my_request):
        url = "https://catalog.api.2gis.com/3.0/items?q="+my_request+"&fields=items.point&radius=20000&locale=ru_RU&sort_point="+my_locale+"&key="+my_key

        payload={}
        headers = {}
        response = requests.request("GET", url, headers=headers, data=payload)
        return response.text

    def click_on_button_go_to_penalti(self):
        Data.number_rule = 1
        self.parent.get_screen('PenaltieList').ids.zag.text = self.parent.get_screen('PenaltieList').data[Data.number_rule][0]
        self.parent.get_screen('PenaltieList').ids.main_text.text = self.parent.get_screen('PenaltieList').data[Data.number_rule][1]
        Data.screen_history.append('GPSHelper')
        self.parent.current = 'PenaltieList'
        self.menu_marker_disallowed.dismiss()

    def click_on_map(self, widget, touch):
        if self.fishing_disallowed:
            if touch.is_double_tap:
                coord_click = self.main_map.get_latlon_at(touch.x, touch.y, self.main_map.zoom)
        
                coords = [(coord_click.lon, coord_click.lat)]
                with open('resources/layers/fishing_disallowed.geojson') as f:
                    data = json.load(f)
        
                featureChoosen = None
                for feature in data['features']:
                    polygon_coords = feature['geometry']['coordinates'][0]
                    path = matplotlib.path.Path(polygon_coords)
                    if path.contains_points(coords):
                        featureChoosen = feature
                        break

                if featureChoosen['properties']['name'] == None:
                    Data.polygon_text = 'Информация в базе отсутствует'
                Data.polygon_text = featureChoosen['properties']['name']
                Data.urlToPenalti = 'test'
                Data.is_polygon = True
                self.menu_marker_disallowed = MDCustomBottomSheet(screen=Factory.ContentMarkerDisAllowed())
                self.menu_marker_disallowed.open()

    def markerSilurus(self,widget):
        self.menu_marker_silurus = MDCustomBottomSheet(screen = Factory.ContentMarkerSilurus())
        self.menu_marker_silurus.open()

    def markerCyprinus(self, widget):
        self.menu_marker_cyprinus = MDCustomBottomSheet(screen = Factory.ContentMarkerCyprinus())
        self.menu_marker_cyprinus.open()

    def markerAllowedPressed(self, widget):
        self.menu_marker_allowed = MDCustomBottomSheet(screen = Factory.ContentMarkerAllowed())
        self.menu_marker_allowed.open()

    def markerDisAllowedPressed(self, widget):
        self.menu_marker_disallowed = MDCustomBottomSheet(screen = Factory.ContentMarkerDisAllowed())
        self.menu_marker_disallowed.open()

    def markerShopsPressed(self, widget):
        self.menu_marker_shops = MDCustomBottomSheet(screen = Factory.ContentMarkerShops())
        self.menu_marker_shops.open()

    def center_from_marker(self, lon, lat): 
        min_lon, max_lon, min_lat, max_lat = lon-1, lon+1, lat-1, lat+1
        radius = haversine(min_lon, min_lat, max_lon, max_lat)
        self.main_map.zoom = get_zoom_for_radius(radius, lat)

    def centering(self, layer):
        lon, lat = layer.center
        min_lon, max_lon, min_lat, max_lat = layer.bounds
        radius = haversine(min_lon, min_lat, max_lon, max_lat)
        self.main_map.zoom = get_zoom_for_radius(radius, lat)

    def click_silurus(self, widget):
        if self.silurus:
            self.silurus = False
            self.main_map.remove_layer(self.layer_silurus)
            widget.md_bg_color = (241/255, 244/255, 250/255, 1.0)
        else:
            self.silurus = True
            self.main_map.add_layer(self.layer_silurus)
            self.layer_silurus.reposition()
            widget.md_bg_color = MDApp.get_running_app().theme_cls.primary_color
        
    def click_cyprinus(self, widget):
        if self.cyprinus:
            self.cyprinus = False
            self.main_map.remove_layer(self.layer_cyprinus)
            widget.md_bg_color = (241/255, 244/255, 250/255, 1.0)
        else:
            self.cyprinus = True
            self.main_map.add_layer(self.layer_cyprinus)
            self.layer_cyprinus.reposition()
            widget.md_bg_color = MDApp.get_running_app().theme_cls.primary_color

    def click_fishing_allowed(self, widget):
        if self.fishing_allowed:
            self.fishing_allowed = False
            self.main_map.remove_layer(self.layer_fishing_allowed)
            widget.children[0].children[0].source = 'resources/map_sign/fishing_allowed_off.png'
        else:
            self.fishing_allowed = True
            self.main_map.add_layer(self.layer_fishing_allowed)
            self.layer_fishing_allowed.reposition()
            widget.children[0].children[0].source = 'resources/map_sign/fishing_allowed_on.png'

    def showObjectMap(self):
        self.layer_object_map.add_widget(MapMarker(lon=Data.object_map_lon, lat=Data.object_map_lon, source='resources/pictures/marker.png'))
        self.main_map.add_layer(self.layer_object_map)
        self.main_map.center_on(self.layer_object_map.children[0].lat, self.layer_object_map.children[0].lon)
        self.layer_object_map.reposition()

    def click_fishing_disallowed(self, widget):
        if self.fishing_disallowed:
            self.fishing_disallowed = False
            self.main_map.remove_layer(self.layer_polygon_disallowed)
            self.main_map.remove_layer(self.layer_fishing_disallowed)
            widget.children[0].children[0].source = 'resources/map_sign/fishing_disallowed_off.png'
        else:
            self.fishing_disallowed = True
            self.centering(self.layer_polygon_disallowed)
            self.main_map.add_layer(self.layer_polygon_disallowed)
            self.main_map.add_layer(self.layer_fishing_disallowed)
            self.layer_fishing_disallowed.reposition()
            widget.children[0].children[0].source = 'resources/map_sign/fishing_disallowed_on.png'

    def click_fishing_shops(self, widget):
        if self.fishing_shops:
            self.fishing_shops = False
            self.main_map.remove_layer(self.layer_fishing_shops)
            widget.children[0].children[0].source = 'resources/map_sign/fishing_shop_off.png'
        else:
            self.fishing_shops = True
            self.main_map.add_layer(self.layer_fishing_shops)
            self.layer_fishing_shops.reposition()
            widget.children[0].children[0].source = 'resources/map_sign/fishing_shop_on.png'

    def click_on_button_gps(self):
        note = XNotification(text='Это всплывающая подсказка', show_time=3, title='Подсказка jps')
        #Dialog('Вы уже на данной странице', 'Внимание!')

    def click_on_button_note(self):
        try:
            self.main_map.remove_layer(self.layer_object_map)
        except:
            pass
        self.menu_block = MDCustomBottomSheet(screen = Factory.CustomMenuBlock())
        self.menu_block.open()

    def close_menu(self):
        self.menu_block.dismiss()

    def click_on_button_plus(self):
        self.parent.current = 'News'
        Data.screen_history.append('GPSHelper')

    def click_on_button_user(self):
        Data.screen_history.append('GPSHelper')
        self.parent.current = 'User'

    def click_on_button_calendar(self):
        mn_now = datetime.date.today().month
        days_in_mon = MONTH_LIST[str(mn_now)]
        if days_in_mon == 28:
            twenty_nine_label.disabled = True
            thirty_label.disabled = True
            thirty_one_label.disabled = True
        elif days_in_mon == 30:
            thirty_one_label.disabled = True
        Data.screen_history.append('GPSHelper')

        self.parent.current = 'Calendar'

    def click_on_button_fish(self):
        self.fish_layers = MDCustomBottomSheet(screen = Factory.CustomFishLayers())
        if self.silurus:
            self.fish_layers.children[0].children[0].children[0].ids.but_silurus.md_bg_color = MDApp().get_running_app().theme_cls.primary_color
        if self.cyprinus:
            self.fish_layers.children[0].children[0].children[0].ids.but_cyprinus.md_bg_color = MDApp().get_running_app().theme_cls.primary_color
        self.fish_layers.open()

    def click_on_button_userGps(self):
        self.gps = Gps(self)
        self.gps.run()

    def click_on_button_layers(self):
        data = json.loads(Data.data_fishing_disallowed)
        with open('./template_layer.json') as file:
            template = json.load(file)
        template['features'] = data
        for item in template['features']:
            item.pop('id')
            item['geometry'] = item['geom']
            item['type'] = 'Feature'
            item.pop('geom')
            item.pop('extensions')
            item['properties'] = item['fields']
            item.pop('fields')
            item['properties'].pop('id_1')
            item['properties']["stroke"] = "#555555"
            item['properties']["stroke-width"] = 0
            item['properties']["stroke-opacity"] = 0
            item['properties']["fill"] = "#ff0000"
            item['properties']["fill-opacity"] = 0.5
        with open('./resources/layers/fishing_disallowed.geojson', 'w', encoding = 'UTF-8') as file:
            json.dump(template, file, ensure_ascii = False)
        self.layers = MDCustomBottomSheet(screen = Factory.CustomBottomSheet())
        if Data.map_src:
            self.layers.children[0].children[0].children[0].ids.but_map.md_bg_color = MDApp().get_running_app().theme_cls.primary_color
            self.layers.children[0].children[0].children[0].ids.but_satellite.md_bg_color = (241/255, 244/255, 250/255, 1.0)
            self.layers.children[0].children[0].children[0].ids.but_hybrid.md_bg_color = (241/255, 244/255, 250/255, 1.0)
        elif Data.hybrid_src:
            self.layers.children[0].children[0].children[0].ids.but_map.md_bg_color = (241/255, 244/255, 250/255, 1.0)
            self.layers.children[0].children[0].children[0].ids.but_satellite.md_bg_color = (241/255, 244/255, 250/255, 1.0)
            self.layers.children[0].children[0].children[0].ids.but_hybrid.md_bg_color = MDApp().get_running_app().theme_cls.primary_color
        elif Data.satellite_src:
            self.layers.children[0].children[0].children[0].ids.but_map.md_bg_color = (241/255, 244/255, 250/255, 1.0)
            self.layers.children[0].children[0].children[0].ids.but_satellite.md_bg_color = MDApp().get_running_app().theme_cls.primary_color
            self.layers.children[0].children[0].children[0].ids.but_hybrid.md_bg_color = (241/255, 244/255, 250/255, 1.0)
        if self.fishing_allowed:
            self.layers.children[0].children[0].children[0].ids.image_allowed.source = 'resources/map_sign/fishing_allowed_on.png'
        if self.fishing_disallowed:
            self.layers.children[0].children[0].children[0].ids.image_disallowed.source = 'resources/map_sign/fishing_disallowed_on.png'
        if self.fishing_shops:
            self.layers.children[0].children[0].children[0].ids.image_shops.source = 'resources/map_sign/fishing_shop_on.png'
        self.layers.open()

class Onboard(Screen):
    pass

class RegistrationMain(Screen):
    input_surname = ObjectProperty()
    input_name = ObjectProperty()
    input_lastname = ObjectProperty()
    input_mail = ObjectProperty()
    input_phone = ObjectProperty()

    def __init__(self, **kwargs):
        super(RegistrationMain, self).__init__(**kwargs)

    def click_on_button_privacy_policy(self):
        #Data.save_info(surname=self.input_surname.text, name=self.input_name.text, lastname=self.input_lastname.text, mail=self.input_mail.text, phone=self.input_phone.text)
        self.parent.current = 'RegistrationDop'

    def click_on_button_terms_and_agreements(self):
        #Data.save_info(surname=self.input_surname.text, name=self.input_name.text, lastname=self.input_lastname.text, mail=self.input_mail.text, phone=self.input_phone.text)
        self.parent.current = 'RegistrationDop'

    def click_on_button_enter(self):
        self.parent.current = 'Enter'

    def click_on_button_register(self):
        if self.input_surname.text == '':
            Dialog('Вы не ввели фамилию', 'Внимание!')
        else:
            if self.input_name.text == '':
                Dialog('Вы не ввели имя', 'Внимание')
            else:
                if self.input_lastname.text == '':
                    Dialog('Вы не ввели отчество', 'Внимание')
                else:
                    if self.input_mail.text == '':
                        Dialog('Вы не ввели почту', 'Внимание')
                    else:
                        if re.match('/^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[-1-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/', self.input_mail.text):
                            Dialog('Неккоректный ввод почты', 'Внимание')
                        else:
                            if self.input_phone.text == '':
                                Dialog('Вы не ввели телефон', 'Внимание')
                            else:
                                if re.match('^[7][\d]{3}[\d]{3}[\d]{2}[\d]{2}$', self.input_phone.text) == None:
                                    Dialog('Неккоректный ввод телефона, формат ввода X(XXX)XXXXXXX', 'Внимание')
                                else:
                                    self.imei = plyer.uniqueid.get_uid()
                                    url = "http://get-fishing.ru/admin/Fishing/user/add/"

                                    payload={'csrfmiddlewaretoken':'A3KuhvpzTfM7NYyTtwDsnLui9t0oCFgXwqiP0Sbw2eQyQ6znfJNT3OBkG0L0XifX', 'user_surname':self.input_surname.text, 'user_name':self.input_name.text, 'user_lastname':self.input_lastname.text, 'user_email':self.input_mail.text, 'user_phone':self.input_phone.text, 'user_imei':self.imei, '_save':'Сохранить'}
                                    payload_compaund = urllib.parse.urlencode(payload)
                                    headers = {
                                        'Content-Type': 'application/x-www-form-urlencoded',
                                        'Cookie': 'csrftoken=6xIvTxW7j9eBdibEWnkBQdhcHHVMvN9a; sessionid=qzrj47y6h5jxkl6wgc2a9s4420t9z48i'
                                    }

                                    response = requests.request("POST", url, headers=headers, data=payload_compaund)
                                    Dialog('Регистрация успешно завершена!', 'Поздравляем!')
                                    URL = 'http://get-fishing.ru/fishing/user/'
                                    Data.data_user = requests.get(URL).text
                                    self.parent.current = 'RegistrationDop'

class RegistrationDop(Screen):
    button_continue = ObjectProperty()

    def click_on_checkbox_agree(self, instance, value):
        if value:
            self.button_continue.disabled = False
        else:
            self.button_continue.disabled = True

    def click_on_back(self):
        self.parent.current = 'Onboard'

    def click_on_button_continue(self):
        self.parent.get_screen('RegistrationMain').ids.input_surname.text = Data.input_surname
        self.parent.get_screen('RegistrationMain').ids.input_name.text = Data.input_name
        self.parent.get_screen('RegistrationMain').ids.input_lastname.text = Data.input_lastname
        self.parent.get_screen('RegistrationMain').ids.input_mail.text = Data.input_mail
        self.parent.get_screen('RegistrationMain').ids.input_phone.text = str(Data.input_phone)
        self.parent.current = 'Enter'

class Enter(Screen):
    IMEI = StringProperty()

    def entering(self):
        uid = plyer.uniqueid.get_uid()
        self.IMEI = str(uid)

        data = json.loads(Data.data_user)
        res = False
        for item in data:
            if item['fields']['user_imei'] == self.IMEI:
                #message = 'Ваш код доступа для приложения: ' + str(Data.code)

                #password = 'wpjscpeqmnutvuxd'
                #msg['From'] = 'app.fishing@yandex.ru'
                #msg['To'] = self.input_mail.text

                #msg.attach(MIMEText(message, 'plain'))

                #server = smtplib.SMTP_SSL('smtp.yandex.com', 465)
                #server.login(msg['From'], password)
                #server.sendmail(msg['From'], msg['To'], msg.as_string())
                #server.quit()

                Data.screen_history.append('Enter')
                user_info.name = item['fields']['user_name']
                user_info.surname = item['fields']['user_surname']
                user_info.lastname = item['fields']['user_lastname']
                user_info.phone = item['fields']['user_phone']
                user_info.mail = item['fields']['user_email']
                res = True
                break
        if res:
            self.parent.current = 'GPSHelper'
        else:
            Dialog('Вы не зарегестрированы в приложении', 'Внимание!')
            self.parent.current = 'RegistrationMain'

class WindowManager(ScreenManager):
    pass

class MyApp(MDApp):
    window_manager = ObjectProperty()
    theme_cls = ThemeManager()
    title = 'Умная рыбалка'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        URL = 'http://get-fishing.ru/fishing/fishes/'
        Data.data_fish = requests.get(URL).text
        URL = 'http://get-fishing.ru/fishing/weapons/'
        Data.data_weapons = requests.get(URL).text
        URL = 'http://get-fishing.ru/fishing/base_chill/'
        Data.data_base_chill = requests.get(URL).text
        URL = 'http://get-fishing.ru/fishing/bait/'
        Data.data_bait = requests.get(URL).text
        URL = 'http://get-fishing.ru/fishing/buy_fish/'
        Data.data_buy_fish = requests.get(URL).text
        URL = 'http://get-fishing.ru/fishing/equipment/'
        Data.data_equipment = requests.get(URL).text
        URL = 'https://get-fishing.nextgis.com/api/resource/13/feature/?srs=4326&geom_format=geojson'
        Data.data_fishing_disallowed = requests.get(URL).text
        URL = 'http://get-fishing.ru/fishing/user/'
        Data.data_user = requests.get(URL).text
        URL = 'http://get-fishing.ru/fishing/recipes/'
        Data.data_recipe = requests.get(URL).text

        Window.bind(on_keyboard=self.android_button_click)

        @mainthread
        def delayed():
            self.load_database()
        delayed()

    def android_button_click(self,window, key, *largs):
        if key == 27:
            if not len(Data.screen_history) == 0:
                self.root.current = Data.screen_history[-1]
                Data.screen_history.pop()
            else:
                self.window_manager.current = 'Onboard'
            return True

    def load_database(self):
        conn = SQLCommander.connect("resources/DB/db.db")
        cur = conn.cursor()

        cur.execute("SELECT * FROM catalog ORDER BY name")

        allItems = cur.fetchall()
        allItems = list(allItems)

        Data.db = allItems
        #db[n][0] - id, db[n][1] - name, db[n][2] - none, db[n][3] - description, db[n][4] - pic, db[n][5] - latin, db[n][6] - gif

    def build(self):
        self.theme_cls.theme_style = "Light"
        LabelBase.register(name='Proxima Nova', fn_regular='resources/fonts/proximanova_regular.ttf')
        theme_font_styles.append('Proxima Nova')
        self.theme_cls.font_styles['Proxima Nova'] = ["Proxima Nova", 16, False, 0.15]
        from kivy.resources import resource_find
        filename = resource_find(KIVY_FILENAME) or KIVY_FILENAME
        if filename in Builder.files:
            Builder.unload_file(filename)
        return Builder.load_file(filename)

APP_PROCESS = MyApp()
APP_PROCESS.run()
