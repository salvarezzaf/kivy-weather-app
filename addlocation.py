from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty  # @UnresolvedImport

class AddLocation(BoxLayout):
    
    search_input = ObjectProperty()
    results = ObjectProperty()
    
    def search_city(self):
        test_list_item = self.search_input.text
        if  not self.results.item_strings:
            self.results.item_strings = test_list_item
        else:
            self.results.item_strings.append(test_list_item)
        #self.results.adapter.data.clear()  
        #self.results.adapter.data.extend(test_list_item)  
        #self.results._trigger_reset_populate()  
        