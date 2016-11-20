from kivy.properties import StringProperty
from kivy.uix.boxlayout import BoxLayout

from dbutil import DbUtil


class AppSettings(BoxLayout):
    current_temp_unit = StringProperty()
    db_util = DbUtil()

    def get_default_tem_unit(self):
        self.current_temp_unit = self.db_util.get_default_tem_unit()

