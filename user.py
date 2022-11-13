from kivy.uix.screenmanager import Screen
from kivy.properties import StringProperty
import user_info
from dialog import Dialog
from kivy import platform

class User(Screen):
    user_surname = StringProperty()
    user_name = StringProperty()

    def entering(self):
        self.user_surname = user_info.surname
        self.user_name = user_info.name

    def click_on_profile_details(self):
        self.parent.current = 'ProfileDetails'

    def click_on_note(self):
        self.parent.current = 'Notes'

    def click_on_telegram(self):
        if platform == 'android': #check if the app is on Android
            import jnius
            from jnius import cast
            from jnius import autoclass
            appName = "org.telegram.messenger"
            PythonActivity = autoclass('org.kivy.android.PythonActivity') #request the Kivy activity instance
            Intent = autoclass('android.content.Intent') # get the Android Intend clast
            String = autoclass('java.lang.String')
            currentActivity = cast('android.app.Activity', PythonActivity.mActivity)
            Context = autoclass('android.content.Context')
            pm = currentActivity.getApplicationContext().getPackageManager();
            Uri = autoclass('android.net.Uri')
            flag = False
            try:
                pm.getPackageInfo(cast('java.lang.CharSequence', String('org.telegram.messenger')), PackageManager.GET_ACTIVITIES);
                flag = True;
            except:
                flag = True;

            if flag:
                uri = Uri.parse('https://telegram.me/+ZNRNXnSbanxmZTQy')
                intent = Intent(Intent.ACTION_VIEW)
                intent.setData(uri)
                currentActivity.startActivity(intent) # show the intent in the game activity
            else:
                Dialog('Telegram не установлен', 'Внимание')
