from kivy.app import App
from kivy.properties import ObjectProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder
from kivy.utils import get_color_from_hex
from kivy.core.window import Window
from kivy.core.text import LabelBase
from dbutil import DbUtil
from addlocation import AddLocation

Builder.load_file("kvFiles/currentconditions.kv")
Builder.load_file("kvFiles/buttons.kv")
Builder.load_file("kvFiles/locationforecast.kv")
Builder.load_file("kvFiles/addlocation.kv")


class YamaRoot(BoxLayout):
    current_conditions = ObjectProperty()

    def show_current_conditions(self, location):
        pass


class YamaApp(App):
    pass

if __name__ == '__main__':
    Window.clearcolor = get_color_from_hex('#34495e')
    LabelBase.register("OpenSans", fn_regular="fonts/OpenSans-Regular.ttf")
    LabelBase.register("FontAwesome", fn_regular="fonts/fontawesome-webfont.ttf")
    #DbUtil.save_startup_location(DbUtil.create_db_session())
    DbUtil.create_db_session()
    YamaApp().run()
