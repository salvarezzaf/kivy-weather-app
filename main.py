from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder
from kivy.factory import Factory
from currentconditions import CurrentCondition
from kivy.utils import get_color_from_hex
from kivy.core.window import Window
from kivy.core.text import LabelBase

Builder.load_file("kvFiles/currentconditions.kv")
Factory.register("CurrentCondition", cls=CurrentCondition)

class YamaRoot(BoxLayout):
    pass


class YamaApp(App):
    pass

if __name__ == '__main__':
    Window.clearcolor = get_color_from_hex('#34495e')
    LabelBase.register("OpenSans", fn_regular="fonts/OpenSans-Regular.ttf")
    YamaApp().run()
