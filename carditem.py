from kivymd.uix.card import MDCard
from kivymd.uix.behaviors import RoundedRectangularElevationBehavior
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel
from kivy.uix.image import AsyncImage
from kivy import platform

class CardItem(MDCard, RoundedRectangularElevationBehavior):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.on_release = self.callback
        self.elevation = 3
        self.size_hint_y = None
        self.height = "86dp"
        self.padding = "4dp"
        self.radius = [12, ]
        self.args = args

        img = AsyncImage()
        if args[3] == 'avatar.png':
            img.source = 'resources/news_pic/avatar.png'
        elif args[3] == 'i.webp':
            img.source = 'resources/news_pic/i.webp'
        elif args[3] == 'jp-logo.jpg':
            img.source = 'resources/news_pic/jp-logo.jpg'
        else:
            img.source = args[3]
        img.radius = self.radius
        img.size_hint_x = None
        img.width = self.height
        self.add_widget(img)

        mdbl = MDBoxLayout()
        mdbl.orientation = "vertical"
        mdbl.adaptive_height = True
        mdbl.spacing = "6dp"
        mdbl.padding = "12dp", 0, 0, 0
        mdbl.pos_hint = {"center_y": .5}

        lab_main = MDLabel()
        lab_dop = MDLabel()
        lab_main.text = args[0]
        lab_main.font_style = "H6"
        lab_main.adaptive_height = True
        lab_dop.text = args[1]
        lab_dop.font_style = "Caption"
        lab_dop.theme_text_color = "Hint"
        lab_dop.adaptive_height = True

        mdbl.add_widget(lab_main)
        mdbl.add_widget(lab_dop)
        self.add_widget(mdbl)

    def callback(self):
        if platform == 'android': #check if the app is on Android
            import jnius
            from jnius import cast
            from jnius import autoclass
            PythonActivity = autoclass('org.kivy.android.PythonActivity') #request the Kivy activity instance
            Intent = autoclass('android.content.Intent') # get the Android Intend clast
            currentActivity = cast('android.app.Activity', PythonActivity.mActivity)
            Uri = autoclass('android.net.Uri')
            uri = Uri.parse(self.args[2])
            intent = Intent(Intent.ACTION_VIEW)
            intent.setData(uri)
            currentActivity.startActivity(intent) # show the intent in the game activity
