from kivy.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty  # @UnresolvedImport
from kivy.network.urlrequest import UrlRequest
from weatherutil import WeatherUtil

class CurrentCondition(BoxLayout):
    util = WeatherUtil()
    current_location_name = StringProperty()
    current_condition_text = StringProperty()
    current_condition_img = StringProperty()
    current_temp = StringProperty()
    high_low_temps = StringProperty()
    degree_symbol = u"\u00B0"
    
    def __init__(self, **kwargs):
        super(CurrentCondition, self).__init__(**kwargs)        
        self.getCurrentConditions()
    
    def getCurrentConditions(self):
        conditions_url = self.util.get_property_from_config_file("WeatherUrls", "CurrentConditions")
        forecast_url = self.util.get_property_from_config_file("WeatherUrls", "Forecast")
        conditions_url_formatted = conditions_url.format("GB","Glasgow")
        forecast_url_formatted = forecast_url.format("GB","Glasgow")
        request = UrlRequest(conditions_url_formatted,self.parseCurrentWeatherData)
        highlowRequest = UrlRequest(forecast_url_formatted, self.parseHighLowTemperature)
    
    def parseCurrentWeatherData(self, request, data):
        location = data['current_observation']['display_location']['city']
        country = data['current_observation']['display_location']['country']
        
        self.current_location_name = location + "," + country
        self.current_condition_text = data['current_observation']['weather']
        self.current_condition_img = self.util.get_icon_for_conditions(data['current_observation']['icon'],
                                                                    data['current_observation']['display_location']['latitude'],
                                                                    data['current_observation']['display_location']['longitude'])
        self.current_temp = str(data['current_observation']['temp_c']) + self.degree_symbol
    
    def parseHighLowTemperature(self,request,data):
        high_temp = str(data['forecast']['simpleforecast']['forecastday'][0]['high']['celsius'])
        low_temp = str(data['forecast']['simpleforecast']['forecastday'][0]['low']['celsius'])
        self.high_low_temps = high_temp + self.degree_symbol + "/" +  low_temp + self.degree_symbol  
