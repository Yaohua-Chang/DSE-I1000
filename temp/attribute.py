class Attribute:
    def __init__(self, name, type):
        self.name = name
        self.type = type
        self.less_than_value = None
        self.more_than_value = None

    def set_less_than_value(self, value):
         self.less_than_value = value
    
    def set_more_than_value(self, value):
         self.more_than_value = value