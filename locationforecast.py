from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty  # @UnresolvedImport
from kivy.network.urlrequest import UrlRequest
from kivy.factory import Factory
from weatherutil import WeatherUtil
from dbutil import DbUtil


class LocationForecast(BoxLayout):
    default_location = ObjectProperty()
    wrapper = ObjectProperty()
    util = WeatherUtil()
    db_util = DbUtil()
    degree_symbol = u"\u00B0"

    def get_weather_forecast(self):
        self.default_location = self.db_util.get_default()
        forecast_url = WeatherUtil.get_property_from_config_file("WeatherUrls", "Forecast")
        forecast_url_formatted = forecast_url.format(self.default_location.location_code, self.default_location.location_name)
        request = UrlRequest(forecast_url_formatted, self.create_forecast_wrapper)

    def create_forecast_wrapper(self, request, data):
        for forecast in data['forecast']['simpleforecast']['forecastday'][1:]:
            current_forecast = Factory.DayForecastWrapper()
            current_forecast.forecast_img = self.util.get_icon_for_conditions(forecast['icon'], self.default_location.location_lat, self.default_location.location_long, True)
            current_forecast.forecast_txt = forecast['conditions']
            high_temp = str(forecast['high']['celsius'])
            low_temp = str(forecast['low']['celsius'])
            current_forecast.hilowtemps = high_temp + self.degree_symbol + "/" + low_temp + self.degree_symbol  
            current_forecast.day = forecast['date']['weekday']
            self.wrapper.add_widget(current_forecast)
