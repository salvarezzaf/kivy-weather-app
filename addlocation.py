from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty  # @UnresolvedImport
from weatherutil import WeatherUtil
from kivy.network.urlrequest import UrlRequest
import json
from models.models import Location
from dbutil import DbUtil
from libs.garden.xpopup.notification import XNotification, XError

class AddLocation(BoxLayout):
    
    search_input = ObjectProperty()
    results = ObjectProperty()
    util = DbUtil()
    cached_results = None
    
    args_converter = lambda self, row_index, row_data: {'text':row_data, 'size_hint_y': None, 'height': '40sp'}
        
    def search_query_city(self):
        not_found = ['Start typing to add new city']
        search_query = WeatherUtil.get_property_from_config_file("WeatherUrls", "SearchLocation")
        query_formatted = search_query.format(self.search_input.text)
        if len(self.search_input.text) > 1:
            request = UrlRequest(query_formatted, self.display_results)
        else:
            self.results.item_strings= not_found
            self.results.disabled=True
        
    def display_results(self, request, data):
        data = json.loads(data.decode()) if not isinstance(data, dict) else data
        self.cached_results = data
        cities = [city['name'] for city in data['RESULTS']]
        self.results.disabled=False
        self.results.item_strings = cities
        self.results.adapter.bind(on_selection_change=self.save_selection)
        del self.results.adapter.data[:]
        self.results.adapter.data.extend(cities)
        self.results._trigger_reset_populate
        
    def save_selection(self, adapter):        
        
        try:
            location = adapter.selection[0].text
            selected_location=None           
            success = ["Location saved successfully"]
            
            for city in self.cached_results['RESULTS']:
                if city['name']==location:
                    format_loc_name = city['name'].split(",")
                    selected_location = Location(location_name=format_loc_name[0],location_code=city['c'],location_lat=city['lat'],location_long=city['lon'],isDefault=True)
                    if not self.util.location_exists(format_loc_name[0]):
                        self.util.remove_existing_default()
                        self.util.save(selected_location)
                        XNotification(text="Location Saved Successfully" ,show_time=1, size_hint=(0.4, 0.2),title='Saved')
                    else:
                        XNotification(text="Location already exists" ,show_time=1, size_hint=(0.4, 0.2),title='Entry exists')
                    break            
                                                                          
        except Exception:            
            XError(text="Could not add location. Try again",size_hint=(0.4, 0.2),title='Error')
            
            