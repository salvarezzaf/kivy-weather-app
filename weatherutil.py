import ConfigParser
import ephem
import datetime
import os

"""
    Utility class to help with common tasks related to api handling
    and data processing.

"""

class WeatherUtil:
    """
        Reads configuration.ini file for a specific section and option
        and return the option value.
        
        Args:
            section: config file section name
            option: property name within a config file section
        Returns:
            string value of the option is exists else none        
    """
    def get_property_from_config_file(self, section, option):
        configOption = {}
        config = ConfigParser.ConfigParser()
        config.read("config/configuration.ini")
        configOption[option] = config.get(section, option)
        return configOption.get(option)
    
    """
        Calculate the path to the right weather icon according to
        time of the day and current weather conditions.
        
        Args:
            iconName: icon field coming from weather api response
            lat: latitude value for location coming from weather api response
            long: longitude value for location coming from weather api response
        Returns:
            string corresponding to icon path in img folder
        
    """    
    def get_icon_for_conditions(self,iconName,lat,long):
        base_path = "img/"
        img_ext = ".png"
        night_icon = base_path + iconName + "night" + img_ext
        day_icon = base_path + iconName + img_ext
        unknown_icon = base_path + "unknown" + img_ext
        
        if self.is_night(lat, long):
            if self.image_exits(night_icon):
                return night_icon
            elif self.image_exits(day_icon):
                return day_icon
            else:
                return unknown_icon          
        else:
            if self.image_exits(day_icon):
                return day_icon
            else:
                return unknown_icon    
            
    
    """
        Check if current time is within night time, if it is
        function returns true or false.
        
        Args:
            lat: latitude for location
            long: longitude for location
            
        Returns:
            True/False
    
    """    
    def is_night(self, lat,long):
        suntimes = self.calculate_sun_rise_and_set(lat, long)
        sunrise = suntimes.get("sunrise").time()
        sunset = suntimes.get("sunset").time()
        if self.time_in_range(sunset, sunrise):
            return True
        else:
            return False
        
    
    """
      Calculates sun rise and set for the location identified by lat and long
      It makes use of ephem library to calculate sun position in time for location
      
      Args:
          lat: latitude value for current location
          long: longitude value for current location
      Returns:
          Dict with sun rise and set time
        
    """    
    def calculate_sun_rise_and_set(self,lat,long):
        now = datetime.datetime.now()
        location = ephem.Observer()
        location.lat=lat
        location.long = long
        location.date = now
        sun = ephem.Sun()        
        suntimes = {"sunrise": ephem.localtime(location.next_rising(sun)),"sunset":ephem.localtime(location.next_setting(sun))}
        return suntimes
        
    """
        Check if current time is within range start_time and end_time
        This method is used in conjunction with is_night to understand if
        night icons need to be loaded instead
        
        Args:
            start_time: sunset start time for current location
            end_time: sunrise start time for current location
        Returns:
            True/False
    
    """        
    def time_in_range(self,start_time,end_time):
        time_now = datetime.datetime.now().time().replace(microsecond=0)
        if start_time <= end_time:
            return start_time <= time_now <= end_time
        else:
            return start_time <= time_now or time_now <= end_time
        
    def image_exits(self, icon):
        return os.path.isfile(icon)
      