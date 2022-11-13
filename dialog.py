from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDRoundFlatButton

class DialogTemplate(MDDialog):
    def __init__(self, **kwargs):
        super(DialogTemplate, self).__init__(**kwargs)

    def callback(self, widget):
        self.dialog.dismiss()

class Dialog(DialogTemplate):
    def __init__(self, text, title, **kwargs):
        super(Dialog, self).__init__(**kwargs)
        self.dialog = MDDialog(title=title, text=text, size_hint=[.75, .55], auto_dismiss=False, buttons=[MDRoundFlatButton(text='OK', on_release=self.callback)])
        self.dialog.open()
