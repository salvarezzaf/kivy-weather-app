from kivy.app import App
from kivy.properties import ObjectProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder
from kivy.utils import get_color_from_hex
from kivy.core.window import Window
from kivy.core.text import LabelBase, Label

from addlocation import AddLocation
from appsettings import AppSettings
from currentconditions import CurrentCondition
from dbutil import DbUtil
from locationforecast import LocationForecast
from storedlocations import StoredLocations
from models.models import Settings
from weatherutil import WeatherUtil

Builder.load_file("kvFiles/currentconditions.kv")
Builder.load_file("kvFiles/buttons.kv")
Builder.load_file("kvFiles/locationforecast.kv")
Builder.load_file("kvFiles/addlocation.kv")
Builder.load_file("kvFiles/storedlocations.kv")
Builder.load_file("kvFiles/appsettings.kv")


class YamaRoot(BoxLayout):
    current_conditions = ObjectProperty()
    fav_locations = ObjectProperty()
    forecast = ObjectProperty()
    add_location = ObjectProperty()
    db_util = DbUtil()

    def __init__(self, **kwargs):
        super(YamaRoot, self).__init__(**kwargs)
        self.load_startup_widget()
        self.db_util.load_default_settings_if_empty()

    def show_current_conditions(self, location):
        self.db_util.save_selected_location(location)
        self.clear_widgets()
        self.create_conditions_widget()
        self.create_forecast_widget()

    def create_conditions_widget(self):
        self.current_conditions = CurrentCondition()
        self.current_conditions.get_current_conditions()
        self.add_widget(self.current_conditions)

    def create_forecast_widget(self):
        self.forecast = LocationForecast()
        self.forecast.get_weather_forecast()
        self.add_widget(self.forecast)

    def create_add_city_widget(self):
        self.clear_widgets()
        self.add_widget(AddLocation())

    def load_startup_widget(self):
        if self.db_util.get_default() is None:
            self.create_add_city_widget()
        else:
            self.clear_widgets()
            self.create_conditions_widget()
            self.create_forecast_widget()

    def show_fav_locations(self):
        self.clear_widgets()
        self.fav_locations = StoredLocations()
        self.fav_locations.get_favourite_locations()
        self.add_widget(self.fav_locations)

    def add_as_new_default(self, location_name):
        self.db_util.remove_existing_default()
        self.db_util.set_default(location_name)
        self.show_fav_locations()

    def remove_location(self, location_name):
        self.db_util.delete_location(location_name)
        self.show_fav_locations()

    def show_app_settings(self):
        self.clear_widgets()
        self.db_util.load_default_settings_if_empty()
        settings = AppSettings()
        settings.get_default_tem_unit()
        self.add_widget(settings)

    def save_temp_setting(self, tem_unit):
        self.db_util.save_or_update_settings(tem_unit)

class YamaApp(App):

    def on_pause(self):
        return True

    def on_resume(self):
        pass

if __name__ == '__main__':
    Window.clearcolor = get_color_from_hex('#34495e')
    LabelBase.register("OpenSans", fn_regular="fonts/OpenSans-Regular.ttf")
    LabelBase.register("FontAwesome", fn_regular="fonts/fontawesome-webfont.ttf")
    DbUtil.create_db_session()
    YamaApp().run()
