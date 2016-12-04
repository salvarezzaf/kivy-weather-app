from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty, ListProperty  # @UnresolvedImport
from kivy.uix.listview import ListItemButton
from weatherutil import WeatherUtil
from kivy.network.urlrequest import UrlRequest
from dbutil import DbUtil
import json
import sys
import urllib


class AddLocation(BoxLayout):
    reload(sys)
    sys.setdefaultencoding('utf-8')
    search_input = ObjectProperty()
    results = ObjectProperty()
    util = DbUtil()
    cached_results = None

    args_converter = lambda self, row_index, row_data: {'text': row_data, 'size_hint_y': None, 'height': '40sp'}

    def search_query_city(self):
        not_found = ['']
        search_query = WeatherUtil.get_property_from_config_file("WeatherUrls", "SearchLocation")
        query_formatted = search_query.format(urllib.quote(self.search_input.text))
        if len(self.search_input.text) > 1:
            request = UrlRequest(query_formatted, self.display_results)
        else:
            self.results.item_strings = not_found
            self.results.disabled = True

    def display_results(self, request, data):
        data = json.loads(data.decode()) if not isinstance(data, dict) else data
        self.cached_results = data
        cities = [city['name'] for city in data['RESULTS']]
        self.results.disabled = False
        self.results.item_strings = cities
        del self.results.adapter.data[:]
        self.results.adapter.data.extend(cities)
        self.results._trigger_reset_populate


class LocationButton(ListItemButton):
    location = ListProperty()
