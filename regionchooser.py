from kivy.uix.screenmanager import Screen
from kivy.properties import NumericProperty
import json

class RegionChooser(Screen):
    index = NumericProperty()

    def click_on_region(self, widget):
        data = None

        with open('subinfo.json') as file:
            data = json.load(file)

        data['region'] = widget.text

        with open('subinfo.json', 'w', encoding = 'UTF-8') as file:
            json.dump(data, file, ensure_ascii = False)

        self.parent.current = 'GPSHelper'
