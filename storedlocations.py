from kivy.factory import Factory
from kivy.properties import ObjectProperty, StringProperty
from kivy.uix.boxlayout import BoxLayout

from dbutil import DbUtil


class StoredLocations(BoxLayout):
    wrapper = ObjectProperty()
    db_util = DbUtil()

    def __init__(self, **kwargs):
        super(StoredLocations, self).__init__(**kwargs)
        self.wrapper.bind(minimum_height=self.wrapper.setter('height'))

    def get_favourite_locations(self):
        location_list = self.db_util.find_all()
        for location in location_list:
                loc_widget = Factory.LocationWrapper()
                if location.isDefault:
                    loc_widget.location_name = location.location_name+" (Default)"
                    loc_widget.default_or_not = u"\uf005"
                    loc_widget.is_disabled = True
                else:
                    loc_widget.location_name = location.location_name
                    loc_widget.default_or_not = u"\uf067"

                self.wrapper.add_widget(loc_widget)


