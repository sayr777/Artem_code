from kivymd.uix.toolbar import MDTopAppBar
from kivymd.app import MDApp

class SliverToolbar(MDTopAppBar):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.shadow_color = (0, 0, 0, 0)
        self.type_height = "medium"
        self.headline_text = "Новости рыбалки"
        self.left_action_items = [["arrow-left", lambda x: self.callback()]]
        self.right_action_items = [["attachment", lambda x: self.parent.parent.parent.click_on_button_go_chat()]]

    def callback(self):
        self.parent.parent.parent.parent.current = 'GPSHelper'
