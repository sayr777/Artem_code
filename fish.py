from kivymd.uix.card import MDCard
from kivy.properties import StringProperty

class CardFish(MDCard):
    def __init__(self, dop, **kwargs):
        super(CardFish, self).__init__(**kwargs)
        print(dop)
