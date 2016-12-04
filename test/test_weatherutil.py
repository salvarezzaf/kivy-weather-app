import unittest

import datetime

from freezegun import freeze_time
from mock import Mock, patch
from mock.mock import MagicMock

from app.weatherutil import WeatherUtil


class TestWeatherUtil(unittest.TestCase):
    def setUp(self):
        self.config_section = "WeatherUrls"
        self.condition = "clear"
        self.icon_path = "app/img/"
        self.fake_lat = "12.123"
        self.fake_lon = "55.345"
        self.suntimes = {"sunrise": datetime.datetime(2016,12,03,6,10),"sunset":datetime.datetime(2016,12,03,16,45)}
        self.provider_base_url = "http://api.wunderground.com/api/1d70f175da750a8a/"
        self.config_opts = {"CurrentConditions": self.provider_base_url + "conditions/q/{}/{}.json",
                            "Forecast": self.provider_base_url + "forecast/q/{}/{}.json",
                            "SearchLocation": "http://autocomplete.wunderground.com/aq?query={}"
                            }
        self.weather_util = WeatherUtil()

    def test_get_property_from_config_file(self):
        self.assertEqual(self.weather_util.get_property_from_config_file(self.config_section, "CurrentConditions"),
                         self.config_opts.get("CurrentConditions"))
        self.assertEqual(self.weather_util.get_property_from_config_file(self.config_section, "Forecast"),
                         self.config_opts.get("Forecast"))
        self.assertEqual(self.weather_util.get_property_from_config_file(self.config_section, "SearchLocation"),
                         self.config_opts.get("SearchLocation"))

    @patch.object(WeatherUtil,'is_night',MagicMock(return_value=False))
    def test_get_icon_for_conditions_returns_day_icon_path(self):
        self.assertEqual(self.weather_util.get_icon_for_conditions(self.condition, self.fake_lat, self.fake_lon, False),
                         self.icon_path + self.condition + ".png")

    @patch.object(WeatherUtil, 'is_night', MagicMock(return_value=True))
    def test_get_icon_for_conditions_returns_night_icon_path(self):
        self.assertEqual(self.weather_util.get_icon_for_conditions("clear", self.fake_lat, self.fake_lon, False),
                         self.icon_path + self.condition+"night" + ".png")

    def test_get_icon_for_conditions_returns_day_icon_for_forecast(self):
        self.assertEqual(self.weather_util.get_icon_for_conditions("clear", self.fake_lat, self.fake_lon, True),
                         self.icon_path + "clear" + ".png")

    def test_get_icon_for_conditions_returns_unknown_icon_for_unknown_condition(self):
        self.assertEqual(self.weather_util.get_icon_for_conditions("notAValidCondition", self.fake_lat, self.fake_lon, False),
                        self.icon_path + "unknown" + ".png")

    @patch.object(WeatherUtil, 'time_in_range', MagicMock(return_value=False))
    def test_is_night_returns_false(self):
        self.assertFalse(self.weather_util.is_night(self.fake_lat,self.fake_lon))

    @patch.object(WeatherUtil, 'time_in_range', MagicMock(return_value=True))
    def test_is_night_return_true(self):
        self.assertTrue(self.weather_util.is_night(self.fake_lat,self.fake_lon))

    @patch.object(WeatherUtil, 'calculate_sun_rise_and_set')
    def test_calculate_sun_rise_and_set(self,mock_suntimes):
        mock_suntimes.return_value=self.suntimes
        actual_results = self.weather_util.calculate_sun_rise_and_set(self.fake_lat,self.fake_lon)
        self.assertDictEqual(actual_results,self.suntimes)

    def test_time_in_range(self):
        freezer = freeze_time("2016-12-04 13:00:00")
        freezer.start()
        self.assertTrue(self.weather_util.time_in_range(datetime.time(06,10,0),datetime.time(16,45,0)))
        freezer.stop()
        freezer = freeze_time("2016-12-04 22:00:00")
        freezer.start()
        self.assertFalse(self.weather_util.time_in_range(datetime.time(06, 10, 0), datetime.time(16, 45, 0)))
        freezer.stop()

    def test_image_exists(self):
        self.assertTrue(self.weather_util.image_exits("app/img/cloudy.png"))
        self.assertFalse(self.weather_util.image_exits("not_valid_path"))

