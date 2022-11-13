from kivy.uix.screenmanager import Screen
from kivy.properties import StringProperty
import user_info

class ProfileDetails(Screen):
    user_name = StringProperty()
    user_surname = StringProperty()
    user_mail = StringProperty()
    user_phone = StringProperty()

    def entering(self):
        self.user_name = user_info.name
        self.user_surname = user_info.surname
        self.user_mail = user_info.mail
        self.user_phone = user_info.phone

    def click_on_name(self):
        pass

    def click_on_phone(self):
        pass

    def click_on_mail(self):
        pass
